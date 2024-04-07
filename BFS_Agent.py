from State import State
from Graphics import Graphics
from State import State
from Action import Action
from Constant import *
from Graphics import *
from RushHour import *
import numpy as np
import copy

class BFS_Agent:
    def __init__(self , rushhour:RushHour):
        self.rushhour = rushhour
        self.path = []

    def get_Action(self,events  = None ,state:State = None):
        if self.path is None or len(self.path) == 0:
            self.search_path(state)
            print(self.path)
            print(len(self.path))
        return self.path.pop(0)
    
    def search_path (self, state):
        visited = {state: None}
        queue = [state]

        while queue:
            state = queue.pop()
            if self.rushhour.is_end_of_game(state):
                print(len(visited))
                print(visited[state])
                break
            actions = self.rushhour.all_legal_actions(state)
            for action in actions:
                new_state = self.rushhour.get_next_State(state , action)
                if new_state not in visited:
                    queue.insert(0, new_state)
                    visited[new_state] = action
            
        return self.find_path(state , visited)

    def find_path (self, state, visited):
        self.path = []
        while visited[state]:
            action = visited[state]
            self.path.insert(0, action)
            # state = self.rushhour.get_next_State(state , action)
            state = self.rushhour.get_next_State(state , self.Inverse(action))
        return self.path 
    
    def Inverse (self,action):
        if action[1] == 1:
            return (action[0] , 3)
        if action[1] == 3:
            return (action[0] , 1)
        if action[1] == 2:
            return (action[0] , 4)
        if action[1] == 4:
            return (action[0] , 2)
