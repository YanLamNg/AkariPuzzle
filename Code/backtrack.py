# COMP 4190
# Authors:
#   Xiaojian Xie 7821950
# 	YanLam Ng 7775665
# Group: 9

import os
import sys
sys.path.append(os.getcwd())

import Code.Game as game
import numpy as np
import sys

counter = 0
testing_file_name = 'puzzle_sample/sample.txt'


def solvePuzzle(puzzle):
    notAssigned = np.where(puzzle.arr == puzzle.LIGHT_OFF)
    notAssigned_list = list(zip(notAssigned[0], notAssigned[1]))

    domain = (puzzle.LIGHT_OFF, puzzle.LIGHT_BULB)
    result = solvePuzzleUtil(puzzle, notAssigned_list, domain)
    if result:
        print("**************")
        puzzle.print_puzzle()
        print("puzzle solved. \ntotal number of nodes visited: {}".format(counter))
        return True
    else:
        print("solution doesn't exist")
        return False

def solvePuzzleUtil(puzzle_rec, notAssigned_list, domain):
    global counter
    if puzzle_rec.isFinished():
        return True

    if len(notAssigned_list) == 0:
        return False

    cell = notAssigned_list[0]
    row = cell[0]
    col = cell[1]

    notAssigned_list.remove(cell)

    for i in domain:
        counter += 1
        if i == puzzle_rec.LIGHT_BULB:
            if checkValid(puzzle_rec, row, col):
                puzzle_rec.insert_light_bulb(row, col)
                if solvePuzzleUtil(puzzle_rec, notAssigned_list, domain):
                    return True
                else:
                    puzzle_rec.removeLightBulb(row, col)

        elif i == puzzle_rec.LIGHT_OFF:
            if solvePuzzleUtil(puzzle_rec, notAssigned_list, domain):
                return True

    notAssigned_list.insert(0, cell)

    return False

def checkValid(puzzle_rec, row, col):
    return puzzle_rec.isValidBulb(row, col) and puzzle_rec.isWallNeigbourValid(row, col)


if __name__ == '__main__':
    f = game.read_puzzle_file(fileName=testing_file_name)
    puzzle = game.get_next_puzzle(f, isForward=True)

    while puzzle is not None:
        solvePuzzle(puzzle)
        puzzle = game.get_next_puzzle(f, isForward=True)
