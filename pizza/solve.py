import localsolver

import numpy as np

from functools import partial
from os.path   import join

from arguments import parse_args
from constants import file_names, input_extension, input_folder
from constants import output_extension, output_solve_folder
from data      import evaluate, load as load_data, read, write as write_data
from utils     import cache as cache_data

# -------------------------------- Data ----------------------------------------
cache = partial(cache_data, True)

def write(solution):
  name = file_name + '_' + str(evaluate(solution)) + output_extension
  path = join(output_solve_folder, name)
  write_data(path, solution)

# ---------------------------- Preprocessing -----------------------------------
def preprocess(data, recompute, display):
  R, C, L, H, tomatoes = data
  patterns = compute_patterns(L, H)

  inputs = (R, C, L, tomatoes, patterns, display)
  slices, areas, overlap = cache(get_slices, inputs, recompute, (R, C))

  return R, C, slices, areas, overlap

def compute_patterns(L, H):
  p = []
  for w in range(0, H):
    areas = [(w + 1) * (h + 1) for h in range(w, H)]
    p += [(w, h) for h, a in zip(range(w, H), areas) if a >= L * 2 and a <= H]
  p += [(h, w) for w, h in p if w != h]
  return p

def get_slices(R, C, L, tomatoes, patterns, display):
  tomatoes = np.array(tomatoes)
  overlap = [[[] for j in range(C)] for i in range(R)]
  slices, areas = [], []
  for i in range(R):
    if display and i % 50 == 0: print(i)
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

# ---------------------------- Main function -----------------------------------
def main(**args):
  data = read(file_name)
  solution = solve(data, **args)
  write(solution)

def solve(data, recompute, display, load, callback, time, **args):
  R, C, slices, areas, overlap = preprocess(data, recompute, display)

  with localsolver.LocalSolver() as ls:
    model = ls.model

    # Variables
    x = [model.bool() for i in range(len(slices))]

    # Constraints
    for i in range(R):
      if display and i % 50 == 0: print(str(i) + '/' + str(R))
      for j in range(C):
        model.constraint(model.sum(x[s] for s in overlap[i][j]) <= 1)

    # Objective
    model.maximize(model.sum(s * area for s, area in zip(x, areas)))

    model.close()

    if callback: set_callback(ls, slices, x)
    if load: load_initial_position(load, slices, x)

    ls.create_phase().time_limit = int(time)

    ls.solve()

    solution = retrieve_solution(slices, x)

    return solution

# -------------------------------- Load ----------------------------------------
def load_initial_position(name, slices, x):
  path = join(output_solve_folder, file_name + '_' + name + output_extension)
  solution = set(load_data(path))

  def keep_slice(s):
    return all([min(c % 250, 250 - (c % 250)) >= 8 for c in s])

  start = [1 if s in solution and keep_slice(s) else 0 for s in slices]

  for s, v in zip(x, start):
    if v == 1:
      s.value = 1

# -------------------------------- Utils ---------------------------------------
def set_callback(ls, slices, x):
  def cb(ls, code):
    solution = retrieve_solution(slices, x)
    write(solution)

  ls.add_callback(localsolver.LSCallbackType.DISPLAY, cb)

def retrieve_solution(slices, x):
  solution = [coords for s, coords in enumerate(slices) if x[s].value == 1]
  return solution

# ------------------------------ Arguments -------------------------------------
if __name__ == '__main__':
  parsed_args = parse_args(True)
  file_name = parsed_args.pop('file_name')

  if file_name == 'all':
    for file_name in file_names:
      main(**parsed_args)
  else:
    main(**parsed_args)
