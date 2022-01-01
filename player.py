import random

# import dealer
import socket

from db import DB


# from dealer import Dealer


class Player:

    def __init__(self, num_of_players, idx, x):
        self.idx = idx
        self.__db = DB(idx)
        self.__num_of_players = num_of_players
        self.x = x

        self.__poly = []
        self.__generate_poly()

    def get_num_of_players(self):
        return self.__num_of_players

    def get_poly_val(self):
        return sum(coef * self.x ** k for (k, coef) in enumerate(self.__poly, start=1))

    # sum all players poly of x_player_index
    def get_players_sum_Xi_val(self):
        return
        # return (sum(player.get_poly_val(self.__player_index) for player in dealer.players))

    # Let T(ai) be the set of objects whose A attribute value is ai
    # A is a dict where the keys are attributes and the values are the matching desired values
    def get_Tai(self, A):
        attrs_str, values_str = self.__get_attrs_permutation(A)

        try:
            return self.__db[attrs_str][values_str][0]
        except KeyError:
            return 0

    def __get_attrs_permutation(self, A):
        attrs = list(A.keys())
        attrs.sort()
        values = [A[attr] for attr in attrs]
        attrs_str = ','.join(attrs)
        values_str = ','.join(values)
        return attrs_str, values_str

    # let T(ai,cj) be the set of objects with value of A is ai and category cj.
    # A is a dict where the keys are attributes and the values are the matching desired values
    def get_Tac(self, A, c):
        attrs_str, values_str = self.__get_attrs_permutation(A)

        try:
            return self.__db[attrs_str][values_str][1][c]
        except KeyError:
            return 0

    def get_c_sum(self, c):
        # return (count # of objects with category c in db)
        return

    def __generate_poly(self):
        for i in range(self.__num_of_players):
            coefficient = random.randint(-20, 20)
            while coefficient == 0:
                coefficient = random.randint(-20, 20)
            self.__poly.append(coefficient)

    def connect(self, port=8000):
        port = 8000
        host = "127.0.0.1"
        dealer = socket.socket()
        dealer.connect((host, port))
        print(f"player #{self.idx} created")
