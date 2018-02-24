from os      import listdir
from os.path import join

input_folder = 'input'
input_extension = '.in'

output_folder = 'output'
output_algo_folder = join(output_folder, 'algo')
output_solver_folder = join(output_folder, 'solver')
output_extension = '.dat'

file_names = [f.split('.')[0] for f in listdir(input_folder)]
