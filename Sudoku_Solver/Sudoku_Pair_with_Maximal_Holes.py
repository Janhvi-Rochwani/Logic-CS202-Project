import itertools
from pysat.formula import CNF, IDPool
from pysat.card import *
from pysat.solvers import Solver
import csv
import time

def unique_pair(sudoku1, sudoku2, k):
    cnf = CNF()
    digits = range(1, (k*k)+1)
    block_heads = range(1, (k*k)+1, k)
    restrictions = []

    vpool = IDPool(start_from=1)    #ID function for sudoku1
    bla = lambda i, j, k: vpool.id('bla{0}@{1}@{2}'.format(i, j, k))

    vpool2 = IDPool(start_from=(k**6)+1)    #ID function for sudoku2
    bleh = lambda i, j, k: vpool2.id('bleh{0}@{1}@{2}'.format(i, j, k))

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
    
    s = Solver(name='g4')

    for cl in cnf.clauses:
        s.add_clause(cl)

    s.solve(assumptions = restrictions)

    sol = s.get_model()

    if (sol):   #if the formula is unsatisfiable, function returns None
        sol1 = []
        sol2 = []
        for i in range((k**6)):
            if sol[i]>0:
                id = vpool.obj(sol[i])
                sol1.append(int(id.split("@")[2]))  #accessing elements using vpool IDs
        for i in range(k**6):
            j = i + k**6
            if sol[j]>0:
                id = vpool2.obj(sol[j])
                sol2.append(int(id.split("@")[2]))  #accessing elements using vpool IDs

        one = []; two = []

        for i in range(k*k):
            one.append([sol1[i*k*k + j] for j in range(k*k)])
        for i in range(k*k):
            two.append([sol2[i*k*k + j] for j in range(k*k)])
      
        s.delete()
        return one, two
    else: 
        s.delete()
        return 0, 0

def solutions(sudoku1, sudoku2, k):
    #gives 1 if 1 solution

    cnf = CNF()
    digits = range(1, (k*k)+1)
    block_heads = range(1, (k*k)+1, k)
    restrictions = []

    vpool = IDPool(start_from=1)
    bla = lambda i, j, k: vpool.id('bla{0}@{1}@{2}'.format(i, j, k))

    vpool2 = IDPool(start_from=(k**6)+1)
    bleh = lambda i, j, k: vpool2.id('bleh{0}@{1}@{2}'.format(i, j, k))

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

    s.solve(assumptions = restrictions)
        
    count = 0   #keeping track of number of models
    for m in s.enum_models(assumptions = restrictions):
        count += 1
        if(count>1):
            break
    s.delete()
    return count

def is_redundant_cell(sudoku1, a, b, sudoku2, k):
    trial = sudoku1[a-1][b-1]
    sudoku1[a-1][b-1] = 0
    g = solutions(sudoku1, sudoku2, k)
    if(g>1):    #if more than one solution exists, do not create hole at (a, b)
        sudoku1[a-1][b-1] = trial
    return sudoku1, sudoku2

# start = time.time()

k = int(input())
digits = range(1, (k*k)+1)
sudoku1 = [[0 for x in range(k*k)] for y in range(k*k)]
sudoku2 = [[0 for x in range(k*k)] for y in range(k*k)]

sol1, sol2 = unique_pair(sudoku1, sudoku2, k)

for (a, b) in itertools.product(digits, repeat = 2):
    sol1, sol2 = is_redundant_cell(sol1, a, b, sol2, k)
    #checking for holes
for (a, b) in itertools.product(digits, repeat = 2):
    sol2, sol1 = is_redundant_cell(sol2, a, b, sol1, k)
    
line1 = [["Sudoku1"]]
line2 = [["Sudoku2"]]

filename = "Q2_output.csv"

with open(filename, 'w', newline='\n') as csvfile: 
    csvwriter = csv.writer(csvfile)        
    csvwriter.writerows(line1)
    csvwriter.writerows(sol1)
    csvwriter.writerows(line2)
    csvwriter.writerows(sol2)

# end = time.time()
# print(end - start)