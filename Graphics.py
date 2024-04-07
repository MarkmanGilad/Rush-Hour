import pygame
from State import State
import numpy as np
from Constant import *

DARK_RED = (150, 0, 0)
DARK_GREEN = (0, 150, 0)
DARK_BLUE = (0, 0, 150)
LIGHT_RED = (255, 100, 100)
LIGHT_GREEN = (100, 255, 100)
LIGHT_BLUE = (100, 100, 255)

pygame.init()
class Graphics:
    def __init__(self,State:State ):
        self.state = State
        self.screen = self.setup_screen()

    def draw(self):
        self.screen.fill(LIGHTBLUE)
        self.draw_grid(self.screen,(WIDTH,HEIGHT),SQUARE_SIZE)
        self.draw_exit(self.screen , ROWS -1 , SQUARE_SIZE)
        self.draw_cars(self.screen , SQUARE_SIZE)
        self.draw_text(self.screen)
        
    def setup_screen(self):
        window_size = (WIDTH, HEIGHT)
        screen = pygame.display.set_mode(window_size)
        screen.fill(LIGHTBLUE)
        return screen
    
    def is_background(self ,action: tuple[int, int]):
        if self.screen.get_at(self.calc_pos(action)) == LIGHTBLUE:
            return True
        else:
            return False

    def draw_grid(self, screen, grid_size, cell_size):
        # Outer lines in black 
        pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, HEIGHT), 5)

        # Grid inner lines 
        for i in range(grid_size[0] + 1):
            x = i * cell_size
            pygame.draw.line(screen, BLACK, (x, 0), (x, HEIGHT))

        for j in range(grid_size[1] + 1) :
            y = j * cell_size
            pygame.draw.line(screen, BLACK, (0, y), (WIDTH, y))

    def draw_exit(self, screen, lowest_row_index, cell_size):
        # Black layer for the red car to pass 
        for i in range(0,7):
            pygame.draw.rect(screen,BLACK, (i * cell_size , lowest_row_index * cell_size , cell_size + 10 , cell_size + 30 ))

    def car_length(self, index):
        count = np.count_nonzero(self.state.board == index)  # Count occurrences of index
        return count
    
    def draw_cars(self, screen, cell_size):
        margin = 2  # Define the margin between cars
        board = self.state.board
        max_car_num = np.amax(board)
        for car_number in range(1, max_car_num + 1): 
            car_locations = []  # Store the locations of cells for each car number
            for i in range(6):
                for j in range(7):
                    if self.state.board[i, j] == car_number:
                        car_locations.append((i, j))
            
            if car_locations:  # If there are cells for the current car number
                top_i, top_j = min(car_locations)  # Find the top-left corner of the car
                bottom_i, bottom_j = max(car_locations)  # Find the bottom-right corner of the car
                
                # Calculate the rectangle size for the car
                rect_width = (bottom_j - top_j + 1) * cell_size - margin
                rect_height = (bottom_i - top_i + 1) * cell_size - margin
                
                # Set colors based on car number
                if car_number == 1:
                    color_top = LIGHT_RED
                    color_bottom = DARK_RED
                else:
                    if self.car_length(car_number) == 3:
                        color_top = LIGHT_GREEN
                        color_bottom = DARK_GREEN
                    else:
                        color_top = LIGHT_BLUE
                        color_bottom = DARK_BLUE
                        
                # Draw the base shape of the car without texture
                pygame.draw.rect(screen, color_top, (top_j * cell_size + margin, top_i * cell_size + margin, rect_width, rect_height))
                pygame.draw.rect(screen, color_bottom, (top_j * cell_size + margin, top_i * cell_size + (rect_height // 2) + margin, rect_width, rect_height // 2 - margin))
                
                # Create a textured surface for the car (diagonal stripes)
                texture_surface = pygame.Surface((rect_width, rect_height), pygame.SRCALPHA)
                for i in range(0, rect_width + rect_height, 10):
                    pygame.draw.line(texture_surface, (50, 50, 50, 100), (i, 0), (i - rect_height, rect_height), width=2)
                
                # Overlay the texture on the car
                screen.blit(texture_surface, (top_j * cell_size + margin, top_i * cell_size + margin))    
        
    # def draw_cars(self, screen , cell_size):
    #     for i in range(6):
    #         for j in range(7):
    #             if self.state.board[i,j] == 1:
    #                 color = RED
    #                 pygame.draw.rect(screen, color, (j*cell_size, i*cell_size, 1*cell_size, 1*cell_size))
    #             elif self.state.board[i,j] != 0:
    #                 if self.car_length(self.state.board[i,j]) == 3:
    #                     color = GREEN
    #                 else:
    #                     color = BLUE
    #                 pygame.draw.rect(screen, color, (j*cell_size, i*cell_size,1*cell_size, 1*cell_size))

    def draw_text(self, screen):
        # FONTS 
        font = pygame.font.Font(None, 36)
        font2 = pygame.font.Font(None, 50)
           # Render the text
        text2 = font2.render("^", True, RED)
        text = font.render("GET THE RED CAR IN HERE", True, RED)

            # Get the rectangle containing the text 
        text_rect = text.get_rect()
        text_rect2 = text2.get_rect()
          # Change position of the text
        text_rect.centerx = screen.get_rect().centerx
        text_rect.centery = screen.get_rect().bottom - 50

            # Pos of txt2
        text_rect2.centerx = screen.get_rect().centerx
        text_rect2.centery = screen.get_rect().bottom - 70
         # Draw the text
        screen.blit(text, text_rect)
        screen.blit(text2,text_rect2)

    def calc_row_col(self, pos):
        x, y = pos
        col = x // SQUARE_SIZE
        row = y // SQUARE_SIZE
        return (row, col)

    def calc_pos(self, row_col):
        row, col = row_col
        y = row * SQUARE_SIZE + SQUARE_SIZE//2
        x = col * SQUARE_SIZE + SQUARE_SIZE//2
        return x, y

    # def car_length2(self , index):
    #     if self.state.Cars[index].direction == VERTICAL:
    #         y1 = self.state.Cars[index].start[1]
    #         y2 = self.state.Cars[index].end[1]
    #         if (y2 - y1) == 2:
    #             return 3
    #         else:
    #             return 1
    #     if self.state.Cars[index].direction == HORIZONTTAL:
    #         x1 = self.state.Cars[index].start[0]
    #         x2 = self.state.Cars[index].end[0]
    #         if (x2 - x1) == 2:
    #             return 3
    #         else:
    #             return 1
    

    # def update_board(self , cars:dict):
    #     for i in cars:
    #         x1 = cars[i].start[0]
    #         y1 = cars[i].start[1]
    #         x2 = cars[i].end[0]
    #         y2 = cars[i].end[1]
    #         # print(x1,y1)
    #         # print(x2,y2)
    #         if cars[i].direction == VERTICAL:
    #             length = cars[i].end[1] - cars[i].start[1]
    #             # print("len" , length)
    #             if length == 1:
    #                 self.state.board[y1,x1] = i
    #                 self.state.board[y2,x2] = i
    #             elif length == 2:
    #                 self.state.board[y1,x1] = i
    #                 self.state.board[y2 -1,x2 ] = i
    #                 self.state.board[y2,x2] = i
    #         if cars[i].direction == HORIZONTTAL:
    #             length2 = cars[i].end[0] - cars[i].start[0]
    #             # print("len" , length2)
    #             if length2 == 1:
    #                 self.state.board[y1,x1] = i
    #                 self.state.board[y2,x2] = i
    #             elif length2 == 2:
    #                 self.state.board[y1,x1] = i
    #                 self.state.board[y2,x2-1] = i
    #                 self.state.board[y2,x2] = i
