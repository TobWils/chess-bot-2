import chess
import chess.pgn as pgn
import numpy as np


class chess_bot():
    def __init__(self, bot_player):
        self.player = bot_player

    def initalise_board(self):
        self.board = chess.Board()
    
    def read_game_data(self, max_games_to_read):
        with open("lichess_db_1_decompresed.pgn", "r") as fp:
            count = sum(1 for line in fp)
        
        num_games = int(count/18)
        print(num_games)
        self.Games = np.array([0]*num_games, dtype=np.ndarray)
        with open("lichess_db_1_decompresed.pgn") as raw_data:
            for i in range(min(num_games,max_games_to_read)):
                self.Games[i] = pgn.read_game(raw_data)

    def display_board(self):
        print(self.board)
    
    def main(self):
        self.initalise_board()

        self.read_game_data(10)








test = chess_bot(1)
test.main()
