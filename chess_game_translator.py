import numpy as np
import pandas as pd

import chess
import chess.pgn as pgn

import time

class chess_translator():
    def __init__(self):
        pass
    
    def read_game_data(self, max_games_to_read):
        with open("lichess_db_1_decompresed.pgn", "r") as fp:
            count = sum(1 for line in fp)
        
        num_games = int(count/18)
        self.num_games = min(num_games,max_games_to_read)
        self.Games = np.array([0]*min(num_games,max_games_to_read), dtype=np.ndarray)
        with open("lichess_db_1_decompresed.pgn") as raw_data:
            for i in range(min(num_games,max_games_to_read)):
                self.Games[i] = pgn.read_game(raw_data)
    
    def bitboards_to_array(self, bb: np.ndarray) -> np.ndarray: # i did not write this initaly got it from here -> https://chess.stackexchange.com/questions/29294/quickly-converting-board-to-bitboard-representation-using-python-chess-library
        bb = np.asarray(bb, dtype=np.uint64)[:, np.newaxis]
        s = 8 * np.arange(7, -1, -1, dtype=np.uint64)
        b = (bb >> s).astype(np.uint8)
        b = np.unpackbits(b, bitorder="little")
        return b #.reshape(-1, 8, 8) this portion is modified from the origonal so that the input is one vector
    
    def translate_board(self, board): # i did not write this initaly got it from here -> https://chess.stackexchange.com/questions/29294/quickly-converting-board-to-bitboard-representation-using-python-chess-library
        black, white = board.occupied_co

        bitboards = np.array([
            black & board.pawns,
            black & board.knights,
            black & board.bishops,
            black & board.rooks,
            black & board.queens,
            black & board.kings,
            white & board.pawns,
            white & board.knights,
            white & board.bishops,
            white & board.rooks,
            white & board.queens,
            white & board.kings,
        ], dtype=np.uint64)

        return self.bitboards_to_array(bitboards)
    
    def main(self):
        num_games_read = 1000

        start = time.time()
        self.read_game_data(num_games_read)
        num_games_read = self.num_games

        total_num_positions = 0
        for i in range(num_games_read):
            total_num_positions += sum(1 for _ in self.Games[i].mainline_moves())
        
        positions = np.zeros((total_num_positions,768)) # 12*64 = 768 dont forget
        outcomes = np.zeros((total_num_positions,2))

        n = 0
        for i in range(len(self.Games)):
            board = self.Games[i].board() # im not giving it the starting state as a position as it will never need to evaluate that as a potential move

            for move in self.Games[i].mainline_moves():
                board.push(move)

                positions[n] = self.translate_board(board)
                out_str = self.Games[i].headers["Result"]
                outcomes[n][0] = float(out_str[0])
                outcomes[n][1] = float(out_str[2])
                n += 1
        
        pd.DataFrame(positions).to_csv("bot_translated_data/translated_positions_big.csv", index=False, header=False)
        pd.DataFrame(outcomes).to_csv("bot_translated_data/outcomes_big.csv", index=False, header=False)
        end = time.time()

        print(f"time taken was: {end - start}\navg time per game was: {(end - start)/num_games_read}\n")


test = chess_translator()
test.main()