import pygame
from Action import Action
from Graphics import Graphics
from Constant import *
from State import State
from RushHour import *
class Human_Agent:
    def __init__(self, rushhour:RushHour):
        self.mode = 0 # 0 - get car; 1 - get direction
        self.carNum = None
        self.rushhour = rushhour

    def get_Action (self, events , state:State):
        for event in events:
            if self.mode == 0:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    rowCols = self.pos_To_rowcols(pos)
                    rows , cols = rowCols
                    if state.board[rows,cols] != 0:
                        self.carNum = state.board[rows,cols]
                        self.mode = 1
                        return None
            if self.mode == 1:           
                if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                    self.mode = 0
                    return None
                key = self.find_Step(event)
                if key:
                    if self.rushhour.is_legal_move2(key , self.carNum , state):
                        self.mode = 0
                        return self.carNum , self.rushhour.action_To_Direction(key)
                    return None

        # if mode == 0:
            #   check for mousebutton and calc position
            #   if choose car: 
            #       self.car = car_number; 
            #       mode = 1
            #   return None;

            # if mode == 1:
            #   # if key is esc
                    # לאפס הכל ולהחזיר נון
            #   check for key
            #   if key is legal:
            #       mode = 0
            #       return self.car, direction
            #   return None
#-----------------------
    # def is_legal_move2(self , key , carNum , state:State):
    #     if key == Action.DOWN and carNum == 1 and state.board[5,3] == 1:
    #         return True
    #     if key == Action.RIGHT and state.Cars[carNum].direction == HORIZONTTAL:
    #         lstTuple = []
    #         for row in range(6):
    #             for col in range(7):
    #                 if state.board[row,col] == carNum:
    #                     lstTuple.append((row,col))
    #         row_col_End = lstTuple[len(lstTuple)-1]
    #         rowEnd = row_col_End[0]
    #         colEnd = row_col_End[1]
    #         if colEnd == 5:
    #             print("illegal move")
    #             return False
    #         if state.board[rowEnd ,colEnd + 1] == 0:
    #             return True
    #     if key == Action.LEFT and state.Cars[carNum].direction == HORIZONTTAL:
    #         lstTuple = []
    #         for row in range(6):
    #             for col in range(7):
    #                 if state.board[row,col] == carNum:
    #                     lstTuple.append((row,col))
    #         row_col_End = lstTuple[0]
    #         rowEnd = row_col_End[0]
    #         colEnd = row_col_End[1]
    #         if colEnd == 0:
    #             print("illegal move")

    #             return False
    #         if state.board[rowEnd ,colEnd -1] == 0:
    #             return True
    #     if key == Action.UP and state.Cars[carNum].direction == VERTICAL:
    #         lstTuple = []
    #         for row in range(6):
    #             for col in range(7):
    #                 if state.board[row,col] == carNum:
    #                     lstTuple.append((row,col))
    #         row_col_End = lstTuple[0]
    #         rowEnd = row_col_End[0]
    #         colEnd = row_col_End[1]
    #         if rowEnd == 0:
    #             print("illegal move")
    #             return False
    #         if state.board[rowEnd - 1,colEnd] == 0:
    #             return True
    #     if key == Action.DOWN and state.Cars[carNum].direction == VERTICAL:
    #         lstTuple = []
    #         for row in range(6):
    #             for col in range(7):
    #                 if state.board[row,col] == carNum:
    #                     lstTuple.append((row,col))
    #         row_col_End = lstTuple[len(lstTuple)-1]
    #         rowEnd = row_col_End[0]
    #         colEnd = row_col_End[1]
    #         if rowEnd == 5:
    #             print("illegal move")
    #             return False
    #         if state.board[rowEnd + 1,colEnd] == 0:
    #             return True
    #     print("illegal move")
    #     return False
    
    # def action_To_Direction(self ,action:Action):
    #     if action == Action.UP:
    #         return 1
    #     if action == Action.RIGHT:
    #         return 2
    #     if action == Action.DOWN:
    #         return 3
    #     if action == Action.LEFT:
    #         return 4 
        
    def find_Step (self , event):            
        if event.type == pygame.KEYUP:
            match event.key:
                case pygame.K_LEFT: return Action.LEFT
                case pygame.K_RIGHT: return Action.RIGHT
                case pygame.K_UP: return Action.UP
                case pygame.K_DOWN: return Action.DOWN
 
    def pos_To_rowcols(self, pos):
        row_col = self.calc_row_col(pos) 
        return row_col
    
    def get_Action_RowsCols (self, event= None):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            row_col = self.calc_row_col(pos) 
            return row_col
        else:
            return None

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
