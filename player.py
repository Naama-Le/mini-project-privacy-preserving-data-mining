import numpy
import random
import csv
import dealer
from dealer import Dealer
class Player:

    def __init__(self, num_of_players, player_index):
        self.__player_index = player_index
        self.__db = "db" + str(player_index) + ".csv"
        self.__num_of_players = num_of_players
        self.__polynom_coefs = []

    def get_polynom_coef(self):
        return self.__polynom_coefs

    def random_vals_X(self):
        return Dealer.get_random_X_vals()

    def get_num_of_players(self):
        return self.__num_of_players

    def create_poly(self, sec_val):
        rank = self.get_num_of_players()-1
        self.__polynom_coefs =  [sec_val] + [random.randint(-20,20) for _ in range(rank-1)]
        return self.__polynom_coefs

    def calc_poly_val(self, index):
        x = self.random_vals_X[index]
        return sum(coef * x**n for n, coef in enumerate(self.__polynom_coefs))

    def get_poly_val(self, index):
        return self.calc_poly_val(index)

    # sum all players poly of x_player_index
    def get_players_sum_Xi_val(self):
        return (sum(player.get_poly_val(self.__player_index) for player in dealer.players))    


