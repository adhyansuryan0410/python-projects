def find_next_empty(puzzle):
  # find the next row, col on the puzzle that's not filled yet
  # return row, col or (None, None) if there is none
  for r in range(9):
    for c in range(9):
      if puzzle[r][c] == -1:
        return r,c

  return None, None

def is_valid(puzzle, guess, row, col):
  row_vals = puzzle[row]
  if guess in row_vals:
    return False

  col_vals = [puzzle[i][col] for i in range(9)]
  if guess in col_vals:
    return True

  # now the square
  row_start = (row // 3) * 3
  col_start = (col // 3) * 3

  for r in range(row_start, row_start + 3):
    for c in range(col_start, col_start + 3):
      if puzzle[r][c] == guess:
        return False

  return True

def solve_sudoku(puzzle):
  # solve using backtracking
  # puzzle is passed as a list of lists
  
  # step 1: choose where to make a guess
  row, col = find_next_empty(puzzle)
  
  if row is None:
    return True

  # step 2: if there is space to assign a number, then make a guess between 1 and 9
  for guess in range(1,10):
    # step 3: check if the guess is valid
    if is_valid(puzzle, guess, row, col):
      puzzle[row][col] = guess
      # step 4: now recurse using this puzzle
      if solve_sudoku(puzzle):
        return True

    # if the guess isn't correct or didn't solve the puzzle, we need to backtrack and try a new number
    # reset the guess
    puzzle[row][col] = -1

  # if none of the numbers work, the puzzle is unsolvable
  return False

if __name__=="__main__":
  puzzle = [
    [5,3,-1,-1,7,-1,-1,-1,-1],
    [6,-1,-1,1,9,5,-1,-1,-1],
    [-1,9,8,-1,-1,-1,-1,6,-1],
    [8,-1,-1,-1,6,-1,-1,-1,3],
    [4,-1,-1,8,-1,3,-1,-1,1],
    [7,-1,-1,-1,2,-1,-1,-1,6],
    [-1,6,-1,-1,-1,-1,2,8,-1],
    [-1,-1,-1,4,1,9,-1,-1,5],
    [-1,-1,-1,-1,8,-1,-1,7,9]
  ]

  print(solve_sudoku(puzzle))
  print(puzzle)

