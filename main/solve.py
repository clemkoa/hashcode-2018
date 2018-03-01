import localsolver

from functools import partial
from os.path   import join

from arguments import parse_args
from constants import file_names, output_extension, output_solve_folder
from data      import evaluate, load as load_data, read, write as write_data
from utils     import cache as cache_data

# -------------------------------- Data ----------------------------------------
cache = partial(cache_data, True)

def write(solution):
  name = file_name + '_' + str(evaluate(solution)) + output_extension
  path = join(output_solve_folder, name)
  write_data(path, solution)

# ---------------------------- Preprocessing -----------------------------------
def preprocess(data):
  return data

# ---------------------------- Main function -----------------------------------
def main(**args):
  data = read(file_name)
  solution = solve(data, **args)
  # write([[0], [1, 3, 5]])

def solve(data, load, callback, time, **args):
  # data = preprocess(data)
  R, C, F, N, B, T, demand = data
  compatible = build_compatible(demand)
  print(compatible)

  assert False

  starts = []

  with localsolver.LocalSolver() as ls:
    model = ls.model

    # # Data
    # starts = [start for start, _, _, _ in demand]
    # ends = [end for _, end, _, _ in demand]
    # startX = model.array([x for _, x in starts])
    # startY = model.array([y for y, _ in starts])
    # startT = model.array([t for _, _, t, _ in demand])
    # endX = model.array([x for _, x in ends])
    # endY = model.array([y for y, _ in ends])
    # endT = model.array([t for _, _, _, t in demand])

    # # Variables
    # car = [model.list(N) for i in range(F)]

    # # Constraints
    # model.partition(cars)
    # is_valid = model.function(lambda position, i: position + )
    # for car in cars:


    # model.constraint(model.sum(x[s] for s in overlap[i][j]) <= 1)

    # Objective
    # model.maximize(model.sum(s * area for s, area in zip(x, areas)))

    model.close()

    if callback: set_callback(ls)
    if load: load_initial_position(load)

    ls.create_phase().time_limit = int(time)

    ls.solve()

    solution = retrieve_solution()

    return solution

# -------------------------------- Load ----------------------------------------
def load_initial_position(name):
  raise NotImplementedError

# -------------------------------- Utils ---------------------------------------
def set_callback(ls):
  def cb(ls, code):
    raise NotImplementedError

  ls.add_callback(localsolver.LSCallbackType.DISPLAY, cb)

def retrieve_solution():
  raise NotImplementedError

def dist(start, end):
  (ys, xs), (ye, xe) = start, end
  return abs(ys - ye) + abs(xs - xe)

def build_compatible(demand):
  def check(first, second):
    return second[2] - first[2] + dist(first[1], second[0])
  compatible = [[check(first, second) for second in demand] for first in demand]
  return compatible

# --------------------------- Argument parsing ---------------------------------
if __name__ == '__main__':
  parsed_args = parse_args(True)
  file_name = parsed_args.pop('file_name')

  if file_name == 'all':
    for file_name in file_names:
      main(**parsed_args)
  else:
    main(**parsed_args)
