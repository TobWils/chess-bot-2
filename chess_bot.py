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

class ChessGamesDataset(Dataset):
    def __init__(self, data_dir, labels_dir):
        self.data = pd.read_csv(data_dir).to_numpy()
        self.labels = pd.read_csv(labels_dir).to_numpy()

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx], self.labels[idx]


class ChessBotModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.LinearReLUstack = nn.Sequential(
            nn.Linear(768, 512),
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Linear(512, 2),
            nn.Softmax(dim=0)
        )
    
    def forward(self, x):
        logits = self.LinearReLUstack(x)
        return logits

class chess_bot():
    def __init__(self, bot_player):
        self.player = bot_player
        self.brain = ChessBotModel()

    def initalise_board(self):
        self.board = chess.Board()
    

    def display_board(self):
        print(self.board)
    
    def train(self):
        device = torch.accelerator.current_accelerator().type if torch.accelerator.is_available() else "cpu"
        print(f"Using {device} device\n")
        self.brain.to(device)

        start = time.time()
        GameData = ChessGamesDataset("bot_translated_data/translated_positions_big.csv","bot_translated_data/outcomes_big.csv")
        end = time.time()

        print(f"time taken was: {end - start}\nlegth of data: {len(GameData)}\n")

        batch_size = 32
        train_size = int(0.8*len(GameData))
        train_set, test_set = torch.utils.data.random_split(GameData,[train_size, len(GameData) - train_size])
        train_loader = DataLoader(train_set, batch_size=batch_size, shuffle=True)
        test_loader = DataLoader(test_set, batch_size=batch_size, shuffle=True)


        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(self.brain.parameters(), lr = 10**(-3))

        num_epochs = 15
        train_losses, test_losses = [], []

        for epoch in range(num_epochs) :
            # Set the model to train
            self.brain.train()
            running_loss = 0.0
            for boards, labels in train_loader:
                boards, labels = boards.to(torch.float32).to(device), labels.to(torch.float32).to(device)
                optimizer.zero_grad()
                outputs = self.brain(boards)
                loss = criterion(outputs, labels)
                loss.backward()
                optimizer.step()
                running_loss += loss.item() * boards.size(0)
            train_loss = running_loss / len(train_loader.dataset)
            train_losses.append(train_loss)

            # validation prtion
            self.brain.eval()
            running_loss = 0.0
            correct_predicts = 0
            num_predicts = 0
            with torch.no_grad():
                for boards, labels in test_loader:
                    boards, labels = boards.to(torch.float32).to(device), labels.to(torch.float32).to(device)
                    outputs = self.brain(boards)
                    num_predicts += outputs.size(0)
                    correct_predicts += sum(1*(torch.argmax(outputs[i]) == torch.argmax(labels[i])) for i in range(outputs.size(0)))
                    loss = criterion(outputs, labels)
                    running_loss += loss.item() * boards.size(0)
            test_loss = running_loss/ len(test_loader.dataset)
            test_losses.append(test_loss)

            # print epoch stats
            print(f"Epoch {epoch+1}/{num_epochs} - Train loss: {train_loss}, Test loss: {test_loss}, Test acuracy: {100*correct_predicts/num_predicts}")

    def main(self):
        self.initalise_board()








test = chess_bot(1)
test.train()
