from enum import Enum

class Action (Enum):
    UP = 1
    RIGHT = 2
    LEFT = 4
    DOWN = 3

    def Inverse (action):
        if action[1] == 1:
            return 3
        if action[1] == 3:
            return 1
        if action[1] == 2:
            return 4
        if action[1] == 4:
            return 2