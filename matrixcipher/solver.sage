from sage.modules.free_module_integer import IntegerLattice
from random import randint
import sys
from itertools import starmap
from operator import mul

with open("output.txt", "r") as f:
    A_values = eval(f.readline().strip())
    b_values = eval(f.readline().strip())

# from https://hackmd.io/@hakatashi/B1OM7HFVI
def Babai_closest_vector(M, G, target):
  small = target
  for _ in range(1):
    for i in reversed(range(M.nrows())):
      c = ((small * G[i]) / (G[i] * G[i])).round()
      small -= M[i] * c
  return target - small

m = len(b_values)
n = m

# this time it is enough to set 46*46 matrix
A = matrix(ZZ, m, n)
for x in range(m):
  for y in range(n):
    A[y, x] = A_values[y][x]
lattice = IntegerLattice(A, lll_reduce=True)
print("LLL done")
gram = lattice.reduced_basis.gram_schmidt()[0]
target = vector(ZZ, b_values)
res = Babai_closest_vector(lattice.reduced_basis, gram, target)
print("Closest Vector: {}".format(res))

# caution: It will not work properly without intervening transposition operations.
M = Matrix(ZZ, A_values).transpose()
ingredients = M.solve_right(res)
print("Ingredients: {}".format(ingredients))

flag = ''
for _ in ingredients:
  flag += chr(_)
print(flag)