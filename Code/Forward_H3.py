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
import Code.Forward_H2 as h2
from sklearn.preprocessing import normalize
DEBUG = False
counter = 0
checked_set = []
testing_file_name = 'puzzle_sample/sample.txt'

def normalize(v):
    norm=np.linalg.norm(v, ord=1)
    if norm==0:
        norm=np.finfo(v.dtype).eps
    return v/norm


def solvePuzzleH3(puzzle):
    global counter, checked_set
    counter = 0
    checked_set = []

    if solvePuzzleUtil_H3(puzzle,np.copy(puzzle.probability_arr)):
        puzzle.print_puzzle()
        print("puzzle solved. \ntotal steps: {}".format(counter))
        return True
    else:
        print("solution doesn't exist")
        return False



def solvePuzzleUtil_H3(puzzle_rec,probability_arr):
    global counter,checked_set
    if puzzle_rec.isFinished():
        return True

    fc.update_constraint(puzzle_rec, probability_arr)
    # fc.print_probability_arr(probability_arr)
    # print('/**********************************/')
    possible_cell = np.where(probability_arr >= 0)
    light_off_bulbs = np.where(puzzle_rec.arr == puzzle_rec.LIGHT_OFF)
    possible_cell_set = set(zip(possible_cell[0], possible_cell[1])).intersection(set(zip(light_off_bulbs[0], light_off_bulbs[1])))

    light_bulbs = np.where(puzzle_rec.arr == puzzle_rec.LIGHT_BULB)
    light_bulbs_set = set(zip(light_bulbs[0], light_bulbs[1]))

    edge_num_arr = h2.count_edge(puzzle_rec)

    normalized_v = edge_num_arr / np.sqrt(np.sum(edge_num_arr**2))

    possible_cell_set = sorted(possible_cell_set, key=lambda cell: probability_arr[cell[0], cell[1]]+normalized_v[cell[0], cell[1]]/100, reverse=True)

    if len(possible_cell[0]) > 0:
        for row, col in possible_cell_set:
            counter += 1
            if puzzle_rec.isValidBulb(row, col) and puzzle_rec.isWallNeigbourValid(row, col) and light_bulbs_set.union({(row,col)}) not in checked_set:
                puzzle_rec.insert_light_bulb(row, col)

                next_probability_arr = np.copy(probability_arr)
                fc.check_cell_lightup_constraint(puzzle_rec, next_probability_arr, row, col)
                next_probability_arr[row, col] = -1
                if DEBUG:
                    puzzle_rec.print_puzzle()
                    print("****************")
                    # fc.print_probability_arr(probability_arr)

                if solvePuzzleUtil_H3(puzzle_rec, next_probability_arr):
                    return True
                else:
                    puzzle_rec.removeLightBulb(row, col)
                    if DEBUG:
                        puzzle_rec.print_puzzle()
                        # fc.print_probability_arr(probability_arr)
                        print("****************")
                    checked_set.append(light_bulbs_set)
    return False

if __name__ == '__main__':
    f = game.read_puzzle_file(fileName=testing_file_name)
    puzzle = game.get_next_puzzle(f, isForward=True)

    while puzzle is not None:
        # puzzle.print_solution()
        solvePuzzleH3(puzzle)
        puzzle = game.get_next_puzzle(f, isForward=True)
