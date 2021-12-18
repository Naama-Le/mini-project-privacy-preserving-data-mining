from math import log2
import numpy
import random
import csv
from player import Player
from scipy.interpolate import lagrange

players = [Player(4, index) for index in range(4)]
class Dealer:
    def __init__(self):
        self.__num_of_players = 4
        self.__random_X_vals = []

    def create_random_X_vals(self):
        self.__random_X_vals = random.sample(range(1,50), self.__num_of_players)

    def get_random_X_vals(self):
        return self.__random_X_vals

    def get_all_X_vals(self):
        return [player.get_players_sum_X_val() for player in players]
    
    def get_sec_val_sum(self, X, PX):
        return int(round(lagrange(X, PX)(0)))

    # calc E_TA without dividing by T as we'll compare these values to find the best attr A among all
    # A is the set of possible attr values for A
    # Ta is an array holds Ta values for each a
    # Tac is a 2D-aaray holds Tac values for each a and category value c
    def calc_E_TA(self, A, Ta, Tac):
        E_TA = (-sum(sum(abs(Tac[attr][cat])*abs(log2(Tac[attr][cat])) for cat in Tac) for attr in A))
        + (sum(abs(Ta[attr])*log2(abs(Ta[attr])) for attr in A))
        return E_TA