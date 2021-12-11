import numpy
import random
import csv

class Server:
    def __init__(self):
        self.__num_of_players = 4
        self.__random_X_vals = []


    def create_random_X_vals(self):
        self.__random_X_vals = random.sample(range(1,50), self.__num_of_players)

    def get_random_X_vals(self):
        return self.__random_X_vals