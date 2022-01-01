import socket

from dealer import Dealer
from player import Player

host = "127.0.0.1"
port = 8000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(4)

dealer = Dealer(4,s)
players = Player(4)

