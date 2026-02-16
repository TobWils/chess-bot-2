import chess
import chess.pgn as pgn
import numpy as np

# i have not done anything with this after copy pasting it from where i wrote it

M = 3
N = 64
K = 2

class data():
    def __init__(self):
        self.x_vals = np.random.rand(M,N)
        self.y_vals = np.random.rand(M,K)

sample = data()

A = np.ones((M,N+1))
#print(A)
#print(sample.x_vals)
A[:, 1:] = sample.x_vals
#print(A)

At = np.transpose(A)
B = np.dot(At,A)

#print(B)

v = np.dot(At,sample.y_vals)

#print()
#print(v)
#print(v[:,0])

sol = np.array([np.linalg.solve(B,v[:,i]) for i in range(K)])
sol = np.transpose(sol)

#print()
#print(sol)
#print(sol[1:])
#print(sol[0])

#print()
predicts = np.dot(sample.x_vals,sol[1:])
#print(predicts)
predicts = predicts + sol[0]
#print(predicts)

errors = (sample.y_vals - predicts)**2

total_error = np.sum(errors)

#print()
print(total_error)