import numpy as np
import random
from Constant import *

class Create_Board:
    def __init__(self , small_cars = 2, big_cars = 2) :
        self.small_cars = small_cars
        self.big_cars = big_cars

    def create_initial_state1(self):
        board = np.full((6,7),0)
        board[5,3] = 1
        board[4,3] = 1
        car_num_counter = 2
        for i in range(1,self.small_cars + 1):
            flag = True
            while flag:
                row = random.randrange(1,ROWS-1)
                col = random.randrange(1,COLS)
                if board[row,col] == 0:
                    board[row,col] = car_num_counter
                    dic = self.all_possible_points2((row,col), board)
                    lst_points = self.to_lst(dic)
                    if lst_points:
                        point = random.choice(lst_points)
                        board[point[0] , point[1]] = car_num_counter
                        flag = False
                    else:
                        board[row,col] = 0
            car_num_counter += 1
        for i in range(1 , self.big_cars + 1):
            flag = True
            while flag:
                row = random.randrange(1,ROWS-1)
                col = random.randrange(1,COLS)
                if board[row,col] == 0:
                    board[row,col] = car_num_counter
                    lst_points = self.all_possible_points3((row,col) , board)
                    if lst_points:
                        points = random.choice(lst_points)
                        point1 = points[0]
                        point2 = points[1]
                        board[point1[0] , point1[1]] = car_num_counter
                        board[point2[0] , point2[1]] = car_num_counter
                        flag = False
                    else: 
                        board[row,col] = 0
            car_num_counter += 1
        return board

    def to_lst(self, dic:dict):
        lst = []
        for v in dic.values():
            lst.append(v)
        return lst

    def all_possible_points3(self,point:tuple , board):
        point_x = point[0]
        point_y = point[1]
        dic = {"UP" : (point_x -1 , point_y) , "RIGHT" : (point_x , point_y + 1) , "DOWN" : (point_x + 1 , point_y) , "LEFT" : (point_x , point_y - 1)}
        if point_x == 0:
            del dic["UP"]
        if point_x == 5:
            del dic["DOWN"]
        if point_y == 0:
            del dic["LEFT"]
        if point_y == 6:
            del dic["RIGHT"]
        final_lst = []
        if "UP" in dic.keys() and "DOWN" in dic.keys():
            tpl1 = dic["UP"]
            tpl2 = dic["DOWN"]
            if board[tpl1[0] , tpl1[1]] == 0 and board[tpl2[0] , tpl2[1]] == 0:
                tpl = (tpl1 , tpl2)
                final_lst.append(tpl)
        if "RIGHT" in dic.keys() and "LEFT" in dic.keys():
            tpl1 = dic["RIGHT"]
            tpl2 = dic["LEFT"]
            if board[tpl1[0] , tpl1[1]] == 0 and board[tpl2[0] , tpl2[1]] == 0:
                tpl = (tpl1 , tpl2)
                final_lst.append(tpl)
        return final_lst

    def all_possible_points2(self,point:tuple , board):
        point_x = point[0]
        point_y = point[1]
        dic = {"UP" : (point_x -1 , point_y) , "RIGHT" : (point_x , point_y + 1) , "DOWN" : (point_x + 1 , point_y) , "LEFT" : (point_x , point_y - 1)}
        if point_x == 0:
            del dic["UP"]
        if point_x == 5:
            del dic["DOWN"]
        if point_y == 0:
            del dic["LEFT"]
        if point_y == 6:
            del dic["RIGHT"]
        keys = []
        for key in dic.keys():
            point = dic[key]
            x = point[0]
            y = point[1]
            if board[x , y] != 0:
                keys.append(key)
        for key in keys:
            del dic[key]
        return dic

