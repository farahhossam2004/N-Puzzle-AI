import pygame
import random
import time 
from settings import *
from sprite import * 
from heioristic_Function import *
import copy
import heapq
import settings

class Game:
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.shuffle_time = 0
        self.start_shuffle = False
        self.previous_choice = ""
        self.start_game = False     # boolean to check if the game is running 
        self.start_timer = False
        self.start_time = 0
        self.elapsed_time = 0
        self.start_solving = False
        
        


    def create_game(self):
        grid = []
        number = 1
        for x in range(settings.gameSize):
            grid.append([])
            for y in range(settings.gameSize):
                grid[x].append(number)
                number += 1
        grid[-1][-1] = 0
        return grid
    
    
    def shuffle(self):
        possible_moves = []
        for row, tiles in enumerate(self.tiles):
            for col, tile in enumerate(tiles):
                if tile.text == "empty":
                    if tile.right() and col + 1 < settings.gameSize:
                        possible_moves.append("right")
                    if tile.left() and col - 1 >= 0:
                        possible_moves.append("left")
                    if tile.up() and row - 1 >= 0:
                        possible_moves.append("up")
                    if tile.down() and row + 1 < settings.gameSize:
                        possible_moves.append("down")
                    break           # 3shan hya empty tile wahda f l loop t2f b2a 
            if len(possible_moves) > 0:
                break

        if self.previous_choice == "right":
            possible_moves.remove("left") if "left" in possible_moves else possible_moves

        elif self.previous_choice == "left":
            possible_moves.remove("right") if "right" in possible_moves else possible_moves

        elif self.previous_choice == "up":
            possible_moves.remove("down") if "down" in possible_moves else possible_moves

        elif self.previous_choice == "down":
            possible_moves.remove("up") if "up" in possible_moves else possible_moves


        choice = random.choice(possible_moves)
        self.previous_choice = choice
        if choice == "right":
            self.tiles_grid[row][col], self.tiles_grid[row][col + 1] = self.tiles_grid[row][col + 1], self.tiles_grid[row][col]

        elif choice == "left":
            self.tiles_grid[row][col], self.tiles_grid[row][col - 1] = self.tiles_grid[row][col - 1], self.tiles_grid[row][col]

        elif choice == "up":
            self.tiles_grid[row][col], self.tiles_grid[row - 1][col] = self.tiles_grid[row - 1][col], self.tiles_grid[row][col]

        elif choice == "down":
            self.tiles_grid[row][col], self.tiles_grid[row + 1][col] = self.tiles_grid[row + 1][col], self.tiles_grid[row][col]



    def draw_tiles(self):
        self.tiles = []
        for i, row in enumerate(self.tiles_grid):
            self.tiles.append([])
            for j, col in enumerate(row):  # Iterate through columns correctly
                tile_value = self.tiles_grid[i][j]  # Use i and j to access the correct tile value
                # print(f"Drawing tile at ({i}, {j}) with value {tile_value}")
                if tile_value != 0:
                    self.tiles[i].append(Tile(self, j, i, str(tile_value)))  # Pass row as i, column as j
                else:
                    self.tiles[i].append(Tile(self, j, i, "empty"))
        
        # Debugging
        # print("Tiles after draw_tiles:")
        # for row in self.tiles:
        #     print([tile.text for tile in row])


    def new(self):
        self.all_sprites = pygame.sprite.Group()
        self.tiles_grid = self.create_game()
        self.tiles_grid_completed = self.create_game()
        self.elapsed_time = 0
        self.start_timer = False
        self.start_game = False
        self.start_solving = False
        self.button_list = []
        self.button_list.append(Button(775, 100, 250, 50, "Shuffle", cmawy, Black))
        self.button_list.append(Button(775, 170, 250, 50, "Reset", cmawy, Black))
        self.button_list.append(Button(775, 240, 250, 50, "1st Function",Red, White))
        self.button_list.append(Button(775, 310, 250, 50, "2nd Function",Green, White))
        self.button_list.append(Button(775, 380, 250, 50, "3rd Function",LightGrey, White))
        self.button_list.append(Button(775, 450, 250, 50, "4th Function",brown, White))
        self.button_list.append(Button(630, 100,120, 50, "3 x 3",Green, White))
        self.button_list.append(Button(630, 170, 120, 50, "4 x 4",LightGrey, White))
        self.button_list.append(Button(630, 240, 120, 50, "5 x 5",brown, White))
        
        self.draw_tiles()
        
        
    
    def run(self):
        self.playing = True 
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
    
    
    def update(self):
        
        if self.start_game:
            
            if self.tiles_grid == self.tiles_grid_completed:
                self.start_game = False
                self.start_timer = False
            
            if self.start_timer:
            #     self.timer = time.time()
            #     self.start_timer = False
                self.elapsed_time = time.time() - self.start_time
        
        if self.start_shuffle:
            self.shuffle()
            self.draw_tiles()
            self.shuffle_time += 1
            if self.shuffle_time > 30:
                self.start_shuffle = False
                
        if self.start_solving:
            self.start_game = True
            if not self.start_timer:
                self.start_timer = True
                self.start_time = time.time()
            self.draw_tiles()
        
        self.all_sprites.update()
        self.draw()
    
    def draw_grid(self):
        for row in range(-1, gameSize * tileSize, tileSize):
            pygame.draw.line(self.screen, LightGrey, (row, 0), (row, gameSize * tileSize) )
        for column in range(-1, gameSize * tileSize, tileSize):
            pygame.draw.line(self.screen, LightGrey, (0, column), (gameSize * tileSize, column) )
            
            
    
    def draw(self):
        self.screen.fill(BGColor)
        self.all_sprites.draw(self.screen)
        self.draw_grid()
        for button in self.button_list:
            button.draw(self.screen)
        
        UIElement(825, 35, "%.3f" % self.elapsed_time).draw(self.screen)
        pygame.display.flip()
        
    


    def Best_First_Search(self, func):
        priority_Queue = []  # To be visited
        Visited = set()  # Visited states
        self.start_solving = True

        # Push the initial state onto the priority queue
        heapq.heappush(priority_Queue, (func(self.tiles_grid, gameSize), self.tiles_grid))
        
        while priority_Queue:
            current_priority, current_state = heapq.heappop(priority_Queue)
            
            self.tiles_grid = current_state
            self.update()
            print(self.tiles_grid)

            if current_state == self.tiles_grid_completed:
                # self.start_solving = False
                self.update()
                print("Completed")
                return current_state

            Visited.add(tuple(map(tuple, current_state)))

            for neighbour in self.get_neighbours():
                if tuple(map(tuple, neighbour)) not in Visited:
                    heapq.heappush(priority_Queue, (func(neighbour, gameSize), neighbour))
                    self.tiles_grid = neighbour  # Apply the move

        print("No Solution")
        return None
    

    def get_neighbours(self):
        neighbours = []

        for i, tiles in enumerate(self.tiles):
            for j, tile in enumerate(tiles):
                if self.tiles_grid[i][j] == 0:  # Found the empty tile
                    
                    # Move the empty tile up
                    if i - 1 >= 0:
                        up_list = copy.deepcopy(self.tiles_grid)
                        up_list[i][j], up_list[i-1][j] = up_list[i-1][j], up_list[i][j]
                        neighbours.append(up_list)
                    
                    # Move the empty tile down
                    if i + 1 < settings.gameSize:
                        down_list = copy.deepcopy(self.tiles_grid)
                        down_list[i][j], down_list[i+1][j] = down_list[i+1][j], down_list[i][j]
                        neighbours.append(down_list)
                    
                    # Move the empty tile right
                    if j + 1 < settings.gameSize:
                        right_list = copy.deepcopy(self.tiles_grid)
                        right_list[i][j], right_list[i][j+1] = right_list[i][j+1], right_list[i][j]
                        neighbours.append(right_list)
                    
                    # Move the empty tile left
                    if j - 1 >= 0:
                        left_list = copy.deepcopy(self.tiles_grid)
                        left_list[i][j], left_list[i][j-1] = left_list[i][j-1], left_list[i][j]
                        neighbours.append(left_list)
        for neighbour in neighbours:
            print("Neighbour state:", neighbour)
        return neighbours

    def change_board_size(self, new_size):
        global gameSize
        gameSize = new_size
        settings.gameSize = new_size  # Update the settings
        self.new()  # Reinitialize the game with the new board size



    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for row, tiles in enumerate(self.tiles):
                    for col, tile in enumerate(tiles):
                        if tile and tile.click(mouse_x, mouse_y):
                            if tile.right() and col + 1 < settings.gameSize:
                                if self.tiles_grid[row][col + 1] == 0:
                                    self.tiles_grid[row][col], self.tiles_grid[row][col + 1] = self.tiles_grid[row][col + 1], self.tiles_grid[row][col]
                                
                            if tile.left() and col - 1 >= 0:
                                if self.tiles_grid[row][col - 1] == 0:
                                    self.tiles_grid[row][col], self.tiles_grid[row][col - 1] = self.tiles_grid[row][col - 1], self.tiles_grid[row][col]
                                
                            if tile.up() and row - 1 >= 0:
                                if self.tiles_grid[row - 1][col] == 0:
                                    self.tiles_grid[row][col], self.tiles_grid[row - 1][col] = self.tiles_grid[row - 1][col], self.tiles_grid[row][col]
                            
                            if tile.down() and row + 1 < settings.gameSize:
                                if self.tiles_grid[row + 1][col] == 0:
                                    self.tiles_grid[row][col], self.tiles_grid[row + 1 ][col] = self.tiles_grid[row + 1][col], self.tiles_grid[row][col]
                            
                            self.draw_tiles()
                                
                            
                for button in self.button_list:
                    if button.click(mouse_x, mouse_y):
                        if button.text == "Shuffle":
                            self.shuffle_time = 0
                            self.start_shuffle = True
                            self.elapsed_time = 0
                            self.start_timer = False
                            self.start_game = False
                            self.start_solving = False
                        if button.text == "Reset":
                            self.new()
                        if button.text == "1st Function":
                            self.Best_First_Search(misplaced_tiles_function)
                        if button.text == "2nd Function":
                            self.Best_First_Search(misplaced_tiles_with_constraints)
                        if button.text == "3rd Function":
                            self.Best_First_Search(distances)
                        if button.text == "4th Function":
                            self.Best_First_Search(Linear_distances)
                        if button.text == "3 x 3" :
                            self.change_board_size(3)
                        if button.text == "4 x 4" :
                            self.change_board_size(4)
                        if button.text == "5 x 5" :
                            self.change_board_size(5)
                            



game = Game()
while True:
    game.new()
    game.run()  