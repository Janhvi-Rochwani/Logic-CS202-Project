**Prompt:** Implement a SAT solver. Given a formula in the DIMACS representation, your implementation should return: <br/>
<ol>
<li> A model if the formula is satisfiable
<li>report that the formula is unsatisfiable
</ol> Any test case is run by updating the filename to "<name>.cnf".  <br/>
<br/>

***Solution*** <br/> 
The code first reads the number of variables, number of clauses and all the clauses from this cnf file. It then creates a list of lists to store these clauses.
We have used the DPLL algorithm for the SAT Solver.

A unit literal is a literal l that occurs as a clause of unit length ([l]).
A literal is l said to be "pure" is it occurs in the cnf only as "l" (i.e -l does not appear anywhere in the cnf).

The function *DPLL* calls 4 other functions in one non-recursive run:
The functions *find_unit_literals* and *find_pure_literals* do exactly as their names suggest. 
The functions *unit_propagate* and *pure_literal_assign* are used to eliminate clauses with the fixed literal "l" and for unit literals, to also remove the literal "-l" from the rest of the clauses.

**If the cnf has no more clauses, it must be SAT** because all clauses have been satisfied either via unit literals or pure literals.
If the cnf has any empty clauses, it must be UNSAT. A literal is removed from a clause only when it is impossible to set it as True. If a clause is empty, all literals in it must have been false. Therefore, **an empty clause indicates that the formula is UNSAT**.

If the cnf has non-zero non-empty clauses left, we proceed with assumptions. A literal "l" can either be True or False (if the formula is SAT). So, we assume a literal l to be True and try to solve the formula. If the result is UNSAT, we assume the same literal to be False and try to solve the formula. If the result is UNSAT once again, the original formula must be UNSAT.

The literal chosen for the aforementioned purpose is the one that occurs the most number of times in the cnf. Choosing this literal to be True or False (appending it as a supposed unit literal) ensures the maximum number of deletions of clauses in the *unit_propagate* functional step.

Thus, we have ensured that the code is optimised.


