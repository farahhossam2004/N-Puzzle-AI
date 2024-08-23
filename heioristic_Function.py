
#Function  number 1 
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


#Function number 3
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


# Function Number 4 
def Linear_distances(board, size):
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
    linear_conflict = 0
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
                
                # Check for linear conflicts in the row
                if i == correct_i:
                    for k in range(j + 1, size):
                        other_value = board[i][k] # bshof el arkam elfnfs el row l7d mwsl llrkm bta3y
                        if other_value != 0:
                            correct_other_j = None
                            for y in range(size):
                                if correct_board[i][y] == other_value:
                                    correct_other_j = y # condition byshof el mkan els7 bta3 el rkm eltany
                                    break
                            if correct_other_j is not None and correct_other_j < correct_j: # b ytcheck 3almkan bta3 el tany lw 2blh w eltany b3dha f conflict 
                                linear_conflict += 1

                # Check for linear conflicts in the column
                if j == correct_j:
                    for k in range(i + 1, size):
                        other_value = board[k][j]
                        if other_value != 0:
                            correct_other_i = None
                            for x in range(size):
                                if correct_board[x][j] == other_value:
                                    correct_other_i = x
                                    break
                            if correct_other_i is not None and correct_other_i < correct_i:
                                linear_conflict += 1
    
    # Each linear conflict adds an extra cost of 2 moves
    total_distance += 2 * linear_conflict
    
    return total_distance


#Function  number 2
def misplaced_tiles_with_constraints(board, size):
    number_of_places = 0
    row_column_penalty = 0
    
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
            current_value = board[i][j]
            if current_value != correct_board[i][j]:
                number_of_places += 1
                
                # Find the correct position of the current tile
                correct_i, correct_j = None, None
                for x in range(size):
                    for y in range(size):
                        if correct_board[x][y] == current_value:
                            correct_i, correct_j = x, y
                            break
                    if correct_i is not None:
                        break
                
                # Check if the tile is in the correct row but wrong column
                if i == correct_i and j != correct_j:
                    row_column_penalty += 1
                
                # Check if the tile is in the correct column but wrong row
                if j == correct_j and i != correct_i:
                    row_column_penalty += 1

    return number_of_places + row_column_penalty


