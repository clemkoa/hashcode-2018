from os      import listdir
from os.path import join

input_folder = 'input'
input_extension = '.in'

output_folder = 'output'
output_run_folder   = join(output_folder, 'run')
output_solve_folder = join(output_folder, 'solve')
output_extension = '.dat'

cache_folder = 'cache'

file_names = [f.split('.')[0] for f in listdir(input_folder)]
