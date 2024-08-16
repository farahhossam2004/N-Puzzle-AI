
def misplaced_tiles_function(board, size):
    number_of_places = 0
    
    # Initialize the correct board
    correct_board = [[0] * size for _ in range(size)]
    
    tilesplaceholder = 1
    for i in range(size):
        for j in range(size):
            if i == size - 1 and j == size - 1: #lw a5r element 
                correct_board[i][j] = 0 
            else:
                correct_board[i][j] = tilesplaceholder
                tilesplaceholder += 1

    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] != correct_board[i][j]:
                number_of_places += 1

    return number_of_places