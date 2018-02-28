try:
  from _pickle import dump, load
except ImportError:
  from cPickle import dump, load

from os.path import exists, join
from sys     import exit

from constants import cache_folder

def error(message):
  exit('!!! ' + message + ' !!!')

def cache(use_solver, fn, inputs, recompute=False, args=None):
  args = [] if args is None else list(args)
  args = ['solver' if use_solver else 'run', fn.__name__] + args
  path = join(cache_folder, '_'.join(list(map(str, args))))

  if not exists(path) or recompute:
    data = fn(*inputs)
    dump(data, open(path, 'wb'))
  else:
    print('Loading memoized data from ' + path)
    data = load(open(path, 'rb'))

  return data
