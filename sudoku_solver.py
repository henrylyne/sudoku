#!/usr/bin/python
import sys
import json
from Sudoku import Sudoku

# Default dir and puzzle
puzzle_dir = "samples/"
puzzle_name = "34"

# If puzzle number passed in, get the puzzle number to solve
if len(sys.argv) == 2:
    puzzle_name = sys.argv[1]

puzzle_json_file = puzzle_dir + puzzle_name + '.json'
print puzzle_json_file

puzzle = []
try:
    # Open the input file and read the json data.
    with open(puzzle_json_file) as json_data:
        puzzle = json.load(json_data)

except ValueError, msg:
    print "Invalid JSON: %s" % msg


''' First let's create a sudoku puzzle to solve:

 -------------
 |*73|95*|**8|
 |***|*1*|***|
 |*6*|8**|*7*|
 -------------
 |***|*8*|**3|
 |3**|4*5|**9|
 |9**|*3*|***|
 -------------
 |*4*|**6|*8*|
 |***|*4*|***|
 |6**|*91|25*|
 -------------

 This will initially be represented as a 2D array, with 0 for spaces.

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
