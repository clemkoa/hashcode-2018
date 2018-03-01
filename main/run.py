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
    rides = _rides

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

    # Ride data
    ride_start_pos = np.array([r[0] for r in rides])
    ride_end_pos = np.array([r[1] for r in rides])
    ride_start_times = np.array([r[2] for r in rides])
    ride_end_times = np.array([r[3] for r in rides])

    # Additional ride computation
    ride_times = np.sum(np.abs(ride_start_pos - ride_end_pos), 1)
    ride_latest_start_times = ride_end_times - ride_times

    # Dynamic helpers
    positions = np.array([(0, 0) for p in cars])
    free_cars = np.array([0 for car in cars])
    rides_todo = np.array([True for r in rides])
    for time_step in range(T):
        if np.sum(rides_todo) == 0:
            print('Stopping early, all rides done')
            break
        if np.sum(ride_latest_start_times >= time_step) == 0:
            print('Stopping early, no more rides possible')
            break

        if time_step % 500 == 0:
            print('time step: {}, rides taken: {}, rides still possible: {}, cars in rides: {}'.format(
                time_step,
                len(rides) - np.sum(rides_todo),
                np.sum(ride_latest_start_times >= time_step),
                np.sum(free_cars > time_step)
            ))
        for car in np.where(free_cars <= time_step)[0]:
            time_to_go_to_rides = np.sum(np.abs(ride_start_pos - positions[car]), 1)
            rides_worth_it = (time_to_go_to_rides + time_step) <= ride_latest_start_times
            rides_with_bonus = (time_to_go_to_rides + time_step) <= ride_start_times
            valid_rides = np.logical_and(rides_worth_it, rides_todo)
            time_to_go_to_rides_with_validity = time_to_go_to_rides + 10000000 * np.logical_not(valid_rides)

            # Select closest valid ride
            index_ride = np.argmin(time_to_go_to_rides_with_validity)

            # Check for valid selection
            if not valid_rides[index_ride]:
                break
            ((a, b), (x, y), s, f) = rides[index_ride]

            # Add this ride to this car
            rides_todo[index_ride] = False
            solution[car].append(index_ride)
            # Update car's position and next available time

            positions[car] = (x, y)
            free_cars[car] = time_step + time_to_go_to_rides[index_ride] + ride_times[index_ride]

    print('Final: time step: {}, rides taken: {}, rides still possible: {}, cars in rides: {}'.format(
        time_step,
        len(rides) - np.sum(rides_todo),
        np.sum(ride_latest_start_times >= time_step),
        np.sum(free_cars > time_step)
    ))
    print('Rides missed: {}'.format(
        np.sum(rides_todo)
    ))

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
