__Prompt 1__: <p> Write a k-sudoku puzzle pair solver and generator by encoding the problem to propositional logic and solving it via a SAT solver. Given a sudoku puzzle pair **S1, S2** (both of dimension k) as input, your job is to write a program to fill the empty cells of both sudokus such that it satisfies the following constraints, <br/> Individual sudoku properties should hold. <br/> For each empty cell **S1[i, j] ≠ S2[i, j]**, where i is row and j is column.
</p>

**Input** : Parameter **k**, single CSV file containing two sudokus. The first **kxk** rows are for the first sudoku and the rest are for the second sudoku. Each row has **kxk** cells. Each cell contains a number from **1** to **kxk**. Cell with **0** specifies an empty cell. <br>
**Output**: If the sudoku puzzle pair doesn't have any solution, you should return None otherwise return the filled sudoku pair. <br/> <br/>

***Solution*** <br/>
The source code is 'Unique_Sudoku_Pair_Generator.py' <br/>
The test cases are provided in the folder 'tests'. The parameter k should be given as input to the terminal by the tester themselves as mentioned. <br/> 
There are 5 test cases, for k = 2,3,4,5,6
<br/><br/>
The csv test file for different values of k are named as sudoku_with_dimensions_k.csv. For example, the csv file input for k=2 is named as sudoku_with_dimensions_2.csv
<br/>
The expected outputs of each test case are sudoku_with_dimensions_k_output.csv <br/> <br/>

__Prompt 2__: <p>You have to write a k-sudoku puzzle pair generator. The puzzle pair must be maximal (have the largest number of holes possible) and must have a unique solution. <br/>
**Input**: Parameter **k** <br/>
**Output**: CSV file containing two sudokus in the format mentioned above. </p>
<br/>
***Solution*** <br/>
The source code is 'Unique_Sudoku_Pair_with_Maximal_Holes.py' <br/>
The parameter k should be given as input to the terminal by the tester themselves as mentioned. <br/>
The output (maximal sudoku pair) will be written to Q2_output.csv file
