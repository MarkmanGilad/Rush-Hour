from State import State
from Graphics import Graphics
from State import State
from Action import Action
from Constant import *
from Graphics import *
from RushHour import *
import numpy as np

class DFS_Agent:
    def __init__(self , rushhour:RushHour):
        self.rushhour = rushhour
        self.path = []
        self.stop = False
        self.maxLevel = 10
    
    def get_Action(self,events  = None ,state:State = None):
        if self.path is None or len(self.path) == 0:
            self.search_path(state,[state],[])
            print(self.path)
            print(len(self.path))
        return self.path.pop(0)
    
    def search_path (self, state:State, visited, path):
        if self.stop:
            return
        if self.rushhour.is_end_of_game(state):
            self.stop = True
            self.path = path.copy()
            return
        
        if len(path) == self.maxLevel:
            print("max : ", len(visited))
            return
        actions = self.rushhour.all_legal_actions(state)
        for action in actions:
            new_state = self.rushhour.get_next_State(state , action)
            # if new_state in visited:
            #     print ("in", len(visited))
            if new_state not in visited and not self.stop:
                visited.append(new_state)
                path.append(action)
                
                self.search_path(state=new_state, visited=visited, path=path)
                path.pop()
    