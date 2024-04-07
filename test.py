import pygame
from State import State
from RushHour import RushHour
from Graphics import *
from Constant import *


FPS = 60
pygame.display.set_caption('Rush Hour')

env = RushHour()
state = env.random_init_state(shuffle_time=200, cars_num=7) 
graphics = Graphics(state)
def main():
    run = True
    graphics.draw()
    while run:  
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False
        
        pygame.display.update()
    pygame.quit()

if __name__ == '__main__':
    main()