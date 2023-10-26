#!/usr/bin/python3

import numpy as np
import argparse

class TicTacToe:
	def __init__(self, board=None, player=1) -> None:
		if board is None:
			self.board = self.init_board()
		else:
			self.board = board
		self.player = player

	def init_board(self):
		return np.array([[0,0,0],[0,0,0],[0,0,0]])

	def print_board(self):
		print (self.board)

	def eval_win(self): # return 0 if no win, 100 if player 1 wins, -100 if player 2 wins
		# Horizontal
		for i in range(3):
			if self.board[i][0] == self.board[i][1] == self.board[i][2] != 0:
				return self.board[i][0] * 100
		# Vertical
		for i in range(3):
			if self.board[0][i] == self.board[1][i] == self.board[2][i] != 0:
				return self.board[0][i] * 100
		# Diagonal
		if self.board[0][0] == self.board[1][1] == self.board[2][2] != 0:
			return self.board[0][0] * 100
		if self.board[0][2] == self.board[1][1] == self.board[2][0] != 0:
			return self.board[0][2] * 100
		return 0
	
	def areMovesLeft(self): # Check if any valid moves are left
		for i in range(3):
			for j in range(3):
				if self.board[i][j] == 0:
					return True
		return False

	def play_game(self):
		# Had toruble getting the minmax to paly nice with the fact that we swap players. It works well when the player is 1
		# So we are going to pretend that player 1 is always playing. But to get it to play -1's turn, we invert the board
		# This works until it doesn't. That is to say it incorrectly inverts the board when the first player is -1. So extra logic is added to fix that.

		currentPlayer = self.player # This variable doesn't actually matter (to the minmax calculation), it's just to keep track of who's turn it is when printing it to the screen
		inverted = False # We need to make sure that the number of inversions is even. Less we leave the board inverted at the end of the game.

		if(self.player == -1):
			self.board = -1 * self.board

		while(self.eval_win() == 0 and self.areMovesLeft()): # While there is no winner, keep playing
			#print("Current board: \n{}".format(self.board))
			self.play_move(currentPlayer) 
			currentPlayer = -1 * currentPlayer
			self.board = -1 * self.board
			if(inverted):
				inverted = False
			else:
				inverted = True
			#print("Inverted: {}".format(inverted))

		# Logic to handle the case where the first player is -1 or if the board is accidentally left inverted.
		if(inverted):
			self.board = -1 * self.board
		if(self.player == -1):
			self.board = -1 * self.board

		winner = int(self.eval_win() / 100) # Sending this as an int just to be safe
		
		return self.board, winner
	
	def play_move(self, player):
		# Play a move for the sepcified player
		#print("Player {} is playing".format(player))
		# There has to be a valid move at this point as this is checked in play_game()
		bestValye = -1000
		bestX = -1
		bestY = -1

		for i in range(3):
			for j in range(3):
				if self.board[i][j] == 0: # Find all valid moves
					self.board[i][j] = 1 # Make the move
					moveValue = self.minimax(-1, 0)
					self.board[i][j] = 0 # Undo the move
					if moveValue > bestValye:
						bestX = i
						bestY = j
						bestValye = moveValue
		self.board[bestX][bestY] = 1

	def minimax(self, player, depth):
		# Check for win in current state
		score = self.eval_win()
		if score == player * 100:
			return score + depth
		if score == -player * 100:
			return score - depth
		if (self.areMovesLeft() == False):
			return 0
		
		if(player > 0): # Maximizer move
			bestValue = -1000

			for i in range(3):
				for j in range(3):
					if self.board[i][j] == 0:
						self.board[i][j] = player
						value = self.minimax(-player, depth+1)
						value = value
						self.board[i][j] = 0
						bestValue = max(bestValue, value)
			return bestValue
		else: # Minimizer move
			bestValue = 1000

			for i in range(3):
				for j in range(3):
					if self.board[i][j] == 0:
						self.board[i][j] = player
						value = self.minimax(-player, depth+1)
						value = value
						self.board[i][j] = 0
						bestValue = min(bestValue, value)
			return bestValue


def load_board( filename ):
	return np.loadtxt( filename)

def main():
	parser = argparse.ArgumentParser(description='Play tic tac toe')
	parser.add_argument('-f', '--file', default=None, type=str ,help='load board from file')
	parser.add_argument('-p', '--player', default=1, type=int, choices=[1,-1] ,help='player that playes first, 1 or -1')
	args = parser.parse_args()

	board = load_board(args.file) if args.file else None
	# Randomly generate a testcase array but make sure it's valid
	# 0 = empty, 1 = player 1, -1 = player 2
	testcase = np.array ([[0,0,0],[0,0,0],[0,0,0]])
	# add 1 random 1's and 1 random -1's
	testcase[np.random.randint(0,3),np.random.randint(0,3)] = 1
	# make sure the second move doesn't overwrite the first
	while True:
		x = np.random.randint(0,3)
		y = np.random.randint(0,3)
		if testcase[x,y] == 0:
			testcase[x,y] = -1
			break


	print("Initial board: \n{}".format(testcase))
	ttt = TicTacToe(testcase, args.player)
	b,p = ttt.play_game()
	print("final board: \n{}".format(b))
	print("winner: player {}".format(p))

if __name__ == '__main__':
	main() 