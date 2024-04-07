import numpy as np
from Constant import *
import torch
import copy

class State:
    def __init__(self ,board):
        self.board = board #np array
        self.g = 0
        self.h = 0
        self.f = 0
        self.step = 0

    def copy (self): 
        newBoard = np.copy(self.board)
        state = State (newBoard )
        state.step = self.step 
        return state

    def __eq__(self, other):
        return np.equal(self.board, other.board).all()

    def Cars_and_Steps(self):
        #פעולה של הערכה יוריסטית של כל צעד מהנקודה הסופית מביא נקודה אחת שלילית וכל רכב שחוסם מביא נקודה אחת שלילית
        count = 0
        row_index = 0
        for row in range(ROWS - 1):
            if self.board[row , 3] == 1:
                row_index = row
        count = 6 - row_index       
        for row in range(row_index + 1, ROWS - 1):
            if self.board[row , 3] != 0:
                count += 1
                
        self.h = count
        self.f = self.h + self.g
        return count
    
    def toTensor (self, device = torch.device('cpu')) -> tuple:
        board_np = self.board.reshape(-1)
        board_tensor = torch.tensor(board_np, dtype=torch.float32, device=device)
        # state_tensor = torch.cat((board_tensor, torch.tensor([self.step])))
        
        return board_tensor
    
    def tensorToState (state_tensor):
        board_tensor = state_tensor[0:42]
        board = board_tensor.reshape([6,7]).cpu().numpy()
        state = State(board) 
        state.step = state_tensor[-1].item()
        return state
    
    def calc_h (self , Heuristic = Cars_and_Steps):
        return Heuristic(self)
    
    def __hash__(self) -> int:
        return hash(repr(self.board))
    