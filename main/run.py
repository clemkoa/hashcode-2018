import numpy as np

from copy      import deepcopy
from functools import partial
from os        import walk
from os.path   import join
from zipfile   import ZipFile, ZIP_DEFLATED

from arguments import parse_args
from constants import file_names, output_extension, output_run_folder
from data      import evaluate, read, write as write_data
from utils     import cache as cache_data
from utils     import *

cache = partial(cache_data, False)
def write(data, solution):
    name = file_name + '_' + str(evaluate(data, solution)) + output_extension
    path = join(output_run_folder, name)
    write_data(path, solution)

def zip_code():
    def zipdir(path, zip_output):
        # ziph is zipfile handle
        for root, dirs, files in walk(path):
            for file in files:
                if file.endswith('.py') or file.endswith('.in') or file.endswith('.dat'):
                    zip_output.write(join(root, file))

    zip_output = ZipFile('output/run/code.zip', 'w', ZIP_DEFLATED)
    zipdir('../main', zip_output)
    zip_output.close()

# ---------------------------- Main functions ----------------------------------
def run(**args):
    data = read(file_name)
    (R, C, F, N, B, T, _rides) = deepcopy(data)
    print('number of rows', R)
    print('number of columns', C)
    print('number of vehicles', F)
    print('number of rides', N)
    print('bonus', B)
    print('number of time steps', T)
    # for ride in rides:
    #     print('ride', ride)
    #     ((a, b), (x, y), s, f) = ride

    cars = range(F)
    solution = [[] for car in cars]
    positions = [(0,0) for p in cars]
    print(cars)
    print(positions)
    rides = _rides

    print()
    print()
    print()
    free_cars = [0 for car in cars]
    taken_rides = [False for r in rides]
    for time_step in range(T):
        if time_step % 500 == 0:
            print('time step', time_step)
        for car in cars:
            if free_cars[car] > time_step:
                continue
            for index_ride, ride in enumerate(rides):
                if taken_rides[index_ride]:
                    continue
                ((a, b), (x, y), s, f) = ride
                if (is_ride_valid_from_position(positions[car][0], positions[car][1], time_step, a, b, x, y, s, f)):
                    taken_rides[index_ride] = True
                    solution[car].append(index_ride)
                    positions[car] = (x,y)
                    free_cars[car] = f
                    break

    print(solution[0])
    write(data, solution)
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
