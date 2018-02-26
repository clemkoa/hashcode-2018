import os

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

# ---------------------------- Main function -----------------------------------
def run(**args):
    data = read(file_name)
    rows_number, columns_number, min_ingredient_number, max_total_ingredient_number, data = data
    data = np.array(data)

    shape = (1, max_total_ingredient_number)
    (x, y) = data.shape
    results = []
    for row in range(x):
        for column in range(y):
            xmin = row
            xmax = xmin + 1
            ymin = column
            ymax = ymin + max_total_ingredient_number - 1
            if (is_slice_okay(xmin, xmax, ymin, ymax, data, min_ingredient_number, max_total_ingredient_number)):
                data = update_slice(xmin, xmax, ymin, ymax, data)
                results.append([xmin, ymin, xmax - 1, ymax - 1])

    write(results)

def is_slice_okay(xmin, xmax, ymin, ymax, data,
                min_ingredient_number,
                max_total_ingredient_number):
    (x, y) = data.shape
    if xmin < 0 or xmax < 0:
        return False
    if xmax > x or ymax > y:
        return False
    s = data[xmin:xmax, ymin:ymax]

    if 2 in np.squeeze(s):
        return False
    mushroom_number = int(np.sum(np.squeeze(s)))
    tomato_number = int((xmin - xmax) * (ymin - ymax) - mushroom_number)

    return ((xmin - xmax) * (ymin - ymax)) <= max_total_ingredient_number and mushroom_number >= min_ingredient_number and tomato_number >= min_ingredient_number

def update_slice(xmin, xmax, ymin, ymax, data):
    data[xmin:xmax, ymin:ymax] = 2.0
    return data

if __name__ == '__main__':
    parsed_args = parse_args(False)
    file_name = parsed_args.pop('file_name')

    if file_name == 'all':
        for file_name in file_names:
            run(**parsed_args)
    else:
        run(**parsed_args)
