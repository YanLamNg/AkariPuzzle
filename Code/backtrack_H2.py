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

counter = 0
testing_file_name = 'puzzle_sample/sample.txt'


def solvePuzzleH2(puzzle):
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

    cell = findConstraining(puzzle_rec, notAssigned_list)
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

    notAssigned_list.append(cell)

    return False

def checkValid(puzzle_rec, row, col):
    return puzzle_rec.isValidBulb(row, col) and puzzle_rec.isWallNeigbourValid(row, col)

# count number of squares light up by the bulb
def countLightUp(puzzle, row, col):
    count = 0
    for x, y in puzzle.LIGHT_DIRECTION:
        col_temp, row_temp = col + x, row + y
        while puzzle.isInBounds(row_temp, col_temp):
            if puzzle.isLightBulb(row_temp, col_temp):
                break
            elif puzzle.isWall(row_temp, col_temp):
                break
            elif puzzle.arr[row_temp, col_temp] != puzzle.LIGHT_ON:
                count += 1
            col_temp, row_temp = col_temp + x, row_temp + y
    return count


def findConstraining(puzzle, notAssigned_list):
    if len(notAssigned_list) == 0:
        return []
    winner = []
    max_count = 0
    for row, col in notAssigned_list:
        count = countLightUp(puzzle, row, col)
        if count >= max_count:
            winner = tuple([row, col])
            max_count = count

    return winner

if __name__ == '__main__':
    f = game.read_puzzle_file(fileName=testing_file_name)
    puzzle = game.get_next_puzzle(f, isForward=True)

    while puzzle is not None:
        solvePuzzleH2(puzzle)
        puzzle = game.get_next_puzzle(f, isForward=True)





