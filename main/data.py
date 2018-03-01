from os      import mkdir
from os.path import dirname, exists, join

from constants import input_extension, input_folder

# ------------------------------ Parsing ---------------------------------------
# Parse input data file
def read(file_name):
  path = join(input_folder, file_name + input_extension)
  with open(path, 'r') as f:
    R, C, F, N, B, T = map(int, next(f).split())

    def parse_line(line):
      sy, sx, fy, fx, s, f = map(int, line.split())
      return (sy, sx), (fy, fx), s, f

    demand = [parse_line(line) for line in f]

    return R, C, F, N, B, T, demand

# ----------------------------- Persistance ------------------------------------
# Write solution to disk in a submission-ready format
def write(path, solution):
  folder = dirname(path)
  if not exists(folder):
    mkdir(folder)

  with open(path, 'w') as f:
    for car in solution:
      f.write(str(len(car)) + ' ' + ' '.join(map(str, car)) + '\n')

# Load solution from file for solver to use
def load(path):
  print('Loading solution from ' + path)
  with open(path, 'r') as f:
    raise NotImplementedError

# ----------------------------- Evaluation -------------------------------------
# Score solution to avoid stomping our best solutions
def evaluate(solution):
  print('!!! Evaluation not implemented, returning score of 0 !!!')
  return 0
