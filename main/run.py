import numpy as np

from functools import partial
from os.path   import join

from arguments import parse_args
from constants import file_names, output_extension, output_run_folder
from data      import evaluate, read, write as write_data
from utils     import cache as cache_data

cache = partial(cache_data, False)
def write(solution):
    name = file_name + '_' + str(evaluate(solution)) + output_extension
    path = join(output_run_folder, name)
    write_data(path, solution)

# ---------------------------- Main functions ----------------------------------
def run(**args):
    data = read(file_name)
    solution = data
    write(solution)

# --------------------------- Argument parsing ---------------------------------
if __name__ == '__main__':
    parsed_args = parse_args(False)
    file_name = parsed_args.pop('file_name')

    if file_name == 'all':
        for file_name in file_names:
            run(**parsed_args)
    else:
        run(**parsed_args)
