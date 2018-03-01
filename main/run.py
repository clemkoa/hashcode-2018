import numpy as np

from functools import partial
from os        import walk
from os.path   import join
from zipfile   import ZipFile, ZIP_DEFLATED

from arguments import parse_args
from constants import file_names, output_extension, output_run_folder
from data      import evaluate, read, write as write_data
from utils     import cache as cache_data

cache = partial(cache_data, False)
def write(solution):
    name = file_name + '_' + str(evaluate(solution)) + output_extension
    path = join(output_run_folder, name)
    write_data(path, solution)

def zip_code():
    def zipdir(path, zip_output):
        # ziph is zipfile handle
        for root, dirs, files in walk(path):
            for file in files:
                zip_output.write(join(root, file))

    zip_output = ZipFile('../code.zip', 'w', ZIP_DEFLATED)
    zipdir('../main', zip_output)
    zip_output.close()

# ---------------------------- Main functions ----------------------------------
def run(**args):
    data = read(file_name)
    solution = data
    write(solution)
    zip_code()

# --------------------------- Argument parsing ---------------------------------
if __name__ == '__main__':
    parsed_args = parse_args(False)
    file_name = parsed_args.pop('file_name')

    if file_name == 'all':
        for file_name in file_names:
            run(**parsed_args)
    else:
        run(**parsed_args)
