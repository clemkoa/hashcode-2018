from argparse import ArgumentParser
from sys      import argv

from utils  import error

# -------------------- Command line arguments for run.py -----------------------
run_flags = [
  ('f', 'flag', 'Test flag description')
]

run_args = [
  ('a', 'argument', 'default', 'Test argument description')
]

# ------------------- Command line arguments for solve.py ----------------------
solve_flags = [
  ('c', 'callback', 'Set display callback')
]

solve_args = [
  ('t', 'time', 10, 'Time to let LocalSolver run'),
  ('l', 'load', '', 'Path for loading initial position')
]

# ------------------------------- Parsing --------------------------------------
def check_flags_and_args(use_solver):
  flags = solve_flags if use_solver else run_flags
  args  = solve_args  if use_solver else run_args

  short_versions = [arg[0] for arg in flags + args]
  long_versions = [arg[1] for arg in flags + args]

  if len(short_versions) != len(set(short_versions)):
    error('Collision in argument short versions')
  if len(long_versions) != len(set(long_versions)):
    error('Collision in argument long versions')

  for flag in flags:
    if len(flag) != 3:
      error('Flags should be (short, long, help), not ' + str(flag))
  for arg in args:
    if len(arg) != 4:
      error('Args should be (short, long, default, help), not ' + str(arg))

  return flags, args

def parse_args(use_solver):
  parser = ArgumentParser()

  parser.add_argument('file_name', help='Input file name (no extension)')

  flags, args = check_flags_and_args(use_solver)
  for short, long_version, help_str in flags:
    parser.add_argument('-' + short, '--' + long_version, action='store_true',
                        help=help_str)

  for short, long_version, default, help_str in args:
    parser.add_argument('-' + short, '--' + long_version, default=default,
                        help=help_str)

  args = vars(parser.parse_args())

  return args
