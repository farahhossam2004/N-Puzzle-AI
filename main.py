import pygame
import random
import time 
from settings import *
from sprite import * 
from heioristic_Function import *
import copy
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
        self.elapsed_time = 0
        self.high_score = float(self.get_high_score()[0])
        
    def get_high_score(self):
        with open("high_score.txt", "r") as file:
            scores = file.read().splitlines()
        return scores               #list
    
    def save_score(self):
        with open("high_score.txt", "w") as file:
            file.write(str("%.3f\n" % self.high_score))

    def create_game(self):
        grid = []
        number = 1
        for x in range(gameSize):
            grid.append([])
            for y in range(gameSize):
                grid[x].append(number)
                number += 1
        grid[-1][-1] = 0
        return grid
    
    
    def shuffle(self):
        possible_moves = []
        for row, tiles in enumerate(self.tiles):
            for col, tile in enumerate(tiles):
                if tile.text == "empty":
                    if tile.right():
                        possible_moves.append("right")
                    if tile.left():
                        possible_moves.append("left")
                    if tile.up():
                        possible_moves.append("up")
                    if tile.down():
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
        for row , x in enumerate(self.tiles_grid):
            self.tiles.append([])
            for col , tile in enumerate(x):
                if tile!=0:
                    self.tiles[row].append(Tile(self ,  col , row , str(tile)))
                else :
                    self.tiles[row].append(Tile(self ,  col , row , "empty"))
                    
                    
    def new(self):
        self.all_sprites = pygame.sprite.Group()
        self.tiles_grid = self.create_game()
        self.tiles_grid_completed = self.create_game()
        self.elapsed_time = 0
        self.start_timer = False
        self.start_game = False
        self.button_list = []
        self.button_list.append(Button(775, 100, 200, 50, "Shuffle", White, Black))
        self.button_list.append(Button(775, 170, 200, 50, "Reset", White, Black))
        self.button_list.append(Button(400, 100, 250, 50, "1st Function",Red, White))
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
                if self.high_score > 0:
                    self.high_score = self.elapsed_time if self.elapsed_time < self.high_score else self.high_score
                else:
                    self.high_score = self.elapsed_time
                self.save_score()
            
            if self.start_timer:
                self.timer = time.time()
                self.start_timer = False
            self.elapsed_time = time.time() - self.timer
        
        if self.start_shuffle:
            self.shuffle()
            self.draw_tiles()
            self.shuffle_time += 1
            if self.shuffle_time > 120:
                self.start_shuffle = False
                self.start_game = True 
                self.start_timer = True
    
        self.all_sprites.update()
    
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
        UIElement(710, 380, "High Score = %.3f" %(self.high_score if self.high_score > 0 else 0)).draw(self.screen)
        pygame.display.flip()
        
        
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for row, tiles in enumerate(self.tiles):
                    for col, tile in enumerate(tiles):
                        if tile.click(mouse_x, mouse_y):
                            if tile.right() and self.tiles_grid[row][col + 1] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row][col + 1] = self.tiles_grid[row][col + 1], self.tiles_grid[row][col]
                                
                            if tile.left() and self.tiles_grid[row][col - 1] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row][col - 1] = self.tiles_grid[row][col - 1], self.tiles_grid[row][col]
                                
                            if tile.up() and self.tiles_grid[row - 1][col] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row - 1][col] = self.tiles_grid[row - 1][col], self.tiles_grid[row][col]
                            
                            if tile.down() and self.tiles_grid[row + 1][col] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row + 1 ][col] = self.tiles_grid[row + 1][col], self.tiles_grid[row][col]
                            
                            self.draw_tiles()
                                
                            
                for button in self.button_list:
                    if button.click(mouse_x, mouse_y):
                        if button.text == "Shuffle":
                            self.shuffle_time = 0
                            self.start_shuffle = True
                        if button.text == "Reset":
                            self.new()
                        if button.text == "1st Function":
                            if misplaced_tiles_function(self.tiles_grid, gameSize) != 0:
                                new_list = self.tiles_grid
                                for i, tiles in enumerate(self.tiles):
                                    for j, tile in enumerate(tiles):
                                        if self.tiles_grid[i][j] == 0:
                                            
                                            up, down, right, left = None, None, None, None
                            
                                            if tile.up()  :
                                                new_list_up = copy.deepcopy(new_list)
                                                new_list_up[i][j], new_list_up[i-1][j] = new_list_up[i-1][j], new_list_up[i][j]
                                                up = misplaced_tiles_function(new_list_up, gameSize)

                                            if tile.down() :
                                                new_list_down = copy.deepcopy(new_list)
                                                new_list_down[i][j], new_list_down[i+1][j] = new_list_down[i+1][j], new_list_down[i][j]
                                                down = misplaced_tiles_function(new_list_down, gameSize)

                                            if tile.left() :
                                                new_list_left = copy.deepcopy(new_list)
                                                new_list_left[i][j], new_list_left[i][j-1] = new_list_left[i][j-1], new_list_left[i][j]
                                                left = misplaced_tiles_function(new_list_left, gameSize)

                                            if tile.right() :
                                                new_list_right = copy.deepcopy(new_list)
                                                new_list_right[i][j], new_list_right[i][j+1] = new_list_right[i][j+1], new_list_right[i][j]
                                                right = misplaced_tiles_function(new_list_right, gameSize)

                                            if up is not None and (down is None or up < down) and (left is None or up < left) and (right is None or up < right):
                                                self.tiles_grid = new_list_up
                                            elif down is not None and (up is None or down < up) and (right is None or down < right) and (left is None or down < left):
                                                self.tiles_grid = new_list_down
                                            elif right is not None and (up is None or right < up) and (left is None or right < left) and (down is None or right < down):
                                                self.tiles_grid = new_list_right
                                            elif left is not None and (up is None or left < up) and (right is None or left < right) and (down is None or left < down):
                                                self.tiles_grid = new_list_left
                                            else :
                                                print("Stuck")
                                        self.draw_tiles()
                                        self.update()
                            else : 
                                print("Aaaaaa")


                            


    
game = Game()
while True:
    game.new()
    game.run()