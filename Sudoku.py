import sys, traceback

class Sudoku:

    # A box for each 3x3 square in the puzzle
    boxes = ({'rows': [0, 1, 2], 'cols': [0, 1, 2]},
             {'rows': [0, 1, 2], 'cols': [3, 4, 5]},
             {'rows': [0, 1, 2], 'cols': [6, 7, 8]},
             {'rows': [3, 4, 5], 'cols': [0, 1, 2]},
             {'rows': [3, 4, 5], 'cols': [3, 4, 5]},
             {'rows': [3, 4, 5], 'cols': [6, 7, 8]},
             {'rows': [6, 7, 8], 'cols': [0, 1, 2]},
             {'rows': [6, 7, 8], 'cols': [3, 4, 5]},
             {'rows': [6, 7, 8], 'cols': [6, 7, 8]},)

    # A list of cells that can be used to solve the puzzle
    # [ [row, col], ... ]
    cells_to_process = []

    def __init__(self, puzzle):
        self.puzzle = puzzle

        # Numbers 1 through 9
        self.possible = {}
        for num in range(1, 10):
            self.possible[num] = True

        self._init_scratch()

    # Add cell to the list for processing
    def _add_cell_for_processing(self, row, col):
        self.cells_to_process.append([row, col])

    # Initialize a 2D 'scratch' array that contains a dictionary of possible values for each cell
    def _init_scratch(self):
        self.scratch = []

        for row_idx, row_val in enumerate(self.puzzle):
            self.scratch.append([])
            for col_idx, col_val in enumerate(row_val):
                if col_val == 0:
                    self.scratch[row_idx].append(self.possible.copy())
                else:
                    self.scratch[row_idx].append({col_val: True})
                    self._add_cell_for_processing(row_idx, col_idx)

    # The total number of possible values for all the cells combined.
    # When the puzzle is solved it will be 81(9x9).
    def get_scratch_count(self):
        count = 0
        for row in self.scratch:
            for col in row:
                count += len(col)
        return count

    # Display counts of possible values for each cell of the scratch array
    def show_scratch_counts(self):
        for row in self.scratch:
            lengths_in_row = []
            for col in row:
                lengths_in_row.append(len(col))
            print lengths_in_row

    # Display the state of the scratch array
    def show_scratch(self):
        for row in self.scratch:
            row_values = []
            for col in row:
                if len(col) == 1:
                    single = col.keys()
                    row_values.append(single)
                else:
                    row_values.append('*')
            print row_values

    # Return the number value for a cell, or throw an error if there is more than one possible number
    def _get_scratch_cell_number(self, cell):
        scratch_cell_numbers = self.scratch[cell[0]][cell[1]].keys()
        if len(scratch_cell_numbers) == 1:
            return scratch_cell_numbers[0]
        else:
            print "Error: Bad value for cell at row %s, column %s" % (cell[0], cell[1])
            print self.scratch[cell[0]][cell[1]]
            exit()

    #
    def _check_cell(self, row, col):
        if len(self.scratch[row][col]) < 1:
            traceback.print_stack()
            print "Error: Cell empty at row %s, column %s" % (row, col)
            self.show_scratch()
            exit()

        if len(self.scratch[row][col]) == 1:
            self._add_cell_for_processing(row, col)

    # Given the coordinates and number value of a cell,
    # remove that number from the list of possibilities in other cells in the row.
    def _remove_from_row(self, cell, value):
        row_num = cell[0]
        col_num = cell[1]

        for col_idx, col_val in enumerate(self.scratch[row_num]):
            if col_num != col_idx and value in col_val:
                del col_val[value]
                self._check_cell(row_num, col_idx)

    # Given the coordinates and number value of a cell,
    # remove that number from the list of possibilities in other cells in the column.
    def _remove_from_column(self, cell, value):
        row_num = cell[0]
        col_num = cell[1]

        for index in range(0, 9):
            if index != row_num and value in self.scratch[index][col_num]:
                del self.scratch[index][col_num][value]
                self._check_cell(index, col_num)

    def _find_box(self, row, col):
        for box in self.boxes:
            if row in box['rows'] and col in box['cols']:
                return box

    # Given the coordinates and number value of a cell,
    # remove that number from the list of possibilities in other cells in the same box.
    def _remove_from_box(self, cell, value):
        cell_row = cell[0]
        cell_col = cell[1]

        box = self._find_box(cell_row, cell_col)
        for row in box['rows']:
            for col in box['cols']:
                if row != cell_row and col != cell_col:
                    if value in self.scratch[row][col]:
                        del self.scratch[row][col][value]
                        self._check_cell(row, col)

    # Get Uniques: numbers that only occur once in a list
    @staticmethod
    def _find_unique_numbers(row):
        num_count = {}
        for item in row:
                for key in item.keys():
                    if key in num_count:
                        num_count[key] += 1
                    else:
                        num_count[key] = 1

        numbers = []
        for num in num_count:
            if num_count[num] == 1:
                numbers.append(num)
        return numbers

    # Get Non-uniques: numbers that occur more than once in a list
    @staticmethod
    def _find_non_unique_numbers(row):
        num_count = {}
        for item in row:
                for key in item.keys():
                    if key in num_count:
                        num_count[key] += 1
                    else:
                        num_count[key] = 1

        numbers = []
        for num in num_count:
            if num_count[num] > 1:
                numbers.append(num)
        return numbers

    # Unique Rows
    #
    # Set boxes in rows that can have only one possible value
    def _set_unique_numbers_in_row(self, row_idx, unique_numbers):
        for col_idx, value in enumerate(self.scratch[row_idx]):
            for num in unique_numbers:
                if num in value:
                    self.scratch[row_idx][col_idx] = {num: True}
                    self._check_cell(row_idx, col_idx)

    # Update cells that have only one possible number for a row
    def _update_scratch_unique_rows(self):
        for row_idx, row_val in enumerate(self.scratch):
            unique_numbers = self._find_unique_numbers(row_val)
            self._set_unique_numbers_in_row(row_idx, unique_numbers)

    # Unique Cols
    #
    # Set cells in cols that can have only one possible value
    def _set_unique_numbers_in_col(self, col_idx, unique_numbers):
        for row_idx, value in enumerate(self.scratch):
            for num in unique_numbers:
                if num in value:
                    self.scratch[row_idx][col_idx] = {num: True}
                    self._check_cell(row_idx, col_idx)

    # Update cells that have only one possible number for a column
    def _update_scratch_unique_cols(self):
        col_array = []
        for col_idx in range(0, 9):
            col_array.append([])
            for row_idx in range(0, 9):
                col_array[col_idx].append(self.scratch[row_idx][col_idx])

        for col_idx, col in enumerate(col_array):
            unique_numbers = self._find_unique_numbers(col)
            self._set_unique_numbers_in_col(col_idx, unique_numbers)

    # Unique Boxes
    #
    # Set cells in cols that can have only one possible value
    def _set_unique_numbers_in_box(self, box, unique_numbers):
        for row_idx in box['rows']:
            for col_idx in box['cols']:
                for num in unique_numbers:
                    if num in self.scratch[row_idx][col_idx]:
                        self.scratch[row_idx][col_idx] = {num: True}
                        self._check_cell(row_idx, col_idx)

    # Update cells that have only one possible number for a box
    def _update_scratch_unique_boxes(self):
        for box in self.boxes:
            box_array = []

            for row_idx in box['rows']:
                for col_idx in box['cols']:
                    box_array.append(self.scratch[row_idx][col_idx])

            unique_numbers = self._find_unique_numbers(box_array)
            if len(unique_numbers) > 0:
                self._set_unique_numbers_in_box(box, unique_numbers)

    # Box Rows
    #
    def _find_non_unique_box_numbers(self, box):
        numbers = []

        for row_idx in box['rows']:
            for col_idx in box['cols']:
                if len(self.scratch[row_idx][col_idx]) > 1:
                    numbers.append(self.scratch[row_idx][col_idx])

        # A list of all unsolved numbers for a box
        return self._find_non_unique_numbers(numbers)

    # Remove value from the row outside the box
    def _remove_from_row_outside_box(self, row_found, box, number):
        for col in range(0, 9):
            if col not in box['cols'] and number in self.scratch[row_found][col]:
                print "_remove_from_row_outside_box %s: %s, %s" % (number, row_found, col)
                del self.scratch[row_found][col][number]
                self._check_cell(row_found, col)

    # Remove value from the column outside the box
    def _remove_from_col_outside_box(self, col_found, box, number):
        for row in range(0, 9):
            if row not in box['rows'] and number in self.scratch[row][col_found]:
                del self.scratch[row][col_found][number]
                self._check_cell(row, col_found)

    # Find numbers that occur in only one row and scratch that number from the rest of the row
    def _update_scratch_box_rows(self):
        for box in self.boxes:
            # A list of all unsolved numbers for a box
            non_unique_numbers = self._find_non_unique_box_numbers(box)

            # A dictionary keyed by unsolved numbers with a list of row numbers they occur in.
            rows_for_number = {}
            for num in non_unique_numbers:
                rows_for_number[num] = []
                for row_idx in box['rows']:
                    for col_idx in box['cols']:
                        if num in self.scratch[row_idx][col_idx] and row_idx not in rows_for_number[num]:
                            rows_for_number[num].append(row_idx)

            for number in rows_for_number.keys():
                if len(rows_for_number[number]) == 1:
                    self._remove_from_row_outside_box(rows_for_number[number][0], box, number)

    # Find numbers that occur in only one column and scratch that number from the rest of the column
    def _update_scratch_box_cols(self):
        for box in self.boxes:
            # A list of all unsolved numbers for a box
            non_unique_numbers = self._find_non_unique_box_numbers(box)

            # A dictionary keyed by unsolved numbers with a list of columns numbers they occur in.
            cols_for_number = {}
            for num in non_unique_numbers:
                cols_for_number[num] = []

                for col_idx in box['cols']:
                    for row_idx in box['rows']:
                        if num in self.scratch[row_idx][col_idx] and col_idx not in cols_for_number[num]:
                            cols_for_number[num].append(col_idx)

            for number in cols_for_number.keys():
                if len(cols_for_number[number]) == 1:
                    self._remove_from_col_outside_box(cols_for_number[number][0], box, number)

    # Find Pairs
    #
    # Remove number from specific columns inside a box
    def _remove_from_col_inside_box(self, cols_found, box, number):
        print ">>>>>>>>>> _remove_from_col_inside_box:"
        print cols_found
        print box
        print number
        for col in cols_found:
            for row in box['rows']:
                if len(self.scratch[row][col]) > 1 and number in self.scratch[row][col]:
                    print self.scratch[row][col]
                    print "Remove %s, from: %s, %s" % (number, row, col)
                    del self.scratch[row][col][number]
                    self._check_cell(row, col)

    #
    def _remove_other_numbers_from_pair_cells(self, cells, numbers_to_remain):
        for cell in cells:
            row = int(cell[0])
            col = int(cell[1])

            numbers_to_remove = []
            for number in self.scratch[row][col]:
                if number not in numbers_to_remain:
                    numbers_to_remove.append(number)

            for number in numbers_to_remove:
                del self.scratch[row][col][number]
                print "Removed %s from [%s, %s]" % (number, row, col)

    #
    # Find box pairs
    def _find_box_pairs(self):

        # This contains row and column data for each number in each 3x3 square
        # Example:
        # box_numbers[0] = {3: {'rows': ['0', '2'], 'cols': ['0', '2']}}
        #
        box_numbers = []

        for box_idx, box in enumerate(self.boxes):
            box_numbers.append({})
            # A list of all unsolved numbers for a box
            non_unique_numbers = self._find_non_unique_box_numbers(box)

            # A dictionary keyed by unsolved numbers with a list of cells they occur in.
            cells_for_number = {}
            for num in non_unique_numbers:
                cells_for_number[num] = []
                for row_idx in box['rows']:
                    for col_idx in box['cols']:
                        if num in self.scratch[row_idx][col_idx]:
                            cells_for_number[num].append(str(row_idx)+str(col_idx))

            numbers_for_cell = {}
            for number in cells_for_number:
                if len(cells_for_number[number]) == 2:
                    if number not in box_numbers[box_idx]:
                        box_numbers[box_idx][number] = {}

                    cell_1 = cells_for_number[number][0]
                    cell_2 = cells_for_number[number][1]
                    box_numbers[box_idx][number]['rows'] = [int(cell_1[0])]
                    if cell_2[0] not in box_numbers[box_idx][number]['rows']:
                        box_numbers[box_idx][number]['rows'].append(int(cell_2[0]))

                    box_numbers[box_idx][number]['cols'] = [int(cell_1[1])]
                    if cell_2[1] not in box_numbers[box_idx][number]['cols']:
                        box_numbers[box_idx][number]['cols'].append(int(cell_2[1]))

                    pair_key = cell_1 + cell_2
                    if pair_key in numbers_for_cell:
                        numbers_for_cell[pair_key].append(number)
                    else:
                        numbers_for_cell[pair_key] = [number]

            # Find naked pairs for a box
            for cells in numbers_for_cell:
                if len(numbers_for_cell[cells]) == 2:
                    cell_array = [[cells[0], cells[1]], [cells[2], cells[3]]]
                    self._remove_other_numbers_from_pair_cells(cell_array, numbers_for_cell[cells])

        # Find matching column pairs across each column of squares
        for column in [0, 1, 2]:
            square_a = column
            square_b = square_a + 3
            square_c = square_b + 3
            for number in box_numbers[square_a]:
                if number in box_numbers[square_b] and cmp(box_numbers[square_a][number]['cols'], box_numbers[square_b][number]['cols']) == 0:
                    # remove number from columns in square_c
                    #pass
                    self._remove_from_col_inside_box(box_numbers[square_a][number]['cols'], self.boxes[square_c], number)
                elif number in box_numbers[square_c] and cmp(box_numbers[square_a][number]['cols'], box_numbers[square_c][number]['cols']) == 0:
                    # remove number from columns in square_b
                    pass
                    #self._remove_from_col_inside_box(box_numbers[square_a][number]['cols'], self.boxes[square_b], number)

            for number in box_numbers[square_b]:
                if number in box_numbers[square_c] and cmp(box_numbers[square_b][number]['cols'], box_numbers[square_c][number]['cols']) == 0:
                    # remove number from columns in square_a
                    #pass
                    self._remove_from_col_inside_box(box_numbers[square_b][number]['cols'], self.boxes[square_a], number)

    #
    def _find_pairs(self):
        self._find_box_pairs()

    #
    def _process_cell(self, cell):
        cell_value = self._get_scratch_cell_number(cell)
        self._remove_from_row(cell, cell_value)
        self._remove_from_column(cell, cell_value)
        self._remove_from_box(cell, cell_value)

    #
    def _process_ready_cells(self):
        while len(self.cells_to_process) > 0:
            cell = self.cells_to_process.pop(0)
            self._process_cell(cell)

    # Iterate over the cells ready for processing and update the scratch array
    def solve_puzzle(self):
        last_count = self.get_scratch_count()
        print "count: %s" % last_count
        while last_count > 81:
            self._process_ready_cells()

            if len(self.cells_to_process) < 1:
                self._update_scratch_unique_rows()
                self._update_scratch_unique_cols()
                self._update_scratch_unique_boxes()
                self._update_scratch_box_rows()
                self._update_scratch_box_cols()
                self._find_pairs()

            current_count = self.get_scratch_count()
            print "count: %s" % current_count
            if last_count == current_count:
                print "Not solved"
                break
            else:
                last_count = current_count
