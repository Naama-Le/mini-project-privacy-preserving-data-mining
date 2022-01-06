import random
from math import log2
from node import Node
from scipy.interpolate import lagrange
from shared import PLAYERS
import copy


class Dealer:
    def __init__(self, num_of_PLAYERS):
        self.__num_of_PLAYERS = num_of_PLAYERS
        self.__tree = Node()

    def get_random_X_vals(self):
        return list(random.sample(range(1, 50), self.__num_of_PLAYERS))

    def get_sec_val_sum(self, X, PX):
        return int(round(lagrange(X, PX)(0)))

    # calc E_TA without dividing by T as we'll compare these values to find the best attr A among all
    # A is the set of possible attr values for A attr
    # Ta is an array holds Ta values for each a
    # Tac is a 2D-aaray holds Tac values for each a and category value c
    def calc_E_TA(self, A, Ta, Tac):
        E_TA = 0
        for ai in A:
            for cj in Tac[ai].keys():
                T_ai_cj = Tac[ai][cj]
                if T_ai_cj != 0:
                    E_TA -= T_ai_cj * log2(T_ai_cj)
            T_ai = Ta[ai]
            if T_ai != 0:
                E_TA += T_ai * log2(T_ai)
        return E_TA

    def build_tree(self, R, C):
        self.__ID3(R, C, self.__tree)

    # R: Set of attributes to be considered
    # C = {c1,c2,...,ck}: Set of possible categories.
    def __ID3(self, R, C, node):
        # first cond: check if all objects in O have the same category ci
        # we do it by check is_one_category in each player for each category.
        # if all players return that is_one_category == cat
        #  => node.value = cat
        cat = ''
        for player in PLAYERS:
            player_cat = player.is_one_category(node.attrs)
            if player_cat is not None:
                if player_cat == '':
                    continue
                elif cat == '':
                    cat = player_cat
                elif cat != player_cat:
                    cat = ''
                    break
            else:
                break
        if (cat != ''):
            node.value = cat
            return

        if (len(R) == 0):
            # second condition
            # Return a leaf node whose category is set to the dominant category among the objects in O
            # we calc the dominant by using secret sum af all players get_c_sum
            node.value = self.find_max_category(node.attrs, C)
            return

        # else -  Determine the attribute A that best classifies the objects in O
        # and assign it as the test attribute for the current tree node
        # ask from each player to calc Ta and Tac and sum the other PLAYERS values by SSS
        # the dealer will find the sum of the ss and find the optimal A using calc_E_TA.
        # then - Create a new node for every possible value ai of A
        # and recursively call this method on it with R0 = (R - {A})

        best_attr = ''
        min_E_TA = float('inf')
        for attr, vals in R.items():
            Ta = {}
            Tac = {}
            for ai in vals:
                node_attrs = copy.deepcopy(node.attrs)
                node_attrs[attr] = ai
                Ta[ai] = self.get_Tai(node_attrs)
                Tac[ai] = {}
                for ci in C:
                    Tac[ai][ci] = self.get_Tac(node_attrs, ci)

            curr_E_TA = self.calc_E_TA(R[attr], Ta, Tac)
            if (curr_E_TA < min_E_TA):
                min_E_TA = curr_E_TA
                best_attr = attr
        node.value = best_attr
        node.children = {}
        for attr_value in R[node.value]:
            child = Node()
            child.attrs = copy.deepcopy(node.attrs)
            child.attrs[best_attr] = attr_value
            if self.get_Tai(child.attrs) == 0:
                # no matching objects for this attrs' values in the data. set it as a leaf
                child.value = self.find_max_category(node.attrs, C)
                node.children[attr_value] = child
            else:
                # recursivly call ID3 with the reduced R 
                new_R = copy.deepcopy(R)
                new_R.pop(best_attr, None)
                self.__ID3(new_R, C, child)
                node.children[attr_value] = child

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

    def predict(self, attrs, path=None):
        return self.__predict(self.__tree, attrs, path)

    def __predict(self, node, attrs, path=None):
        if path is not None:
            path.append(node.value)
        if node.children is None or len(node.children) == 0:
            return node.value
        return self.__predict(node.children[attrs[node.value]], attrs, path)
