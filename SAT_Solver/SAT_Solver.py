import copy
import time

def find_unit_literals(clauses):
    units = []
    for x in clauses:
        if (len(x) == 1) and (x[0] not in units):
            #any clause of the form [l] is a "unit", i.e, l has to be true
            units.append(x[0])
            if (x[0] not in fixed):
                fixed.append(x[0])
                #fixed is the list of literals whose truth value has been decided.
    return units            


def unit_propagate(l, clauses):
    tempty = []
    for x in clauses:
        if l in x:
            tempty.append(x)
            #clauses of the form [l, a1, a2, ..] will be true as l is fixed to be true
        elif -l in x:
            x.remove(-l)
            #clauses of the form [-l, a1, a2, ..] will be reduced to [a1, a2, ...]
    for y in tempty:
        clauses.remove(y)


def find_pure_literals(clauses):
    exists = [0 for n in range(nof_variables)]
    bar_exists = [0 for n in range(nof_variables)]
    pures = []
    for i in range(1, nof_variables+1):
        for l in clauses:
            if i in l:
                exists[i-1] = 1 #if a literal i exists in the clauses
                break
        for l in clauses:
            if -i in l:
                bar_exists[i-1] = 1 #if a literal -i exists in the clauses
                break
        if (exists[i-1] == 1 and bar_exists[i-1] == 0):
            pures.append(i) #if i is present and -i is not present, i is "pure"
        if (exists[i-1] == 0 and bar_exists[i-1] == 1):
            pures.append(-i)
    return pures

def pure_literal_assign(clauses, pures):
    for x in pures:
        waste = []
        if (x not in fixed):
            fixed.append(x) #truth values of pure literals are also fixed
        for this_clause in clauses:
            if x in this_clause:
                waste.append(this_clause)
        '''
        introduced a new temporary list because
        iterating on a list while editing it leads to erroneous results
        '''

        for this_clause in waste:
            clauses.remove(this_clause)   


def DPLL(clauses, fixed):
    # cnf = copy.deepcopy(clauses)
    flag = 1 #ensures that the while loop runs at least once
    units = []
    while(flag or len(units)):
        flag = 0
        units = find_unit_literals(clauses) #finds unit clauses
        for l in units:
            unit_propagate(l, clauses) #removes clauses and literals based on l

    flag = 1 #ensures that the while loop runs at least once
    pures = []
    while(flag or len(pures)):
        flag = 0
        pures = find_pure_literals(clauses) #finds unit clauses
        pure_literal_assign(clauses, pures) #removes clauses and literals based on l

    if (len(clauses) == 0):
        #all clauses have been satisfied either via unit literals or pure literals
        return True

    for x in clauses:
        '''
        a literal is removed from a clause only when it is impossible to set it as True.
        If a clause is empty, all literals in it must have been false.
        An empty clause indicates that the formula is UNSAT.
        '''
        if len(x) == 0:
            return False
    '''
    direct assignment in python using equals '=' does not create a new list
    we have used the deepcopy() operation to copy the old list into a new one
    '''
    new_list_1 = copy.deepcopy(clauses)
    new_list_2 = copy.deepcopy(clauses)
    new_fixed_1 = copy.deepcopy(fixed)
    new_fixed_2 = copy.deepcopy(fixed)

    count = [0 for n in range(2*nof_variables)]
    max_count = 0
    max_literal = 0
    #finding the literal that occurs maximum number of times
    for this_clause in clauses:
        for l in this_clause:
            if l>0:
                count[l-1] += 1
                if(max_count < count[l-1]):
                    max_count = count[l-1]
                    max_literal = l
            if l<0:
                count[nof_variables-l-1]
                if(max_count < count[nof_variables-l-1]):
                    max_count = count[nof_variables-l-1]
                    max_literal = l
    l = max_literal
    '''
    we can ensure most deletions of clauses in the recursive call
    by assuming this max_literal to be True or False
    '''
    new_list_1.append([l])
    new_list_2.append([-l])

    return DPLL(new_list_1, new_fixed_1) or DPLL(new_list_2, new_fixed_2)

#main code
# start = time.time()
filename = "testcase_5.cnf"

with open("testcases/" + filename, "r") as f:
    x = f.readlines()

for line in x:
    if line[0] == "p": #reading the cnf
        nof_clauses = int(line.split(" ")[-1])
        nof_variables = int(line.split(" ")[-2])
        break

formula = []
temp = []
i = 0
flag = 0

for line in x:
    if (line[0] != "p") and (line[0] != "c"):
        for num in range(len(line.split(" ")) - 1):
            temp.append(int(line.split(" ")[num]))
        formula.append(temp)
        temp = [] #reading the cnf
        i = i + 1
        if(i == nof_clauses):
            flag = 1
            break
    if(flag == 1):
        break


fixed = []
model = [0 for n in range(nof_variables)]

if(DPLL(formula, fixed)):
    for x in fixed:
        if x>0:
            model[x-1] = 1
        else:
            model[-x-1] = -1
    print("The formula is satisfiable.")
    print("Model: ", end = "")
    for i in range(1, nof_variables+1):
        '''
        if model[i-1] = 1, i is True
        if model[i-1] = -1, i is False
        if model[i-1] = 0, i can be either True or False
        (we have arbitrarily set all such literals to True for our example model)
        '''
        if model[i-1] >= 0:
            print(i, end=" ")
        else: print(-i, end = " ")
        
else: print("The formula is unsatisfiable.")
print()
# end = time.time()
# print("time taken: ", (end - start))