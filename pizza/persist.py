from inspect import signature
from os      import listdir, mkdir
from os.path import exists, join

from constants import input_folder, input_extension, output_extension
from constants import output_algo_folder, output_folder, output_solver_folder
from data      import evaluate, load_solution, parse, persist

import algo, solver

# ---------------------------------- I/O ---------------------------------------
def read(name):
  with open(join(input_folder, name + input_extension), 'r') as f:
    return parse(f)

def write(solution, file_name, strategy, use_solver, **args):
  score = evaluate(solution)
  print('Score: ' + str(score))

  folder = get_strategy_folder(use_solver, strategy)
  path = get_output_path(folder, file_name, strategy, use_solver, score, **args)
  with open(path, 'w') as f:
    persist(solution, f)

def load(file_name, strategy):
  path = get_best_solution_path(file_name)
  with open(path, 'r') as f:
    solution = load_solution(f)
    score = evaluate(solution)
    print('Loaded starting position from ' + path + ' with score ' + str(score))
    return solution

# --------------------------------- Paths --------------------------------------
def get_strategy_folder(use_solver, strategy):
  main_folder = output_solver_folder if use_solver else output_algo_folder
  if not exists(main_folder):
    mkdir(main_folder)

  strategy_folder = join(main_folder, strategy)
  if not exists(strategy_folder):
    mkdir(strategy_folder)

  return strategy_folder

def get_output_path(folder, file_name, strategy, use_solver, score, **args):
  module = solver if use_solver else algo
  parameters = signature(getattr(module, strategy)).parameters
  function_args = list(parameters.keys())[1:-1]
  args_str = '_'.join([str(args[arg]) for arg in function_args])
  args_str = '_' + args_str if args_str else ''

  name = file_name + '_' + str(score) + args_str + output_extension

  return join(folder, name)

def get_best_solution_path(file_name):
  folders = [join(output_algo_folder, f) for f in listdir(output_algo_folder)]

  all_paths = []
  for folder in folders:
    paths = [f for f in listdir(folder) if f.startswith(file_name)]
    scores = [path.split('.')[0].split('_')[1] for path in paths]
    try:
      best = max(scores)
      path = join(folder, paths[scores.index(best)])
      all_paths.append((best, path))
    except ValueError:
      pass

  path = sorted(all_paths)[-1][1]

  return path
