import os
import numpy as np

# ------------------------- Command line arguments -----------------------------
algo_flags = [
  ('v', 'vertical', 'Thin slices computed column-wise'),
]

algo_args = [
  ('d', 'divide', 10, 'Divide pizza into smaller squares')
]

# ----------------------------- Strategies -------------------------------------
def default(data, **args):
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
