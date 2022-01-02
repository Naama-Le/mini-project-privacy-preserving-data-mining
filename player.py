import random
from db import DB
from shared import PLAYERS


class Player:

    def __init__(self, idx, num_of_players):
        self.idx = idx
        self.__db = DB(idx + 1)
        self.__num_of_players = num_of_players

        self.__poly = []
        self.__generate_poly()
        print(len(PLAYERS))

    # def get_poly_val(self):
    #     # x = self.__get_x_vals()
    #     return sum(coef * x ** k for (k, coef) in enumerate(self.__poly, start=1))

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

    def __get_common_category(self, A):
        attrs_str, values_str = self.__get_attrs_permutation(A)
        categories = self.__db[attrs_str][values_str][1]
        return max(categories, key=categories.get)

    def __get_attrs_permutation(self, A):
        attrs = list(A.keys())
        attrs.sort()
        values = [A[attr] for attr in attrs]
        attrs_str = ','.join(attrs)
        values_str = ','.join(values)
        return attrs_str, values_str

    def get_possible_values(self, attr):
        return self.__db.get_possible_values(attr)

    # let T(ai,cj) be the set of objects with value of A is ai and category cj.
    # A is a dict where the keys are attributes and the values are the matching desired values
    def get_Tac(self, A, c):
        attrs_str, values_str = self.__get_attrs_permutation(A)

        try:
            return self.__db[attrs_str][values_str][1][c]
        except KeyError:
            return 0

    def __generate_poly(self):
        for i in range(self.__num_of_players):
            coefficient = random.randint(-20, 20)
            while coefficient == 0:
                coefficient = random.randint(-20, 20)
            self.__poly.append(coefficient)

    def get_db(self):
        return self.__db

    def __get_x(self):
        pass
