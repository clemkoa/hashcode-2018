# ------------------------------ Parsing ---------------------------------------
# Parse input data file
def parse(f):
  R, C, L, H = map(int, next(f).split())
  tomatoes = [[1 if c == 'T' else 0 for c in line.strip()] for line in f]
  return R, C, L, H, tomatoes

# ----------------------------- Persistance ------------------------------------
# Write solution to disk in a submission-ready format
def persist(solution, f):
  f.write(str(len(solution)) + '\n')
  for rect in solution:
    f.write(' '.join(map(str, rect)) + '\n')

# Load solution from file for solver to use
def load_solution(f):
  n = int(next(f))
  slices = [tuple(map(int, next(f).split())) for i in range(n)]
  return slices

# ----------------------------- Evaluation -------------------------------------
# Score solution to avoid stomping our best solutions
def evaluate(solution):
  score = sum([(xr - xl + 1) * (yb - yt + 1)  for xl, yt, xr, yb in solution])
  return score
