import random
import socket
from math import log2

from scipy.interpolate import lagrange

from player import Player

players = [Player(4, index) for index in range(4)]


class Dealer:
    def __init__(self, num_of_players):
        self.__num_of_players = num_of_players
        self.__random_X_vals = self.create_random_X_vals()
        self.__players = []
        self.socket = None

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
        return E_TA

    # R: Set of attributes to be considered
    # O: Set of objects to be considered
    # C = {c1,c2,...,ck}: Set of possible categories.
    def ID3(self, R, C):
        # firct cond
        if (len(R) == 0):
            # Return a leaf node whose category is set to the dominant category among the objects in O
            # we calc the dominant by using secret sum af all players get_c_sum
            return
        # second cond - check if all objects in O have the same category ci
        # we do it by calc get_c_sum in each player for each category.
        # if for a specific category ci all players return that get_c_sum(ci) == curr_db length
        #  => if true -> return ci

        # else -  Determine the attribute A that best classifies the objects in O
        # and assign it as the test attribute for the current tree node
        # ask from each player to calc Ta and Tac and sum the other players values by SSS
        # the dealer will find the sum of the ss and find the optimal A using calc_E_TA.
        # it will then send it back to all players -> to divide their data accordingly
        # then - Create a new node for every possible value ai of A
        # and recursively call this method on it with R0 = (R - {A}) and O' = O(ai) /*

    async def connect(self):
        host = "127.0.0.1"
        port = 8000
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, port))
        self.socket.listen(self.__num_of_players)
        for i in range(self.__num_of_players):
            (player_connection, player_address) = self.socket.accept()
            player_connection.send(f'{i},{self.__num_of_players},{self.__random_X_vals[i]}'.encode())
            self.__players.append(player_connection)

    def main_loop(self):
        print(f"Server created with {self.__num_of_players} parties")
        # for i in range(self.__num_of_players):
        #     # (player_connection, player_address) = self.socket.acceept()
        #     # players.append(player_connection)


def main():
    dealer = Dealer(4)
    dealer.connect()
    dealer.main_loop()
    print("Server created")


if __name__ == "__main__":
    main()
