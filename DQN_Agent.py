import torch
import random
import math
from DQN import DQN
import numpy as np
from RushHour import RushHour
from Constant import *
from State import State

class DQN_Agent:
    def __init__(self,rushhour:RushHour ,parametes_path = None, train = True, env= None):
        self.rushhour = rushhour
        self.DQN = DQN()
        if parametes_path:
            self.DQN.load_params(parametes_path)
        self.train = train
        self.setTrainMode()

    def setTrainMode (self):
          if self.train:
              self.DQN.train()
          else:
              self.DQN.eval()

    def get_Action (self, state, epoch = 50, events= None, train = True) -> tuple:
        actions = self.rushhour.all_legal_actions(state)
        if self.train and train:
            epsilon = self.epsilon_greedy(epoch)
            rnd = random.random()
            if rnd < epsilon:
                return random.choice(actions)
        
        # print(actions)
        state_tensor = state.toTensor()
        actions_np = np.array(actions)
        action_tensor = torch.tensor(actions_np,dtype=torch.float32)
        expand_state_tensor = state_tensor.unsqueeze(0).repeat((len(action_tensor),1))
        with torch.no_grad():
            Q_values = self.DQN(expand_state_tensor , action_tensor)
        max_index = torch.argmax(Q_values)
        return actions[max_index]
    
    def get_Actions (self, states_tensor: State, dones) -> torch.tensor:
        actions = []
        boards_tensor = states_tensor
        # actions_tensor = states_tensor[1]
        for i, board in enumerate(boards_tensor):
            if dones[i].item():
                actions.append((0,0))
            else:
                state = State.tensorToState(boards_tensor[i])
                actions.append(self.get_Action(state = state, train=False)) # fix bug
        return torch.tensor(actions)

    def get_Actions_Values (self, states):
        with torch.no_grad():
            Q_values = self.DQN(states)
            max_values, max_indices = torch.max(Q_values,dim=1) # best_values, best_actions
        
        return max_indices.reshape(-1,1), max_values.reshape(-1,1)

    def Q (self, states, actions):
        Q_values = self.DQN(states)
        rows = torch.arange(Q_values.shape[0]).reshape(-1,1)
        cols = actions.reshape(-1,1)
        return Q_values[rows, cols]

    def epsilon_greedy(self,epoch, start = epsilon_start, final=epsilon_final, decay=epsiln_decay):
        # res = final + (start - final) * math.exp(-1 * epoch/decay)
        if epoch < decay:
            return start - (start - final) * epoch/decay
        return final
        
    def loadModel (self, file):
        self.model = torch.load(file)
    
    def save_param (self, path):
        self.DQN.save_params(path)

    def load_params (self, path):
        self.DQN.load_params(path)

    def __call__(self, events= None, state=None):
        return self.get_Action(state)