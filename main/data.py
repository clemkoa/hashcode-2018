from os      import mkdir
from os.path import dirname, exists, join

from constants import input_extension, input_folder

# ------------------------------ Parsing ---------------------------------------
# Parse input data file
def read(file_name):
  path = join(input_folder, file_name + input_extension)
  with open(path, 'r') as f:
    raise NotImplementedError

# ----------------------------- Persistance ------------------------------------
# Write solution to disk in a submission-ready format
def write(path, solution):
  folder = dirname(path)
  if not exists(folder):
    mkdir(folder)

  with open(path, 'w') as f:
    raise NotImplementedError

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
