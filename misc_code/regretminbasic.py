import numpy as np

NUM_ACTIONS = 3

class CFRPlayer:
	def __init__(self):
		self.regret_sum = np.zeros(NUM_ACTIONS)
		self.strategy = np.zeros(NUM_ACTIONS)
		self.strategy_sum = np.zeros(NUM_ACTIONS)

	def get_strategy(self):
		normalizing_sum = 0
		for a in range(NUM_ACTIONS): 
			if self.regret_sum[a] > 0:
				self.strategy[a] = self.regret_sum[a]
			else:
				self.strategy[a] = 0
			normalizing_sum += self.strategy[a]
		
		for a in range(NUM_ACTIONS):
			if normalizing_sum > 0:
				self.strategy[a] /= normalizing_sum
			else:
				self.strategy[a] = 1.0/NUM_ACTIONS
			self.strategy_sum[a] += self.strategy[a]

		return self.strategy

	def get_average_strategy(): 
		avg_strategy = np.zeros(NUM_ACTIONS)
		normalizing_sum = 0
		
		for a in range(NUM_ACTIONS):
			normalizing_sum += self.strategy_sum[a]
		for a in range(NUM_ACTIONS):
			if normalizing_sum > 0:
				avg_strategy[a] = self.strategy_sum[a] / normalizing_sum
			else:
				avg_strategy[a] = 1.0 / NUM_ACTIONS
		
		return avg_strategy

class Game:
	def __init__(self, player1, player2):
		self.player1 = player1
		self.player2 = player2


	def play_games(self, num_games = 1000000):
		counter = 0
		utility = np.zeros(NUM_ACTIONS)
		for a in range(NUM_ACTIONS):
				utility[a] = p2[a]
		print('utility = ', utility)
		for i in range(num_games): 
			p1_strategy = p1.get_strategy()
			print('ITERATION: ', counter)
			print('current strategy = ', p1_strategy)
			node_util = 0
			for a in range(NUM_ACTIONS):
				node_util += utility[a]*p1_strategy[a]
			print('ev of current strategy = ', node_util)
			for a in range(NUM_ACTIONS):
				regret = utility[a] - node_util
				print('regret of ', a, ' = ', regret)
				p1.regret_sum[a] += regret
			print ('regret sum = ', p1.regret_sum)
			counter += 1
			print('')


if __name__ == "__main__":
	p1 = CFRPlayer()
	p2 = [-10, 7, 4]
	gameset = Game(p1, p2)
	gameset.play_games(num_games = 10)

