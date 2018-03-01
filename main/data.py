from os      import mkdir
from os.path import dirname, exists, join

from constants import input_extension, input_folder
from utils     import time_for_ride

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
    solution = [list(map(int, line.split()))[1:] for line in f]
    return solution

# ----------------------------- Evaluation -------------------------------------
# Score solution to avoid stomping our best solutions

def score_driver(data, driver):
    (R, C, F, N, B, T, rides) = data

    driver_time = 0
    driver_pos = (0,0)
    driver_score = 0
    for user in driver:
        start_pos, end_pos, start_T, end_T = rides[user]
        driver_time += time_for_ride(driver_pos[0], driver_pos[1], start_pos[0], start_pos[1])

        #is the driver time below start_T
        if (driver_time < start_T):
            driver_time = start_T

        #The driver has arrived, we start the ride
        bonus = B if (driver_time==start_T) else 0
        timeTravel = time_for_ride(start_pos[0], start_pos[1], end_pos[0], end_pos[1])

        #we update the score
        if ((driver_time+timeTravel)<end_T):
            driver_score += timeTravel + bonus

        #we update the time and the pos
        driver_time += timeTravel
        driver_pos = end_pos

    return driver_score

def evaluate(data, solution):
    # Check that no ride is done twice
    all_rides_done = [item for sublist in solution for item in sublist]
    if len(all_rides_done) != len(set(all_rides_done)):
        raise ValueError('One or more rides are done by several cars')

    score = 0
    for car in solution:
      score += score_driver(data, car)
    print('Score: {}'.format(score))
    return score
