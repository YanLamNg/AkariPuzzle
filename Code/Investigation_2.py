# COMP 4190
# Authors:
#   Xiaojian Xie 7821950
# 	YanLam Ng 7775665
# Group: 9
import os
import sys
sys.path.append(os.getcwd())
import Code.Game as game
import multiprocessing as mp
from Code.AkariPuzzle import AkariPuzzle as ap
import Code.ForwardChecking as fc
import Code.Forward_H1 as fc_H1
import Code.Forward_H2 as fc_H2
import Code.Forward_H3 as fc_H3
import Code.backtrack_H2 as bt_H2
import numpy as np
from termcolor import colored
import Code.ForwardChecking  as fc
import Code.backtrack as bt
import copy
import time

DEBUG = False
counter = 0
checked_set = []
testing_file_name = 'puzzle_sample/lightup puzzles.txt'

track_methods = {
    'fc.solvePuzzle': fc.solvePuzzle,
    'fc_H1.solvePuzzle': fc_H1.solvePuzzleH1,
    'fc_H2.solvePuzzle': fc_H2.solvePuzzleH2,
    'fc_H3.solvePuzzle': fc_H3.solvePuzzleH3,
    'backtrack.solvePuzzle': bt.solvePuzzle,
    'backtrack_H2.solvePuzzle': bt_H2.solvePuzzleH2
}

file_names = [
    'puzzle_sample/12x12_48W.txt',
    'puzzle_sample/12x12_24W.txt',
    'puzzle_sample/12x12_12W.txt'
]

if __name__ == '__main__':
    for fileName in file_names:
        f = game.read_puzzle_file(fileName=fileName)
        puzzle = game.get_next_puzzle(f, isForward=True)

        while puzzle is not None:
            for method in track_methods:
                print('\n/*********************')
                print(method)
                print('*********************/')
                proc = mp.Process(target=track_methods[method], args=(copy.deepcopy(puzzle),))

                proc.start()
                start_time = time.time()
                proc.join(timeout=600)
                exec_time = time.time() - start_time
                print("execution time: " + str(exec_time))
                if proc.is_alive():
                    print('timeout')
                proc.terminate()
            puzzle = game.get_next_puzzle(f, isForward=True)



