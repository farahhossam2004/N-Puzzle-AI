def misplaced_tiles_function(board, size):
    number_of_places = 0
    
    # Initialize the correct board
    correct_board = [[0] * size for _ in range(size)]
    
    tilesplaceholder = 1
    for i in range(size):
        for j in range(size):
            if i == size - 1 and j == size - 1:  # Last element should be 0
                correct_board[i][j] = 0
            else:
                correct_board[i][j] = tilesplaceholder
                tilesplaceholder += 1

    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] != correct_board[i][j]:
                number_of_places += 1

    return number_of_places



def distances(board, size):
    # Initialize the correct board
    correct_board = [[0] * size for _ in range(size)]
    
    tilesplaceholder = 1
    for i in range(size):
        for j in range(size):
            if i == size - 1 and j == size - 1:  # Last element should be the empty space
                correct_board[i][j] = 0
            else:
                correct_board[i][j] = tilesplaceholder
                tilesplaceholder += 1
    
    # Calculate the Manhattan distance
    total_distance = 0
    for i in range(size):
        for j in range(size):
            current_value = board[i][j]
            if current_value != 0:  # Skip the empty tile
                # Find the correct position of the current tile in the correct board
                correct_position = None
                for x in range(size):
                    for y in range(size):
                        if correct_board[x][y] == current_value:
                            correct_position = (x, y)
                            break
                    if correct_position:
                        break
                
                # Add the Manhattan distance to the total distance
                correct_i, correct_j = correct_position
                total_distance += abs(i - correct_i) + abs(j - correct_j)
    
    return total_distance