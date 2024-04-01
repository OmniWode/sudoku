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

# old puzzle generation
'''
def generate_sudoku():
    puzzle = init_puzzle()
    cell_count = 0
    
    ### digit example
    for digit in range(1, 10):
        print(digit)
    print('---------')
    ###

    for row in range(9):
        for col in range(9):
            cell_count += 1
            options = find_options(puzzle, row, col)

            ## DEBUG TIME
            print("\nDEBUG TIME\n")
            print("cell count: ", cell_count)
            print("options for cell[",row,"][",col,"]: ", options,"\n")

            #smarter find_options() should always return list of valid options
            #but still including this check as error handling
            if len(options) > 0:
                element = choose_option(options)
                puzzle[row][col] = element
                ## DEBUG TIME
                print("selected element: ", element)
            else:
                ## DEBUG TIME
                print("!!IMPOSSIBLE GAME!!")
                print("!!THIS IS A BAD FORK - ABORT!!")
                break

            ## DEBUG TIME
            print_sudoku(puzzle)   
            print('\n------------------------------------------------------\n')

        else:
            continue
        break

    return puzzle

'''

# new puzzle generation
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
    
    empty_space = [0,0]
    empty_space = find_empty(puzzle,empty_space)

    row = empty_space[0]
    col = empty_space[1]

    #options = find_options(puzzle,row,col)
    #value = choose_option(options)

    for num in range(1,10):
        if(is_safe(puzzle,row,col,num)):
            puzzle[row][col] = num

            if solve_puzzle(puzzle):
                return True
            
            puzzle[row][col] = 0

    return False

def complete_puzzle(puzzle):
    if puzzle[8][8] == 0:
        return False
    else:
        return True
    
def find_empty(puzzle,list):
    for r in range(0,9):
        for c in range(0,9):
            if puzzle[r][c] == 0:
                list[0] = r
                list[1] = c
                return list
    return list

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
    
    '''
    print("checking group for value: ", value)
    print("existing members of group for [",row,"][",col,"]: ", group)
    print("value ",value," is valid: ",valid,"\n")
    '''

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
    #puzzle = make_test()


    print("\n==FINAL PUZZLE STATE==\n")
    print_sudoku(puzzle)
    #group = find_group(puzzle, 6, 6)
    #print(group)

    


if __name__ == "__main__":
    main()