from State import State
from Graphics import Graphics
from State import State
from Action import Action
from Constant import *
from Graphics import *
from RushHour import *
import numpy as np
import copy
import time

class A_Star_Agent:
    def __init__(self , rushhour : RushHour):
        self.rushhour = rushhour
        self.path = []
    
    def get_Action(self,events  = None ,state:State = None):
        if self.path is None or len(self.path) == 0:
            self.search_path(state)
            print(self.path)
            print(len(self.path))
        return self.path.pop(0)
    
    def search_path (self, state:State,):
        start_time = time.time()
        visited = {state:None}
        heap = {}
        # state.action = None
        state.g = 0
        state.calc_h()
        heap[state] = state.f, state.g
    
        while heap:
            
            state = min(heap, key= lambda k: heap[k][0])
            heap.pop(state)
            # visited[state] = state.action
            print(state.h, ", ", state.f, ", ", state.g)   
            
            if self.rushhour.is_end_of_game(state):
                print("--- %s seconds for victory ---" % (time.time() - start_time))
                print(len(visited))
                return self.find_path(state, visited)
            
            actions = self.rushhour.all_legal_actions(state)
            for action in actions:
                cost = 1
                new_state = self.rushhour.get_next_State(state , action)
                if new_state in visited:
                    continue
                # new_state.action = action
                visited[new_state] = action

                new_state.g = state.g + cost
                new_state.calc_h()

                if new_state not in heap:
                    heap[new_state] = new_state.f, new_state.g

                elif heap[new_state][1] > state.g + cost:
                    heap[new_state] = new_state.f, new_state.g
                    
        return []

    def find_path (self, state, visited):
        self.path = []
        while visited[state]:
            action = visited[state]
            self.path.insert(0, action)
            print("in action" , action)
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
