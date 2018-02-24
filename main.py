import os
import numpy as np

data_directory = 'data'
files = ['small.in', 'example.in', 'medium.in', 'big.in']
output_directory = 'output'

def solve_pizza(rows_number,
                columns_number,
                min_ingredient_number,
                max_total_ingredient_number,
                data):
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
    return results

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

def write_results(results, filename):
    text_file = open(os.path.join(output_directory, filename), "w")
    tot = len(results)
    text_file.write(str(tot) + '\n')
    for r in results:
        text_file.write(' '.join([str(s) for s in r]) + '\n')
    text_file.close()


for filename in files:
    f = open(os.path.join(data_directory, filename), 'r+')

    meta_parameters = f.readline().strip().split(' ')
    rows_number = int(meta_parameters[0])
    columns_number = int(meta_parameters[1])
    min_ingredient_number = int(meta_parameters[2])
    max_total_ingredient_number = int(meta_parameters[3])


    array = []
    for line in f.readlines():
        a = [0 if e is 'T' else 1 for e in line.strip()]
        array.append(a)
    n = np.array(array)
    print('Solving...', filename)

    results = solve_pizza(rows_number, columns_number, min_ingredient_number, max_total_ingredient_number, n)
    write_results(results, filename + '.txt')
