from os import listdir

from arguments import parse_args
from constants import file_names, input_folder
from persist   import load, read, write
from utils     import error

import algo, solver

def main():
  data = read(file_name)

  if use_solver and args['load']:
    args['load'] = load(file_name, strategy)

  solution = run(data)

  write(solution, file_name, strategy, use_solver, **args)

def run(data):
  try:
    # Run specified strategy by calling associated function
    module = solver if use_solver else algo
    fn = getattr(module, strategy)
  except AttributeError:
    name = str(module.__name__)
    error('Failed to find "' + strategy + '" strategy in module "' + name + '"')

  solution = fn(data, **args)

  return solution

if __name__ == '__main__':
  args = parse_args()
  base_args = ['file_name', 'strategy', 'use_solver']
  file_name, strategy, use_solver = [args.pop(arg) for arg in base_args]

  if file_name == 'all':
    for file_name in file_names:
      main()
  else:
    main()
