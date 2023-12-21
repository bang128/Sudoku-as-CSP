# Sudoku-as-CSP
## Objective
Develop an AI program to solve 9x9 Sudoku as CSP, using backtracking, forward checking and MRV
## Method
- Programmed in Python; read initial sudoku from file input
- Utilized forward checking to assign value to blank cells and remove the value from other cells’ list of possible values; orderly chose a cell to assign by MRV
- Utilized backtracking to re-assign blank cells if the assigned values are incorrect
