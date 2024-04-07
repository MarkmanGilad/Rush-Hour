from State import State
from Graphics import Graphics
from State import State
from Action import Action
from Create_Board import Create_Board
from Constant import *
from Graphics import *
# from Random_Agent import Random_Agent
import numpy as np

class RushHour:
    def __init__(self , state:State = None):
        if state == None:
            self.state = self.get_init_state()
            # self.state = self.init2()
        else:
            self.state = state
    
    def create_initial_state(self):
        board = np.full((7,7),0)
        board[5,3] = 1
        board[4,3] = 1
        print(board)
    
    def get_init_state(self):
        board = np.full((7,7),0)
        # init_board = Create_Board(4,3)
        # board = init_board.create_initial_state1()
        board = self.init3()
        state = State(board)
        state.step = 0
        return state
        # tempRush = RushHour(state)
        # agent = Random_Agent(tempRush)
        # # events = pygame.event.get()
        # for i in range(1,100):
        #     action = agent.get_Action(tempRush.state)
        #     if action:  
        #         tempRush.move2(tempRush.state , action)
        # return tempRush.state

    def find_car(self , rows , cols):
        x = self.state.board[rows,cols] 
        return x
    
    def update_board(self , cars:dict , state: State):
        state.board = np.full((6,7),0)
        for i in cars:
            x1 = cars[i].start[0]
            y1 = cars[i].start[1]
            x2 = cars[i].end[0]
            y2 = cars[i].end[1]
            if cars[i].direction == VERTICAL:
                length = cars[i].end[1] - cars[i].start[1]
                # print("car" , i , "length" , length)
                if length == 1:
                    state.board[y1,x1] = i
                    state.board[y2,x2] = i
                elif length == 2:
                    state.board[y1,x1] = i
                    state.board[y2 -1,x2 ] = i
                    state.board[y2,x2] = i
            if cars[i].direction == HORIZONTTAL:
                length2 = cars[i].end[0] - cars[i].start[0]
                # print("len" , length2)
                if length2 == 1:
                    state.board[y1,x1] = i
                    state.board[y2,x2] = i
                elif length2 == 2:
                    state.board[y1,x1] = i
                    state.board[y2,x2-1] = i
                    state.board[y2,x2] = i
    def calc_direction(self , state:State , car_num):
        row , col = np.where(state.board == car_num)
        row = row[0]
        col = col[0]
        if row != 0 and state.board[row -1 , col] == car_num :
            return "V"
        elif row != 5 and state.board[row + 1 , col] == car_num :
            return "V"
        elif col != 0 and state.board[row , col - 1] == car_num:
            return "H"
        elif col != 6 and state.board[row , col + 1] == car_num:
            return "H"
    
    def is_legal_move2(self , key , carNum , state:State): # לשפר את הפעולה אפשר למצוא את האורך של הרכב לפי ספירה של כמה פעמים המספר מופיע בלוח ולמצוא את האינדקס הראשון עם נאמפי ולייעל את הפעולה
        if key == Action.DOWN and carNum == 1 and state.board[5,3] == 1:
            return True
        if key == Action.RIGHT and self.calc_direction(state , car_num=carNum) == "H":
            lstTuple = []
            for row in range(6): #היה 6
                for col in range(7): # היה 7
                    if state.board[row,col] == carNum:
                        lstTuple.append((row,col))
            row_col_End = lstTuple[len(lstTuple)-1]
            rowEnd = row_col_End[0]
            colEnd = row_col_End[1]
            if colEnd == 6:
                # print("illegal move")
                return False
            # if state.board[rowEnd ,colEnd + 1] == 0:
            if state.board[rowEnd ,colEnd + 1] == 0:

                return True
        if key == Action.LEFT and self.calc_direction(state , car_num=carNum) == "H":
            lstTuple = []
            for row in range(6):
                for col in range(7):
                    if state.board[row,col] == carNum:
                        lstTuple.append((row,col))
            row_col_End = lstTuple[0]
            rowEnd = row_col_End[0]
            colEnd = row_col_End[1]
            if colEnd == 0:
                # print("illegal move")

                return False
            if state.board[rowEnd ,colEnd -1] == 0:
                return True
        if key == Action.UP and self.calc_direction(state , car_num=carNum) == "V":
            lstTuple = []
            for row in range(6):
                for col in range(7):
                    if state.board[row,col] == carNum:
                        lstTuple.append((row,col))
            row_col_End = lstTuple[0]
            rowEnd = row_col_End[0]
            colEnd = row_col_End[1]
            if rowEnd == 0:
                # print("illegal move")
                return False
            if state.board[rowEnd - 1,colEnd] == 0:
                return True
        if key == Action.DOWN and self.calc_direction(state , car_num=carNum) == "V":
            lstTuple = []
            for row in range(6):
                for col in range(7):
                    if state.board[row,col] == carNum:
                        lstTuple.append((row,col))
            row_col_End = lstTuple[len(lstTuple)-1]
            rowEnd = row_col_End[0]
            colEnd = row_col_End[1]
            if rowEnd == 5:
                # print("illegal move")
                return False
            if state.board[rowEnd + 1,colEnd] == 0:
                return True
        # print("illegal move")
        return False
    
    def move2(self , state , action):
        if state.board[5,3] == 1 and action[1] == 3:
            self.clear_car(state)
            return
        if 1 not in state.board and action[0] == 1:
            state.board[4,3] = 1
            state.board[5,3] = 1
            return
        carNumber = action[0]
        direction = action[1]
        lstTuple = []
        for row in range(6):
            for col in range(7):
                if state.board[row,col] == carNumber:
                    location = (row,col)
                    lstTuple.append(location)
        start = lstTuple[0]          
        end = lstTuple[len(lstTuple) - 1]
        if direction == 1:
            state.board[start[0] - 1 , start[1]] = carNumber
            state.board[end[0] , end[1]] = 0  
        if direction == 3:
            state.board[end[0] + 1 , start[1]] = carNumber
            state.board[start[0] , start[1]] = 0  
        if direction == 4:
            state.board[start[0] , start[1] - 1] = carNumber
            state.board[end[0] , end[1]] = 0
        if direction == 2:
            state.board[end[0] , end[1] + 1] = carNumber
            state.board[start[0] , start[1]] = 0
        state.step+=1
               
    def all_legal_actions(self, state:State):
        legal_Action_list = []
        list_of_unique_values = np.unique(state.board).tolist()
        for carNum in list_of_unique_values:
            for dircetion in range(1,5):
                if self.is_legal_move2(self.direction_To_Action(dircetion) , carNum , state):
                    legal_Action_list.append((carNum , dircetion))
        return legal_Action_list
    
    def get_next_State(self, state:State , action):
        newState = state.copy()
        self.move2(newState , action)
        return newState
    
    def clear_car (self, state):
        state.board[state.board == 1] = 0
        
    def is_end_of_game (self, state):
        return 1 not in state.board
    
    def direction_To_Action(self, dircetion):
        if dircetion == 1:
            return Action.UP
        if dircetion == 2:
            return Action.RIGHT
        if dircetion == 3:
            return Action.DOWN
        if dircetion == 4:
            return Action.LEFT
        
    def action_To_Direction(self ,action:Action):
        if action == Action.UP:
            return 1
        if action == Action.RIGHT:
            return 2
        if action == Action.DOWN:
            return 3
        if action == Action.LEFT:
            return 4 
    
    def steps_to_end(self , state):
        row , col = np.where(state.board == 1)
        return 5 - row
        
    def reward(self, state , action):
        if self.is_end_of_game(state):
            return 10
        # return -0.5 * self.steps_to_end(state)
        if action[0] == 1 and action[1] == 3:
            return 0.1
        if action[0] == 1 and action[1] == 1:
            return -0.1
        return 0
    
    def init2 (self):
        board = np.array([[4, 4, 0, 3, 3, 0, 0], 
                          [12, 5, 5, 1, 0, 0, 0],
                          [12, 6, 0, 1, 2, 2, 0],
                          [12, 6, 11, 11, 11, 10, 0],
                          [0, 0, 8, 0, 9, 10, 0],
                          [7, 7, 8, 0, 9, 10, 0]])
        return board
    def init3 (self):
        board = np.array([[0, 0, 0, 0, 0, 0, 0], 
                          [0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 1, 0, 0, 0],
                          [0, 0, 0, 1, 0, 0, 0],
                          [0, 0, 0, 2, 2, 0, 0],
                          [0, 0, 3, 3, 0, 0, 0]])
        return board
    # def is_legal_move(self , rows , cols , action : Action , state: State = None):
    #     if state is None:
    #         state = self.state
    #     if action is None:
    #         return False
    #     car_index = self.find_car(rows,cols)
    #     if  car_index != 0:
    #         if action == Action.UP and self.state.Cars[car_index].direction == VERTICAL:
    #             if self.state.Cars[car_index].start[1] - 1 != -1 and self.find_car(self.state.Cars[car_index].start[1] -1,self.state.Cars[car_index].start[0]) == 0:
    #                 return True
    #         if action == Action.DOWN and self.state.Cars[car_index].direction == VERTICAL:
    #             if self.state.Cars[car_index].end[1] + 1 != 6 and self.find_car(self.state.Cars[car_index].end[1] +1,self.state.Cars[car_index].end[0]) == 0:
    #                 return True
    #         if action == Action.LEFT and self.state.Cars[car_index].direction == HORIZONTTAL:
    #             if self.state.Cars[car_index].start[0] -1 != -1 and self.find_car(self.state.Cars[car_index].start[1],self.state.Cars[car_index].start[0] -1) == 0:
    #                 return True
    #         if action == Action.RIGHT and self.state.Cars[car_index].direction == HORIZONTTAL:
    #             if self.state.Cars[car_index].end[0] + 1 != 6 and self.find_car(self.state.Cars[car_index].end[1],self.state.Cars[car_index].end[0] +1) == 0:
    #                 return True
    #     if state.Cars[1].end[1] == 5:
    #         return "win"
    #     return False
                      
    # def move(self , action:Action , rows , cols , state:State):
    #     if self.is_legal_move(rows , cols , action) == "win":
    #         return "win"
    #     if self.is_legal_move(rows , cols , action) == False:
    #         print("Illegal Move")
    #         return
    #     self.state = state
    #     car_index = self.find_car(rows,cols)
    #     if action == Action.UP:
    #         self.state.Cars[car_index].start = (self.state.Cars[car_index].start[0] , self.state.Cars[car_index].start[1] -1)
    #         self.state.Cars[car_index].end = (self.state.Cars[car_index].end[0] , self.state.Cars[car_index].end[1] -1)
    #         self.update_board(self.state.Cars)
    #     if action == Action.DOWN:
    #         car_index = self.find_car(rows,cols)
    #         self.state.Cars[car_index].start = (self.state.Cars[car_index].start[0] , self.state.Cars[car_index].start[1] +1)
    #         self.state.Cars[car_index].end = (self.state.Cars[car_index].end[0] , self.state.Cars[car_index].end[1] +1)
    #         self.update_board(self.state.Cars)
    #     if action == Action.LEFT:
    #         car_index = self.find_car(rows,cols)
    #         self.state.Cars[car_index].start = (self.state.Cars[car_index].start[0] -1, self.state.Cars[car_index].start[1])
    #         self.state.Cars[car_index].end = (self.state.Cars[car_index].end[0] -1, self.state.Cars[car_index].end[1])
    #         self.update_board(self.state.Cars)
    #     if action == Action.RIGHT:
    #         car_index = self.find_car(rows,cols)
    #         self.state.Cars[car_index].start = (self.state.Cars[car_index].start[0] +1, self.state.Cars[car_index].start[1])
    #         self.state.Cars[car_index].end = (self.state.Cars[car_index].end[0] +1, self.state.Cars[car_index].end[1])
    #         self.update_board(self.state.Cars)
