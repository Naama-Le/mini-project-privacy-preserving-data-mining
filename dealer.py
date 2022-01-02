import random
from math import log2
from node import Node
from scipy.interpolate import lagrange
from shared import PLAYERS, DEALER
from player import Player


class Dealer:
    def __init__(self, num_of_players):
        self.__num_of_players = num_of_players
        self.__random_X_vals = self.create_random_X_vals()

    def create_random_X_vals(self):
        return list(random.sample(range(1, 50), self.__num_of_players))

    def get_random_X_vals(self):
        return self.__random_X_vals

    def get_sec_val_sum(self, X, PX):
        return int(round(lagrange(X, PX)(0)))

    # calc E_TA without dividing by T as we'll compare these values to find the best attr A among all
    # A is the set of possible attr values for A attr
    # Ta is an array holds Ta values for each a
    # Tac is a 2D-aaray holds Tac values for each a and category value c
    def calc_E_TA(self, A, Ta, Tac):
        E_TA = (-sum(sum(abs(Tac[attr][cat]) * abs(log2(Tac[attr][cat])) for cat in Tac) for attr in A)) + (
            sum(abs(Ta[attr]) * log2(abs(Ta[attr])) for attr in A))
        # E_TA = 0
        # for ai in range(p):
        #
        return E_TA;

    # R: Set of attributes to be considered
    # O: Set of objects to be considered
    # C = {c1,c2,...,ck}: Set of possible categories.
    def ID3(self, R, C, node):
        if not node:
            node = Node()
        if len(C) == 1:
            # first cond: check if all objects in O have the same category ci
            # we do it by calc get_c_sum in each player for each category.
            # if for a specific category ci all players return that get_c_sum(ci) == curr_db length
            #  => if true -> return ci
            node.value = C[0];
            return node;
        if (len(R) == 0):
            # second condition
            # Return a leaf node whose category is set to the dominant category among the objects in O
            # we calc the dominant by using secret sum af all players get_c_sum
            node.value = self.find_max_category(node.attrs);
            return node;

        # else -  Determine the attribute A that best classifies the objects in O
        # and assign it as the test attribute for the current tree node
        # ask from each player to calc Ta and Tac and sum the other players values by SSS
        # the dealer will find the sum of the ss and find the optimal A using calc_E_TA.
        # it will then send it back to all players -> to divide their data accordingly
        # then - Create a new node for every possible value ai of A
        # and recursively call this method on it with R0 = (R - {A}) and O' = O(ai) /*
        Ta = []
        Tac = [[]]
        for attr in R:
            for ai in attr:
                Ta[ai] = self.get_Tai(node.attrs, ai)
                for ci in C:
                    Tac[ai][ci] = self.get_Tai_ci(node.attrs, ai, ci)

    def main_loop(self):
        pass


def main():
    DEALER = Dealer(4)
    for i in range(4):
        PLAYERS.append(Player(i, 4))
    DEALER.main_loop()
    print("Server created")


if __name__ == "__main__":
    main()
