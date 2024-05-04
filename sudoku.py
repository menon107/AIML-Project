import random
import tkinter as tk
from tkinter import messagebox

def generate_sudoku():
    grid = [[0 for _ in range(9)] for _ in range(9)]
    solve_sudoku(grid)
    remove_cells(grid, 40) 
    return grid

def solve_sudoku(grid):
    row, col = find_empty_cell(grid)
    if row == -1:
        return True
    for num in range(1, 10):
        if is_valid(grid, row, col, num):
            grid[row][col] = num
            if solve_sudoku(grid):
                return True
            grid[row][col] = 0
    return False

def find_empty_cell(grid):
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                return row, col
    return -1, -1

def is_valid(grid, row, col, num):
    return (
        is_valid_row(grid, row, num) and
        is_valid_col(grid, col, num) and
        is_valid_box(grid, row - row % 3, col - col % 3, num)
    )

def is_valid_row(grid, row, num):
    return num not in grid[row]

def is_valid_col(grid, col, num):
    return num not in [grid[row][col] for row in range(9)]

def is_valid_box(grid, start_row, start_col, num):
    return num not in [
        grid[row][col]
        for row in range(start_row, start_row + 3)
        for col in range(start_col, start_col + 3)
    ]

def remove_cells(grid, num_cells):
    cells = [(row, col) for row in range(9) for col in range(9)]
    random.shuffle(cells)
    for cell in cells[:num_cells]:
        grid[cell[0]][cell[1]] = 0

def generate_new_sudoku():
    global grid
    grid = generate_sudoku()
    update_gui(grid)

def update_gui(grid):
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                entries[i][j].delete(0, tk.END)
                entries[i][j].insert(0, grid[i][j])
                entries[i][j].config(state="disabled")
            else:
                entries[i][j].delete(0, tk.END)
                entries[i][j].config(state="normal")

def check_solution():
    user_solution = [[int(entries[i][j].get()) if entries[i][j].get() else 0 for j in range(9)] for i in range(9)]
    solved_grid = [[grid[i][j] for j in range(9)] for i in range(9)]  
    if solve_sudoku(solved_grid) and user_solution == solved_grid:
        messagebox.showinfo("Result", "Congratulations! Sudoku solved correctly.")
    else:
        messagebox.showerror("Result", "Oops! Sudoku not solved correctly.")

def show_solution():
    solved_grid = [[grid[i][j] for j in range(9)] for i in range(9)]
    solve_sudoku(solved_grid)
    for i in range(9):
        for j in range(9):
            entries[i][j].delete(0, tk.END)
            entries[i][j].insert(0, solved_grid[i][j])
            entries[i][j].config(state="disabled")



root = tk.Tk()
root.title("Sudoku Solver")


entries = [[None for _ in range(9)] for _ in range(9)]
for i in range(9):
    for j in range(9):
        entries[i][j] = tk.Entry(root, width=2, font=('Arial', 20), justify="center")
        entries[i][j].grid(row=i, column=j)


generate_new_sudoku()


new_button = tk.Button(root, text="New Sudoku", command=generate_new_sudoku)
new_button.grid(row=9, columnspan=3)


check_button = tk.Button(root, text="Check Solution", command=check_solution)
check_button.grid(row=9, column=3, columnspan=3)


show_solution_button = tk.Button(root, text="Show Solution", command=show_solution)
show_solution_button.grid(row=9, column=6, columnspan=3)


root.mainloop()
