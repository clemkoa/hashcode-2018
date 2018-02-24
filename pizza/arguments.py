from argparse import ArgumentParser
from sys      import argv

from algo   import algo_flags, algo_args
from solver import solver_flags, solver_args
from utils import error

def check_flags_and_args():
  use_solver = '-s' in argv or '--use-solver' in argv
  flags = solver_flags if use_solver else algo_flags
  args  = solver_args  if use_solver else algo_args

  short_versions = [arg[0] for arg in flags + args] + ['s']
  long_versions = [arg[1] for arg in flags + args] + ['use-solver']

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

def parse_args():
  parser = ArgumentParser()

  parser.add_argument('file_name', help='Input file name (no extension)')
  parser.add_argument('strategy', help='Main algorithm strategy')
  parser.add_argument('-s', '--use-solver', action='store_true',
                      help='Run using solver')

  flags, args = check_flags_and_args()
  for short, long_version, help_str in flags:
    parser.add_argument('-' + short, '--' + long_version, action='store_true',
                        help=help_str)

  for short, long_version, default, help_str in args:
    parser.add_argument('-' + short, '--' + long_version, default=default,
                        help=help_str)

  args = vars(parser.parse_args())

  return args
