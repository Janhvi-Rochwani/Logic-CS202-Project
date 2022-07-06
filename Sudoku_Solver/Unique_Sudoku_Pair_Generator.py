import itertools
from pysat.formula import CNF, IDPool
from pysat.card import *
from pysat.solvers import Solver
import csv

# start = time.time()
k = int(input())

sudoku1 = []
sudoku2 = []
digits = range(1, (k*k)+1)
block_heads = range(1, (k*k)+1, k)
restrictions = []

i = 0

with open("tests/sudoku_with_dimension_%s.csv" % k, newline='\n') as csvfile:
  #input csv file 
    csvReader = csv.reader(csvfile)   
    for row in csvReader:
        if(i<k*k):
          sudoku1.append(row)
          i = i+1
        else:
            sudoku2.append(row)
            i = i+1

cnf = CNF()


vpool = IDPool(start_from=1)
bla = lambda i, j, k: vpool.id('bla{0}@{1}@{2}'.format(i, j, k))

vpool2 = IDPool(start_from=(k**6)+1)
bleh = lambda i, j, k: vpool.id('bleh{0}@{1}@{2}'.format(i, j, k))

for (a, b) in itertools.product(digits, repeat = 2):
    # each cell has only one digit
    cnf.extend(CardEnc.equals(lits=[bla(a, b, c) for c in digits], encoding=EncType.pairwise, bound = 1))

for (b, c) in itertools.product(digits, repeat = 2): 
    # each digit appears only once in column b
    cnf.extend(CardEnc.equals(lits = [bla(a, b, c) for a in digits], encoding= EncType.pairwise, bound = 1))

for (a, c) in itertools.product(digits, repeat = 2): 
    # each digit appears only once in row a
    cnf.extend(CardEnc.equals(lits = [bla(a, b, c) for b in digits], encoding= EncType.pairwise, bound = 1))

for (a, b) in itertools.product(block_heads, repeat = 2):
    # each digit appears only once in a k*k block
  for c in digits:
    cnf.extend(CardEnc.equals(lits = [bla(a + add_a, b + add_b, c) for (add_a, add_b) in itertools.product(range(k), repeat = 2)], encoding= EncType.pairwise, bound = 1))

for (a, b) in itertools.product(digits, repeat = 2): 
    # taking care of already filled cells
    if int(sudoku1[a-1][b-1]) != 0:
      c = int(sudoku1[a-1][b-1])
      assert(c in digits)
      restrictions.append(bla(a, b, c))
  #SUDOKU_1^^^

      
for (a, b) in itertools.product(digits, repeat = 2):
    # each cell has only one digit
    cnf.extend(CardEnc.equals(lits=[bleh(a, b, c) for c in digits], encoding=EncType.pairwise, bound = 1))

for (b, c) in itertools.product(digits, repeat = 2): 
    # each digit appears only once in column b
      cnf.extend(CardEnc.equals(lits = [bleh(a, b, c) for a in digits], encoding= EncType.pairwise, bound = 1))

for (a, c) in itertools.product(digits, repeat = 2): 
    # each digit appears only once in row a    
      cnf.extend(CardEnc.equals(lits = [bleh(a, b, c) for b in digits], encoding= EncType.pairwise, bound = 1))
        
for (a, b) in itertools.product(block_heads, repeat = 2):
    # each digit appears only once in a k*k block
  for c in digits:
      cnf.extend(CardEnc.equals(lits = [bleh(a + add_a, b + add_b, c) for (add_a, add_b) in itertools.product(range(k), repeat = 2)], encoding= EncType.pairwise, bound = 1))

for (a, b) in itertools.product(digits, repeat = 2): 
    # taking care of already filled cells
    if int(sudoku2[a-1][b-1]) != 0:
      c = int(sudoku2[a-1][b-1])
      assert(c in digits)
      restrictions.append(bleh(a, b, c))  
  #SUDOKU_2^^^



for (a, b, c) in itertools.product(digits, repeat = 3):
    cnf.extend(CardEnc.atmost(lits = [bla(a, b, c), bleh(a, b, c)], encoding= EncType.pairwise, bound = 1))
  #Each cell of sudoku 1 and 2 should have diff digits
  #optimise



s = Solver(name='g4')

for cl in cnf.clauses:
  s.add_clause(cl)


s.solve(assumptions= restrictions)

p = 0
flag = 0

sol = s.get_model()

if (sol):
  sol1 = []
  sol2 = []
  for i in range((k**6)):
    if sol[i]>0:
      id = vpool.obj(sol[i])
      sol1.append(int(id.split("@")[2]))
  for i in range(k**6):
    j = i + k**6
    if sol[j]>0:
      id = vpool.obj(sol[j])
      sol2.append(int(id.split("@")[2]))

  one = []; two = []
  for i in range(k*k):
    one.append([sol1[i*k*k + j] for j in range(k*k)])
  for i in range(k*k):
    two.append([sol2[i*k*k + j] for j in range(k*k)])

  print(one)
  print(two)

else:
  flag = 1
  print("None")

line1 = [["Sudoku1"]]
line2 = [["Sudoku2"]]
line3 = [["None"]]

with open("tests/sudoku_with_dimension_%s_output.csv" % k, 'w', newline='\n') as csvfile:
    csvwriter = csv.writer(csvfile)
    if(flag!=1):
        csvwriter.writerows(line1)
        csvwriter.writerows(one)
        csvwriter.writerows(line2)
        csvwriter.writerows(two)
    if(flag==1):
        csvwriter.writerows(line3)

s.delete()

# end = time.time()
# print(end - start)