import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import chess
import chess.pgn as pgn

import time


class chess_bot():
    def __init__(self, bot_player):
        self.player = bot_player

    def initalise_board(self):
        self.board = chess.Board()
    
    def read_game_data(self, max_games_to_read):
        with open("lichess_db_1_decompresed.pgn", "r") as fp:
            count = sum(1 for line in fp)
        
        num_games = int(count/18)
        self.Games = np.array([0]*min(num_games,max_games_to_read), dtype=np.ndarray)
        with open("lichess_db_1_decompresed.pgn") as raw_data:
            for i in range(min(num_games,max_games_to_read)):
                self.Games[i] = pgn.read_game(raw_data)

    def display_board(self):
        print(self.board)
    
    def main(self):
        self.initalise_board()

        num_games_read = 1000

        start = time.time()
        self.read_game_data(num_games_read)
        end = time.time()

        print(f"time taken was: {end - start}\ntime per game was: {(end - start)/num_games_read}")








test = chess_bot(1)
test.main()
