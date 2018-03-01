import localsolver

from functools import partial
from os.path   import join

from arguments import parse_args
from constants import file_names, output_extension, output_solve_folder
from data      import evaluate, load as load_data, read, write as write_data
from utils     import cache as cache_data

# -------------------------------- Data ----------------------------------------
cache = partial(cache_data, True)

def write(data, olution):
  name = file_name + '_' + str(evaluate(data, solution)) + output_extension
  path = join(output_solve_folder, name)
  write_data(path, solution)

# ---------------------------- Preprocessing -----------------------------------
def preprocess(data):
  return data

# ---------------------------- Main function -----------------------------------
def main(**args):
  data = read(file_name)
  solution = solve(data, **args)
  # write(data, [[0], [1, 3, 5]])

def solve(data, load, callback, time, **args):
  # data = preprocess(data)
  R, C, F, N, B, T, demand = data

  with localsolver.LocalSolver() as ls:
    model = ls.model

    # Data
    times = model.array(build_times([((0, 0), (0, 0), 0, 0)] + demand))
    max_lates = model.array([e - s for _, _, s, e in demand])

    # Variables
    cars = [model.list(N) for i in range(F)]

    # Expressions
    lates = [model.array(model.range(0, N), lambda i, prev, a=4, b=6, c=3, car=car: model.max(0, prev + \
      (model.at(times, 0, car[0] + 1) if i == 0 else \
      model.at(times, car[i-1] + 1, \
      car[i] + 1)))) for car in cars]

    # Constraints
    model.constraint(model.disjoint(cars))
    for k, car in enumerate(cars):
      for i in range(N):
        model.constraint(i >= model.count(car) or (lates[k,i] <= model.at(max_lates, car[i])))

    # Objective
    model.maximize(model.sum([model.count(car) for car in cars]))

    model.close()

    l = cars[0].get_value()
    l.clear()
    l.add(0)


    a = cars[1].get_value()
    a.clear()
    a.add(1)
    a.add(2)


    if callback: set_callback(ls)
    if load: load_initial_position(load)

    ls.create_phase().time_limit = int(time)

    print('OK')
    ls.solve()

    for car in cars:
      print(car.value)
    for late in lates:
      print(late.value)
    print(max_lates.value)
    print(build_times([((0, 0), (0, 0), 0, 0)] + demand))

    # solution = retrieve_solution(cars, lates, N)

    print(ls.compute_inconsistency())

    return solution

# -------------------------------- Load ----------------------------------------
def load_initial_position(name):
  raise NotImplementedError

# -------------------------------- Utils ---------------------------------------
def set_callback(ls):
  def cb(ls, code):
    raise NotImplementedError

  ls.add_callback(localsolver.LSCallbackType.DISPLAY, cb)

def retrieve_solution(cars, lates, N):
  for car in cars:
    print(car.value)
  for late in lates:
    print(late.value)

  return []

def dist(start, end):
  (ys, xs), (ye, xe) = start, end
  return abs(ys - ye) + abs(xs - xe)

def build_times(demand):
  def check(first, second):
    ride = dist(first[0], first[1]) + dist(first[1], second[0])
    return first[2] + ride - second[2]
  times = [[check(first, second) for second in demand] for first in demand]
  return times

# --------------------------- Argument parsing ---------------------------------
if __name__ == '__main__':
  parsed_args = parse_args(True)
  file_name = parsed_args.pop('file_name')

  if file_name == 'all':
    for file_name in file_names:
      main(**parsed_args)
  else:
    main(**parsed_args)
