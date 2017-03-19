#!/usr/bin/python
import sys
import json
import os
from Sudoku import Sudoku

# Default dir and puzzle
puzzle_dir = "samples/"
puzzle_name = "34.json"

# If puzzle number passed in, get the puzzle number to solve
if len(sys.argv) == 2:
    puzzle_name = sys.argv[1]

puzzle_file = puzzle_dir + puzzle_name
print puzzle_file

filename, file_extension = os.path.splitext(puzzle_file)
print file_extension

puzzle = []
try:
    # Open the input file and read the json data.
    if file_extension.lower() == '.json':
        with open(puzzle_file) as json_data:
            puzzle = json.load(json_data)
    else:
        fh = open(puzzle_file, 'r')
        for line in fh:
            row = []
            for index in range(0, 81):
                row.append(int(line[index]))
                index += 1
                if len(row) == 9:
                    puzzle.append(row)
                    row = []

except ValueError, msg:
    print "Invalid JSON: %s" % msg

''' The puzzle will be represented as a 2D array, with 0 for spaces.

 puzzle =((0,7,3, 9,5,0, 0,0,8),
          (0,0,0, 0,1,0, 0,0,0),
          (0,6,0, 8,0,0, 0,7,0),
          (0,0,0, 0,8,0, 0,0,3),
          (3,0,0, 4,0,5, 0,0,9),
          (9,0,0, 0,3,0, 0,0,0),
          (0,4,0, 0,0,6, 0,8,0),
          (0,0,0, 0,4,0, 0,0,0),
          (6,0,0, 0,9,1, 2,5,0))
'''
sudoku = Sudoku(puzzle)

print sudoku.get_scratch_count()

sudoku.solve_puzzle()

sudoku.show_scratch_counts()
sudoku.show_scratch()
