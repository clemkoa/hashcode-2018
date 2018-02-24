from _pickle import dump, load
from os.path import exists, join
from sys     import exit

from constants import cache_folder

def error(message):
  exit('!!! ' + message + ' !!!')

def cache(fn, inputs, recompute=False, args=None):
  args = [] if args is None else args
  path = join(cache_folder, '_'.join([fn.__name__] + list(map(str, args))))

  if not exists(path) or recompute:
    data = fn(*inputs)
    dump(data, open(path, 'wb'))
  else:
    print('Loading memoized data from ' + path)
    data = load(open(path, 'rb'))

  return data
