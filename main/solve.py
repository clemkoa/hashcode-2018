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
  write(solution)

def solve(data, load, callback, time, **args):
  data = preprocess(data)

  with localsolver.LocalSolver() as ls:
    model = ls.model

    # Variables
    # x = [model.bool() for i in range(len(slices))]

    # Constraints
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

# --------------------------- Argument parsing ---------------------------------
if __name__ == '__main__':
  parsed_args = parse_args(True)
  file_name = parsed_args.pop('file_name')

  if file_name == 'all':
    for file_name in file_names:
      main(**parsed_args)
  else:
    main(**parsed_args)
