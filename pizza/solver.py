import localsolver

import numpy as np

from pulp import LpInteger, LpMaximize, LpProblem, LpStatus, LpVariable, value

from utils import cache

# ------------------------- Command line arguments -----------------------------
solver_flags = [
  ('l', 'load', 'Load initial position from algo'),
  ('m', 'memoize', 'Store computed data for a faster next run'),
  ('r', 'recompute', 'Recompute memoized data')
]

solver_args = [
  ('t', 'time', 10, 'Time to let LocalSolver run')
]

# ----------------------------- Preprocess -------------------------------------
def preprocess(data, memoize, recompute, **args):
  R, C, L, H, tomatoes = data
  patterns = compute_patterns(L, H)

  inputs = (R, C, L, tomatoes, patterns)
  fn = cache if memoize else lambda f, arguments, r: f(arguments)
  slices, areas, overlap = fn(get_slices, inputs, recompute, (R, C))

  return R, C, slices, areas, overlap

# ----------------------------- Strategies -------------------------------------
def local(data, load, time, **args):
  R, C, slices, areas, overlap = preprocess(data, **args)

  with localsolver.LocalSolver() as ls:
    model = ls.model

    print('Variables')
    # Decision variables
    x = [model.bool() for i in range(len(slices))]

    print('Constraints')
    # Constraints
    for i in range(R):
      if i % 50 == 0: print(i)
      for j in range(C):
        model.constraint(model.sum(x[s] for s in overlap[i][j]) <= 1)

    # Objective
    print('Objective')
    model.maximize(model.sum(s * area for s, area in zip(x, areas)))

    model.close()

    ls.create_phase().time_limit = int(time)
    ls.solve()

    solution = [coords for s, coords in enumerate(slices) if x[s].value == 1]

    return solution

def pulp(data, load, **args):
  R, C, slices, areas, overlap = preprocess(data, **args)

  prob = LpProblem('Pizza', LpMaximize)

  # Variables
  x = [LpVariable('slice_' + str(s), 0, 1) for s in range(len(slices))]

  # Constraints
  for i in range(R):
    for j in range(C):
      prob += sum([x[s] for s in overlap[i][j]]) <= 1

  # Objective
  prob += sum([s * area for s, area in zip(x, areas)])

  prob.solve()

  print("Status = %s" % LpStatus[prob.status])

  solution = [coords for s, coords in enumerate(slices) if x[s].varValue == 1]

  return solution

def compute_patterns(L, H):
  p = []
  for w in range(0, H):
    areas = [(w + 1) * (h + 1) for h in range(w, H)]
    p += [(w, h) for h, a in zip(range(w, H), areas) if a >= L * 2 and a <= H]
  p += [(h, w) for w, h in p if w != h]
  return p

def get_slices(R, C, L, tomatoes, patterns):
  tomatoes = np.array(tomatoes)
  overlap = [[[] for j in range(C)] for i in range(R)]
  slices, areas = [], []
  for i in range(R):
    if i % 50 == 0: print(i)
    for j in range(C):
      for w, h in patterns:
        if i + h < R and j + w < C:
          t = np.sum(tomatoes[i : i + h + 1, j : j + w + 1])
          area = (h + 1) * (w + 1)
          if t >= L and area - t >= L:
            slices.append((i, j, i + h, j + w))
            areas.append(area)
            for di in range(i, i + h + 1):
              for dj in range(j, j + w + 1):
                overlap[di][dj].append(len(slices) - 1)

  return slices, areas, overlap