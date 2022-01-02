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

    def get_idx(self):
        return self.idx

    def get_poly_val(self, x, secret):
        return secret + sum(coef * x ** k for (k, coef) in enumerate(self.__poly, start=1))

    # Let T(ai) be the set of objects whose attrs_dict attribute value is ai
    # attrs_dict is a dict where the keys are attributes and the values are the matching desired values
    def get_Tai(self, attrs_dict, x, stop=False):
        attrs_str, values_str = self.__get_attrs_permutation(attrs_dict)
        t_ai = 0
        try:
            t_ai = self.__db[attrs_str][values_str][0]
        except KeyError:
            pass
        s = self.get_poly_val(x, t_ai)

        if not stop:
            for i in range(len(PLAYERS)):
                if i != self.idx:
                    s += PLAYERS[i].get_Tai(attrs_dict, x, stop=True)
        return s

    def find_category_count(self, attrs_dict, x, s=None, stop=False):
        if s is None:
            s = {}
        attrs_str, values_str = self.__get_attrs_permutation(attrs_dict)
        categories = self.__db[attrs_str][values_str][1]
        for c, val in categories:
            s[c] = self.get_poly_val(x, val)
            if not stop:
                for i in range(len(PLAYERS)):
                    if i != self.idx:
                        s += PLAYERS[i].find_max_category(attrs_dict, x, s, stop=True)
        return s

    def get_possible_values(self, attr):
        return self.__db.get_possible_values(attr)

    # let T(ai,cj) be the set of objects with value of attrs_dict is ai and category cj.
    # attrs_dict is a dict where the keys are attributes and the values are the matching desired values
    def get_Tac(self, attrs_dict, c, x, stop=False):
        attrs_str, values_str = self.__get_attrs_permutation(attrs_dict)

        t_ac = 0
        try:
            t_ac = self.__db[attrs_str][values_str][1][c]
        except KeyError:
            pass

        s = self.get_poly_val(x, t_ac)

        if not stop:
            for i in range(len(PLAYERS)):
                if i != self.idx:
                    s += PLAYERS[i].get_Tac(attrs_dict, c, x, stop=True)
        return s

    def is_one_category(self, attrs_dict):
        attrs_str, values_str = self.__get_attrs_permutation(attrs_dict)
        categories = self.__db[attrs_str][values_str][1]
        if len(categories) == 1:
            return list(categories.keys())[0]
        return None

    def __get_attrs_permutation(self, attrs_dict):
        attrs = list(attrs_dict.keys())
        attrs.sort()
        values = [attrs_dict[attr] for attr in attrs]
        attrs_str = ','.join(attrs)
        values_str = ','.join(values)
        return attrs_str, values_str

    def __generate_poly(self):
        for i in range(self.__num_of_players - 1):
            coefficient = random.randint(-20, 20)
            while coefficient == 0:
                coefficient = random.randint(-20, 20)
            self.__poly.append(coefficient)

    def get_db(self):
        return self.__db
