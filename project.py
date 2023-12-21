from collections import OrderedDict
import copy

# Assume that the input file always contains a valid initial sudoku board with 9 rows and 9 columns.
# Valid initial sudoku board means that there are only numbers 0-9 in the board
# 0: blank cell
# 1-9: cell which is initially numbered without repeating the number in any related cells
#      (in a vertical/horizontal line or a 3x3 grid).
FILE_NAME = "sudoku4.txt"
POSSIBLE_VALUES = {}
RELATED_CELLS = {}
SUDOKU = []


# Return a list of all cells related to the cell at (row, col)
def find_related_cells(row, col):
    related_cells = []

    # In the same horizontal line
    for i in range(9):
        if i != col:
            related_cells.append((row, i))

    # In the same vertical line
    for i in range(9):
        if i != row:
            related_cells.append((i, col))

    # In 3x3 grid
    if row in [0, 3, 6]:
        related_rows = [row + 1, row + 2]
    elif row in [1, 4, 7]:
        related_rows = [row - 1, row + 1]
    else:
        related_rows = [row - 1, row - 2]

    if col in [0, 3, 6]:
        related_cols = [col + 1, col + 2]
    elif col in [1, 4, 7]:
        related_cols = [col - 1, col + 1]
    else:
        related_cols = [col - 1, col - 2]

    for i in range(2):
        for j in range(2):
            related_cells.append((related_rows[i], related_cols[j]))

    return related_cells


# Initially find all possible values for each blank cell and add to POSSIBLE_VALUES
def find_possible_values(sudoku):
    for k in RELATED_CELLS:
        if sudoku[k[0]][k[1]] == 0:
            values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            for cells in RELATED_CELLS[k]:
                x = sudoku[cells[0]][cells[1]]
                if x in values:
                    values.remove(x)
            POSSIBLE_VALUES.update({k: values})


# Update the the list of possible values of current_cell while doing forward_checking
def update_possible_values(value, current_cell, possible_values):
    related_cells = RELATED_CELLS[current_cell]
    keys = possible_values.keys()

    for cell in related_cells:
        if cell in keys:
            if value in possible_values[cell]:
                possible_values[cell].remove(value)
    return possible_values


# Check whether there is any cell that runs out of possible values
def still_possible(possible_values):
    for i in possible_values.keys():
        if not possible_values[i]:
            return False
    return True


# Check if the entire sudoku has been solved
def is_solved(sudoku):
    for r in range(9):
        for c in range(9):
            if sudoku[r][c] == 0:
                return False
    return True


# Recursively solve sudoku, using backtracking, forward-checking and MRV
def play_game(sudoku, possible_values, current_cell):
    # Try the each possible values at current_cell
    for i in possible_values[current_cell]:
        r = current_cell[0]
        c = current_cell[1]

        # Assign value to current_cell in sudoku
        sudoku[r][c] = i

        # Copy possible_values into temp not to change the dictionary before ensuring that the assigned value is correct
        temp = update_possible_values(i, current_cell, copy.deepcopy(possible_values))

        # MRV: Sort the dictionary by length of values (the number of possible values at each blank cell)
        temp = dict(OrderedDict(sorted(temp.items(), key=lambda x: len(x[1]))))

        # Check whether the sudoku is still possible to solve
        if still_possible(temp):
            # When current_cell is assigned, remove it from list of blank cells and continue to other blank cells
            del temp[current_cell]

            # If all cell has been assigned
            if not list(temp.keys()):
                if is_solved(sudoku):
                    return True
                else:
                    return False

            # Recursively solve sudoku at the first cell in the dictionary (the cell with MRV)
            if play_game(sudoku, temp, list(temp.keys())[0]):
                return True

            # If the value assigned to current_cell is incorrect, assign current_cell with 0 (return to blank cell)
            sudoku[r][c] = 0

    # Return False if none of possible values at current_cell is correct -> need to backtrack
    return False


# Display the sudoku board
def display(sudoku):
    for r in range(9):
        for c in range(9):
            print(sudoku[r][c], ' ', end='')
            if c in [2, 5]:
                print('| ', end='')
            if c == 8:
                print()
        if r in [2, 5]:
            print('------------------------------')


def main():
    file = open(FILE_NAME, 'r')
    lines = file.readlines()
    for r in range(9):
        row = lines[r].split()
        for c in range(9):
            row[c] = int(row[c])
        SUDOKU.append(row)

    print("Initial:")
    display(SUDOKU)

    for r in range(9):
        for c in range(9):
            if SUDOKU[r][c] == 0:
                RELATED_CELLS.update({(r, c): find_related_cells(r, c)})

    find_possible_values(SUDOKU)
    possible_values = dict(OrderedDict(sorted(POSSIBLE_VALUES.items(), key=lambda x: len(x[1]))))
    play_game(SUDOKU, possible_values, list(possible_values.keys())[0])

    print()
    print("Solved:")
    display(SUDOKU)


if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
