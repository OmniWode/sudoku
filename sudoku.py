# generates a valid sudoku puzzle
#
# based on solution on 
# https://www.geeksforgeeks.org/sudoku-backtracking-7/

import random

# makes a blank puzzle
def make_blank():
    row1 = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    row2 = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    row3 = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    row4 = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    row5 = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    row6 = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    row7 = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    row8 = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    row9 = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    
    blank = [row1, row2, row3, row4, row5, row6, row7, row8, row9]

    return blank

# makes a valid sample board for testing
def make_sample():
    row1 = [5, 3, 4, 6, 7, 8, 9, 1, 2]
    row2 = [6, 7, 2, 1, 9, 5, 3, 4, 8]
    row3 = [1, 9, 8, 3, 4, 2, 5, 6, 7]
    row4 = [8, 5, 9, 7, 6, 1, 4, 2, 3]
    row5 = [4, 2, 6, 8, 5, 3, 7, 9, 1]
    row6 = [7, 1, 3, 9, 2, 4, 8, 5, 6]
    row7 = [9, 6, 1, 5, 3, 7, 2, 8, 4]
    row8 = [2, 8, 7, 4, 1, 9, 6, 3, 5]
    row9 = [3, 4, 5, 2, 8, 6, 1, 7, 9]
    
    sample = [row1, row2, row3, row4, row5, row6, row7, row8, row9]
    
    return sample

# makes a clear pattern for testing
def make_test():
    puzzle = make_blank()
    puzzle[1][1] = 1
    puzzle[1][4] = 2
    puzzle[1][7] = 3
    puzzle[4][1] = 4
    puzzle[4][4] = 5
    puzzle[4][7] = 6
    puzzle[7][1] = 7
    puzzle[7][4] = 8
    puzzle[7][7] = 9

    return puzzle

# seeds puzzle with random first row
def random_seed(puzzle):
    for col in range(9):
        options = find_options(puzzle,0,col)
        puzzle[0][col] = random.choice(options)

    return puzzle

# main puzzzle generation loop
def generate_sudoku():
    puzzle = make_blank()
    puzzle = random_seed(puzzle)

    if solve_puzzle(puzzle):
        return puzzle
    else:
        puzzle = make_blank
        print("BLAAAAHHHHHH ERROR")
        return puzzle

# recursive funcution call 
def solve_puzzle(puzzle):
    if complete_puzzle(puzzle):
        return True
    
    next_empty = [0,0]
    next_empty = find_empty(puzzle,next_empty)

    row = next_empty[0]
    col = next_empty[1]

    options = randomizer()

    for num in options:
        if(is_safe(puzzle,row,col,num)):
            puzzle[row][col] = num

            if solve_puzzle(puzzle):
                return True
            
            puzzle[row][col] = 0

    return False

# generates a list of digits in random order to randomize generator
def randomizer():
    digits = [1,2,3,4,5,6,7,8,9]
    options = []
    remain = 9

    while remain > 0:
        n = random.randint(0,remain - 1)

        options.append(digits[n])
        digits.pop(n)
        remain -= 1

    return options
        

# chckes if puzzle is fully filled
def complete_puzzle(puzzle):
    if puzzle[8][8] == 0:
        return False
    else:
        return True
    
# returns a list with the coordinates of the next empty [row,col]
def find_empty(puzzle,list):
    for r in range(0,9):
        for c in range(0,9):
            if puzzle[r][c] == 0:
                list[0] = r
                list[1] = c
                return list
    return list

# returns true if puzzle[row][col] = value is a valid placement
def is_safe(puzzle, row, col, value):
    valid_row = check_row(puzzle,row,value)
    valid_col = check_col(puzzle,col,value)
    valid_group = check_group(puzzle,row,col,value)

    if(valid_row and valid_col and valid_group):
        return True
    else:
        return False

# chooses randomly from list of possible options
def choose_option(options):
    element = random.choice(options)

    return element

# makes list of valid values for a given [row][col] 
# given current state of the puzzle
def find_options(puzzle, row, col):
    options = []

    for digit in range(1,10):
        valid_row = check_row(puzzle, row, digit)
        valid_col = check_col(puzzle, col, digit)
        valid_group = check_group(puzzle, row, col, digit)

        if (valid_row and valid_col and valid_group):
            options.append(digit)

    return options

# checks if given value is already in row
def check_row(puzzle, row, value):
    if value in puzzle[row]:
        valid = False
    else:
        valid = True

    return valid

# checks if given value is already in col
def check_col(puzzle, col, value):
    compare = []
    for row in range(9):
        compare.append(puzzle[row][col])
    
    if value in compare:
        valid = False
    else:
        valid = True

    return valid

# checks if given value is already in group
def check_group(puzzle, row, col, value):
    group = find_group(puzzle, row, col)
    
    if value in group:
            valid = False
    else:
        valid = True
    
    return valid

# creates list of existing values in local 3x3 subgroup
def find_group(puzzle, row, col):
    group = []

    group_r_start = int(row/3) * 3
    group_c_start = int(col/3) * 3

    for r in range(3):
        for c in range(3):
            group.append(puzzle[group_r_start + r][group_c_start + c])

    return group

# prints a given puzzle nicely with group dividers
def print_sudoku(puzzle):      
    for row in range(9):
        for col in range(9):
            if (col != 0 ) and (col%3 == 0):
                print('|', puzzle[row][col], end = ' ')
            else:
                print(puzzle[row][col], end=' ')
        print()
        if (row == 2) or (row == 5):
            print('------|-------|------')
        

# runs the show
def main():
    #puzzle = make_sample()
    #puzzle = make_blank()
    
    puzzle = generate_sudoku()

    print("\n==FINAL PUZZLE STATE==\n")
    print_sudoku(puzzle)


if __name__ == "__main__":
    main()