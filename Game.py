import pygame
from State import State
from RushHour import RushHour
from Human_Agent import Human_Agent
from Random_Agent import Randon_Agent
from DFS_Agent import DFS_Agent
from BFS_Agent import BFS_Agent
from A_Star_Agent import A_Star_Agent
from DQN_Agent import DQN_Agent
from Action import Action
from Graphics import *
from Constant import *

FPS = 60
pygame.display.set_caption('Rush Hour')

rushhour = RushHour()
rushhour.state = rushhour.random_init_state(shuffle_time=100, cars_num=5)
graphics = Graphics(rushhour.state)
# agent = Randon_Agent(rushhour = rushhour)
# for i in range(100):
#     events = pygame.event.get()
#     action = agent.get_Action(events , rushhour.state)
#     state_temp = rushhour.get_next_State(rushhour.state , action)
#     if not rushhour.is_end_of_game(state_temp) and action:
#         rushhour.move2(rushhour.state , action)

agent = Human_Agent(rushhour = rushhour)
# agent = Randon_Agent(rushhour = rushhour)
# agent = DFS_Agent(rushhour = rushhour)
# agent = BFS_Agent(rushhour = rushhour)
# agent = A_Star_Agent(rushhour = rushhour)
agent = DQN_Agent(rushhour = rushhour , parametes_path= "Data\params_20.pth" , train=True)


def main():
    run = True
    graphics.draw()
    print(rushhour.state.board)
    step = 0
    while run:  
        # pygame.display.update()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False
        action = agent.get_Action(state = rushhour.state , events = events, train=False)
        if action:  
            rushhour.move2(rushhour.state , action)
            step += 1
            print(action)
            # print(rushhour.state.Cars)
            graphics.draw()
            
        if rushhour.is_end_of_game(rushhour.state):
            print("win")
            run = False
        
        pygame.display.update()
        pygame.time.delay(400)
    pygame.quit()
    print("End Of The Game")


if __name__ == '__main__':
    main()
