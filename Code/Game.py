# COMP 4190
# Authors:
#   Xiaojian Xie 7821950
# 	YanLam Ng 7775665
# Group: 9


from Code.AkariPuzzle import AkariPuzzle
import numpy as np
from termcolor import colored
SHOW_SOLUTION = False
Puzzle_File_Name = "puzzle_sample/sample.txt"

def read_puzzle_file(fileName=Puzzle_File_Name):
    print('Reading sample')
    f = open(fileName, "r")
    return f


def get_next_puzzle(f, isForward=False):
    puzzle = None
    rows, cols = 0, 0
    if f is not None:
        line = f.readline()
        while len(line.strip()) == 0 or line[0] == '#':
            if len(line.strip()) == 0:
                return None
            else:
                line = f.readline()

        rows, cols = (int(s) for s in line.split())
        puzzle = np.zeros((rows, cols), dtype=np.int8)

        for i in range(rows):
            cells = f.readline()
            for j in range(cols):
                if cells[j] is '_':
                    puzzle[i, j] = AkariPuzzle.LIGHT_OFF
                else:
                    puzzle[i, j] = int(cells[j])

#read solution
        line = f.readline()
        solution = np.zeros((rows, cols), dtype=np.int8)
        i = 0
        j = 0
        is_solution_line = False
        while (len(line) == 0 or line[0] == '#' ) and i < rows:
            if len(line.strip()) == 0:
                break

            for ch in line:
                if ch is '_':
                    solution[i, j] = AkariPuzzle.LIGHT_OFF
                    is_solution_line = True
                    j += 1
                elif ch is 'b':
                    solution[i, j] = AkariPuzzle.LIGHT_BULB
                    is_solution_line = True
                    j +=1
                elif ch.isdigit():
                    solution[i, j] = int(ch)
                    is_solution_line = True
                    j +=1

            if is_solution_line:
                i+=1
            line = f.readline()
            j=0
    return AkariPuzzle(rows, cols, puzzle, solution=solution, isForward=isForward)



if __name__ == '__main__':
    f = read_puzzle_file()

    puzzle = get_next_puzzle(f)
    while not puzzle.isFinished():
        puzzle.print_puzzle()
        mode = int(input('\nSelect mode:\n0 ==> insert light bulb\n1 ==> delete light bulb\n'))
        if mode == 0:
            row = int(input('Enter the row of light bulb: '))
            col = int(input('Enter the col of light bulb: '))
            if not puzzle.insert_light_bulb(row, col):
                print('fail to insert')
        elif mode == 1:
            row = int(input('Enter the row of light bulb: '))
            col = int(input('Enter the col of light bulb: '))
            if not puzzle.removeLightBulb(row, col):
                print('fail to remove')
        print('/********************/\n')

    f.close()
    print('done')
