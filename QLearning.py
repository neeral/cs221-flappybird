from init import *
from game_objects import *
from collections import Counter
import random

class QLState:
	NUM_TILES_X = 5
	NUM_TILES_Y = 5
	def __init__(self, bird, pipes):
		self.x = int(pipes[0].x*QLState.NUM_TILES_X/WIN_WIDTH-bird.x*QLState.NUM_TILES_X/WIN_WIDTH)
		self.y = int(pipes[0].bottom_pipe_end_y*QLState.NUM_TILES_Y/WIN_HEIGHT - bird.y*QLState.NUM_TILES_Y/WIN_HEIGHT)

	def short(self):
		return (self.x,self.y)

	def __str__(self):
		return 'Bird({},{}) '.format(self.x, self.y)

	def __lt__(self, other):
		return True

class Qvalue:
	ETA = 0.6
	GAMMA = 0.8

	def __init__(self):
		self.Q = Counter()

	def update(self,state,action,reward,nextState):
		self.Q[(state,action)] = (1-Qvalue.ETA)*self.Q[(state,action)] +\
		 Qvalue.ETA*(reward + Qvalue.GAMMA*max(self.Q[(nextState,'jump')],self.Q[(nextState,'stay')]))

	def policy(self, state):
		if self.Q[(state,'jump')] > self.Q[(state,'stay')]:
			return 'jump'
		else:
			return 'stay'

def epsilon_greedy(Qvalue,epsilon,state):
	if epsilon > random.uniform(0,1):
		return random.choice(['jump','stay'])
	else:
		return Qvalue.policy(state)


