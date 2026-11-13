# N-Queens using Backtracking (first queen is placed by the user)
# The first queen is fixed in row 0; backtracking places queens in rows 1..N-1.

COUNT = 0   # counts how many times the safety check is called (steps)


def is_safe(board, row, col, n):
    """Check if a queen at (row, col) is attacked by any queen above it."""
    global COUNT
    COUNT += 1

    # same column (upper side)
    for i in range(row):
        if board[i][col] == 1:
            return False

    # upper-left diagonal
    i, j = row - 1, col - 1
    while i >= 0 and j >= 0:
        if board[i][j] == 1:
            return False
        i -= 1
        j -= 1

    # upper-right diagonal
    i, j = row - 1, col + 1
    while i >= 0 and j < n:
        if board[i][j] == 1:
            return False
        i -= 1
        j += 1

    return True


def solve(board, row, n):
    """Place queens row by row; backtrack when no column works."""
    if row == n:                       # all queens placed
        return True

    for col in range(n):
        if is_safe(board, row, col, n):
            board[row][col] = 1        # place queen
            if solve(board, row + 1, n):
                return True
            board[row][col] = 0        # backtrack: remove queen
    return False


def print_board(board):
    for row in board:
        print(" ".join(str(c) for c in row))


def main():
    n = int(input("Enter N (size of the board): "))
    if n < 1:
        print("N must be at least 1.")
        return

    col = int(input(f"Enter column (1 to {n}) for the first queen in row 1: ")) - 1
    if not 0 <= col < n:
        print("Invalid column.")
        return

    board = [[0] * n for _ in range(n)]
    board[0][col] = 1                  # first queen placed manually

    print("\nInitial matrix (first queen placed):")
    print_board(board)

    if solve(board, 1, n):             # backtracking starts from row 2
        print("\nFinal N-Queens matrix:")
        print_board(board)
        print("\nQueen positions (row, column):",
              [(r + 1, board[r].index(1) + 1) for r in range(n)])
    else:
        print("\nNo solution exists with the first queen at that position.")

    print("Steps (safety checks) used:", COUNT)
    print("\nTime Complexity  : O(N!)  (worst case; pruning makes it much faster in practice)")
    print("Space Complexity : O(N^2) for the board matrix (O(N) for the recursion stack)")


if __name__ == "__main__":
    main()