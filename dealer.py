import random
from math import log2
import re
from node import Node
from scipy.interpolate import lagrange
from shared import PLAYERS
from player import Player


class Dealer:
    def __init__(self, num_of_PLAYERS):
        self.__num_of_PLAYERS = num_of_PLAYERS
        self.tree = {}

    def get_random_X_vals(self):
        return list(random.sample(range(1, 50), self.__num_of_PLAYERS))

    def get_sec_val_sum(self, X, PX):
        return int(round(lagrange(X, PX)(0)))

    # calc E_TA without dividing by T as we'll compare these values to find the best attr A among all
    # A is the set of possible attr values for A attr
    # Ta is an array holds Ta values for each a
    # Tac is a 2D-aaray holds Tac values for each a and category value c
    def calc_E_TA(self, A, Ta, Tac):
        E_TA = (-sum(sum(abs(Tac[attr][cat]) * abs(log2(Tac[attr][cat])) for cat in Tac) for attr in A)) + (
            sum(abs(Ta[attr]) * log2(abs(Ta[attr])) for attr in A))
        return E_TA

    def build_tree(self):
        R = {
            'Age': ['<=20', '21-25', '26-35', '36+'],
            'Weight': ['<=50', '51-65', '66-80', '81-95', '95+'],
            'Height': ['<=1.6', '1.61-1.7', '1.71-1.8', '1.81+'],
            'OFH': ['yes', 'no'],
            'FAVC': ['yes', 'no'],
            'CAEC': ['0', '1', '2', '3'],
            'FAF': ['0', '1', '2', '3'],
            'Gender': ['Male', 'Female'],
        }
        C = ['Insufficient', 'Normal', 'Overweight', 'Obesity']
        self.tree = self.ID3(R, C, None)

    # R: Set of attributes to be considered
    # O: Set of objects to be considered
    # C = {c1,c2,...,ck}: Set of possible categories.
    def ID3(self, R, C, node):
        if not node:
            node = Node()

        # first cond: check if all objects in O have the same category ci
        # we do it by check is_one_category in each player for each category.
        # if all players return that is_one_category == cat
        #  => node.value = cat
        cat = ''
        for player in PLAYERS:
            player_cat = player.is_one_category(node.attrs)
            if player_cat is not None:
                if cat == '':
                    cat = player_cat
                elif cat != player_cat:
                    cat = ''
                    break
        if cat != '':
            node.value = cat
            return node

        if len(R) == 0:
            # second condition
            # Return a leaf node whose category is set to the dominant category among the objects in O
            # we calc the dominant by using secret sum af all players get_c_sum
            node.value = self.find_max_category(node.attrs, C)
            return node

        # else -  Determine the attribute A that best classifies the objects in O
        # and assign it as the test attribute for the current tree node
        # ask from each player to calc Ta and Tac and sum the other PLAYERS values by SSS
        # the dealer will find the sum of the ss and find the optimal A using calc_E_TA.
        # it will then send it back to all PLAYERS -> to divide their data accordingly
        # then - Create a new node for every possible value ai of A
        # and recursively call this method on it with R0 = (R - {A}) and O' = O(ai) /*

        max_attr = ''
        max_E_TA = 0
        for attr, vals in R:
            Ta = {}
            Tac = {}
            for ai in vals:
                node_attrs = node.attrs
                node_attrs[attr] = ai
                Ta[ai] = self.get_Tai(node_attrs)
                Tac[ai] = {}
                for ci in C:
                    Tac[ai][ci] = self.get_Tac(node_attrs, ci)
            curr_E_TA = self.calc_E_TA(self, R[attr], Ta, Tac)
            if curr_E_TA > max_E_TA:
                max_E_TA = curr_E_TA
                max_attr = attr
        node.value = max_attr
        node.children = {}
        for attr_value in R[node.value]:
            child = Node()
            child.attrs = node.attrs
            child.attrs[max_attr] = attr_value
            if self.get_Tai(child.attrs) == 0:
                child.value = self.find_max_category(node.attrs, C)
                node.children[attr_value] = child
            else:
                new_R = R
                new_R.remove(max_attr)
                node.children[attr_value] = self.ID3(new_R, C, child)

    def find_max_category(self, attrs, C):
        max_cat = ''
        max_value = 0
        for cat in C:
            X_vals = self.get_random_X_vals()
            enc_val = []
            for i in range(len(PLAYERS)):
                enc_val.append(i)
                enc_val[i] = PLAYERS[i].get_Tac(attrs, cat, X_vals[i])
            curr_cat_value = self.get_sec_val_sum(X_vals, enc_val)
            if curr_cat_value > max_value:
                max_value = curr_cat_value
                max_cat = cat
        return max_cat

    def get_Tai(self, attrs):
        X_vals = self.get_random_X_vals()
        enc_Tai = []
        for i in range(len(PLAYERS)):
            enc_Tai.append(i)
            enc_Tai[i] = PLAYERS[i].get_Tai(attrs, X_vals[i])
        return self.get_sec_val_sum(X_vals, enc_Tai)

    def get_Tac(self, attrs, ci):
        X_vals = self.get_random_X_vals()
        enc_Tai_ci = []
        for i in range(len(PLAYERS)):
            enc_Tai_ci.append(i)
            enc_Tai_ci[i] = PLAYERS[i].get_Tac(attrs, ci, X_vals[i])
        return self.get_sec_val_sum(X_vals, enc_Tai_ci)

    def predict(self, attrs):
        return self.__predict(self.tree, attrs)

    def __predict(self, node, attrs):
        if len(node.children) == 0:
            return node.value
        return self.__predict(node.children[attrs[node.value]], attrs)

    def main_loop(self):
        pass


def main():
    dealer = Dealer(4)
    for i in range(4):
        PLAYERS.append(Player(i, 4))
    dealer.main_loop()
    print("Server created")


if __name__ == "__main__":
    main()
