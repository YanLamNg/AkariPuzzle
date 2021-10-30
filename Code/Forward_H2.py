# COMP 4190
# Authors:
#   Xiaojian Xie 7821950
# 	YanLam Ng 7775665
# Group: 9
import os
import sys
sys.path.append(os.getcwd())

import Code.Game as game
from Code.AkariPuzzle import AkariPuzzle as ap
import numpy as np
from termcolor import colored
import Code.ForwardChecking  as fc

DEBUG = False
counter = 0
checked_set = []
testing_file_name = 'puzzle_sample/sample.txt'

def solvePuzzleH2(puzzle):
    global counter, checked_set
    counter = 0
    checked_set = []
    if solvePuzzleUtil_H2(puzzle,np.copy(puzzle.probability_arr)):
        puzzle.print_puzzle()
        print("puzzle solved. \ntotal steps: {}".format(counter))
        return True
    else:
        print("solution doesn't exist")
        return False

def count_edge(puzzle):
    edge_counter = np.zeros((puzzle.rows, puzzle.cols), dtype=np.float64)
    light_off = np.where(puzzle.arr == puzzle.LIGHT_OFF)

    for row,col in zip(light_off[0], light_off[1]):
        if puzzle.isInBounds(row, col) and puzzle.arr[row, col] == ap.LIGHT_OFF:
            edge_counter[row, col]+=1
            for x, y in ap.LIGHT_DIRECTION:
                col_temp, row_temp = col + x, row + y
                while puzzle.isInBounds(row_temp, col_temp):
                    if puzzle.isWall(row_temp, col_temp) or puzzle.isLightBulb(row_temp, col_temp):
                        break
                    elif puzzle.arr[row, col] == ap.LIGHT_OFF:
                        edge_counter[row, col] += 1
                    col_temp, row_temp = col_temp + x, row_temp + y
    return edge_counter

def solvePuzzleUtil_H2(puzzle_rec,probability_arr):
    global counter,checked_set
    if puzzle_rec.isFinished():
        return True

    fc.update_constraint(puzzle_rec, probability_arr)


    edge_num_arr = count_edge(puzzle_rec)
    light_off_edge = np.where(edge_num_arr > 0)

    light_off_edge_set = set(zip(light_off_edge[0], light_off_edge[1]))
    if DEBUG: print(edge_num_arr)
    possible_cell_set = sorted(light_off_edge_set, key=lambda cell: edge_num_arr[cell[0], cell[1]], reverse=False)
    light_bulbs = np.where(puzzle_rec.arr == puzzle_rec.LIGHT_BULB)

    light_bulbs_set = set(zip(light_bulbs[0], light_bulbs[1]))
    if len(light_off_edge_set) > 0:
        for row, col in possible_cell_set:
            counter += 1
            if puzzle_rec.isValidBulb(row, col) and puzzle_rec.isWallNeigbourValid(row, col) and light_bulbs_set.union(
                    {(row, col)}) not in checked_set:
                puzzle_rec.insert_light_bulb(row, col)

                next_probability_arr = np.copy(probability_arr)
                fc.check_cell_lightup_constraint(puzzle_rec, next_probability_arr, row, col)
                next_probability_arr[row, col] = -1
                if DEBUG:
                    puzzle_rec.print_puzzle()
                    print("****************")
                    fc.print_probability_arr(next_probability_arr)

                if solvePuzzleUtil_H2(puzzle_rec, next_probability_arr):
                    return True
                else:
                    puzzle_rec.removeLightBulb(row, col)
                    checked_set.append(light_bulbs_set)
                    if DEBUG:
                        puzzle_rec.print_puzzle()
                        fc.print_probability_arr(probability_arr)
                        print("****************")

    return False

if __name__ == '__main__':
    f = game.read_puzzle_file(fileName=testing_file_name)
    puzzle = game.get_next_puzzle(f, isForward=True)

    while puzzle is not None:
        # puzzle.print_solution()
        solvePuzzleH2(puzzle)
        # print_constraited_puzzle(puzzle)
        puzzle = game.get_next_puzzle(f, isForward=True)
    # LightOffCell = np.where(puzzle.arr in range(5))


