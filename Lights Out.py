import random
from tkinter import Tk, Button, Label

def flip(x, y, check_board, start):

    # Flips the state of the cell and any immediately adjacent cells if they exist
    check_board[x][y] = not check_board[x][y]
    if x - 1 >= 0:
        check_board[x - 1][y] = not check_board[x - 1][y]
    if x + 1 < len(board):
        check_board[x + 1][y] = not check_board[x + 1][y]
    if y - 1 >= 0:
        check_board[x][y - 1] = not check_board[x][y - 1]
    if y + 1 < len(board):
        check_board[x][y + 1] = not check_board[x][y + 1]

    # If the input is from the player it refreshes the screen immediately and checks if the player has won
    if start:
        refresh()

        # If all the cells are false then the player wins
        if not any(any(row) for row in check_board):
            label.configure(text="YOU WIN\nYAY!!!!!")
    return check_board


def refresh():

    # The takes the values from board and updates any cells that have been changed
    for i in range(len(buttons)):
        for j in range(len(buttons[i])):
            if board[i][j]:                                     # On State
                buttons[i][j].configure(background="#f6dab4")
            else:                                               # Off State
                buttons[i][j].configure(background="#6b3e21")

def solve():

    # Activated when user clicks the solve button
    solution = solve_board()  # Gets the solution array from solveBoard

    # Converts the Array into a String of 1s and 0s
    solution_text = ""
    for i in solution:
        for j in i:
            if j:
                solution_text += "1 "
            else:
                solution_text += "0 "
        solution_text += "\n"

    # Changes the label to the Solution String
    label.configure(text=solution_text)


def hint():
    # Activated when user clicks the solve button
    solution = solve_board()  # Gets the solution array from solveBoard

    # Checks if the board is solved
    done = True
    for i in solution:
        for j in i:
            if j:
                done = False
                break

    # If it is not then it finds a cell to help the user solve the puzzle
    if not done:
        x = random.randint(0, 4)
        y = random.randint(0, 4)
        while not solution[x][y]:
            x = random.randint(0, 4)
            y = random.randint(0, 4)

        # When it finds the cell it displays it on the Label
        label.configure(text="(" + str(y + 1) + ", " + str(x + 1) + ")")


def solve_board():

    # Solves the board
    solution = []       # Stores the Solution Array
    temp_board = []     # Copy of board

    # Algorithm to copy the board array and make the solution array
    for i in board:
        temp_row = []
        temp = []
        for j in i:
            temp_row.append(j)
            temp.append(False)
        temp_board.append(temp_row)
        solution.append(temp)

    # Algorithm to solve the board
    for h in range(2):

        # First Part is run through twice, for the new inputs from the second half of the algorithm
        for i in range(4):
            for j in range(5):
                if temp_board[i][j] == 1:
                    solution[i + 1][j] = not solution[i + 1][j]
                    flip(i + 1, j, temp_board, False)

        # Looks up the cases the 5th row and then grabs the inputs for the associated row (Only run through the first time)
        if h == 0:
            for i in row_five_cases:
                if temp_board[4] == i:
                    for j in i:
                        solution[0][j] = True
                        flip(0, j, temp_board, False)

    # Returns the Solution Array
    return solution


def scramble(start):

    # Picks random cells to flick on to create an initial scramble or reset the board
    for i in range(10):
        x = random.randint(0, 4)
        y = random.randint(0, 4)
        flip(x, y, board, False)
    refresh()

    # Resets the label
    if start:
        label.configure(text="")


# Cases that can occur on the bottom row
row_five_cases = [[False, False, True,  True,  True ],
                  [False, True,  False, True,  False],
                  [False, True,  True,  False, True ],
                  [True,  False, False, False, True ],
                  [True,  False, True,  True,  False],
                  [True,  True,  False, True,  True ],
                  [True,  True,  True,  False, False]]

# Row 1 inputs to solve those cases
row_one_inputs = [[3], [1, 4], [0], [3, 4], [4], [2], [1]]

# Builds the window and titles it
window = Tk()
window.title("Lights Out")

# Two arrays for the data board and the display board
buttons = []
board = [[False, False, False, False, False],
         [False, False, False, False, False],
         [False, False, False, False, False],
         [False, False, False, False, False],
         [False, False, False, False, False]]

# Calls to scramble the board
scramble(False)

# Configures all the grid buttons
for x in range(5):
    temp_button_row = []
    for y in range(5):
        temp_button = Button(window, width=10, height=5, command=lambda i=x, j=y: flip(i, j, board, True))
        temp_button_row.append(temp_button)
        temp_button.grid(row=x, column=y)
    buttons.append(temp_button_row)

# Calls refresh() to make the button colors match the state of the data board
refresh()

# Configures the Solution, Hint, and Reset Buttons and the Label
Button(window, width=10, height=5, text="Solution", command=lambda: solve()).grid(row=0, column=5)
Button(window, width=10, height=5, text="Hint"    , command=lambda: hint()).grid(row=1, column=5)
Button(window, width=10, height=5, text="Reset"   , command=lambda: scramble(True)).grid(row=4, column=5)
label = Label(window, width=10, height=5, foreground="#000000", text="")
label.grid(row=2, column=5)

# Opens the window
window.mainloop()
