import pygame
from Action import Action
from Graphics import Graphics
from Constant import *
from State import State
from RushHour import RushHour
import random
class Randon_Agent:
    def __init__(self , rushhour:RushHour):
        self.rushhour = rushhour

    def get_Action(self, events  = None ,state:State = None , train = None):
        legal_action_list = self.rushhour.all_legal_actions(state)
        return random.choice(legal_action_list)