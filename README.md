# Artificial Intelligence_A1

COMP 4190
Artificial Intelligenc
Assignment 1

Authors:

Xiaojian Xie 7821950

YanLam Ng 7775665

Group: 9

To run the program simply run the python code either for ForwardChecking.py or backtracking.py. 
If you want to test with heuristic, run the code which the file name format is <algorithm_Hn>. 

Environment:

The running environment using anaconda version (conda 4.7.12) and python 3.7. The python packages included  'numpy', 'termcolor' and 'multiprocessing' were installed by pip 

How to run in terminal:

1.go the the project directory "comp4190a1" 

2.run 'python Code\\{filename}'

File we could run: backtrack.py, backtrack_H2.py, ForwardChecking.py, Forward_H1.py, Forward_H2.py, Forward_H3.py, Investigation_1.py, Investigation_2.py

To running other sample file, change the "testing_file_name" variable to the file path

Backtracking: In this puzzle, the domain for each cell is no bulb and bulb, so the possible move is placing the bulb or
leaving blank. While one of the moves is legal, the algorithm would process recursively until the solution is found. 
Otherwise, do backtrack and keep going.

Backtracking_H1: H1 is Most Constrained Heuristic. Since backtrack algorithm does not track the domain for each cell, 
this heuristic is not available.

Backtracking_H2: This algorithm applies Most Constraining Heuristic. It places the light bulb to the cell that will 
impact the most unassigned cells. The priority is calculated by checking how many cells 
each bulb could light up. 

Backtracking_H3: Since H1 is not available, H3 (combination of H1 and H2) is the same as H2. 

Forward Checking: In this algorithm, We check all constraint satisfaction. we would insert a light bulb that is valid constraint. We will backtrack if no valid light bulb can be inserted

Forward Checking H1: It is Most constrained heuristic. We created a array that store the probability of the bulb where can be inserted. we assign -1 for invalid light bulb position, 1 is comfirm location and 0 is uncertain. We evenly give the probability base on the number of bulb around the wall and the wall constraint. Then, we choose the largest probability of the bulb.   

Forward Checking H2: In the most constraining heuristic, we places the light bulb to the cell that will impact the most unassigned cells. The priority is calculated by checking how many cells 
each bulb could light up. 

Forward Checking H3: H3 is on H1. If the priority of the light bulbs are same(the probability is same), the light bulb would be chosen by H2. 

Python File:

Game.py is for reading the sample file. When reading the file, make sure the sample solution is commented by '#' and no empty line between each line.

AkariPuzzle.py is for the puzzle game structure.

