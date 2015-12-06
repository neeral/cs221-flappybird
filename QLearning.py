from init import *
from game_objects import *
from collections import Counter
import random

class QLState:
	NUM_TILES_X = 40
	NUM_TILES_Y = 40
	def __init__(self, bird, pipes):
		self.x = int(pipes[0].x*float(QLState.NUM_TILES_X)/float(WIN_WIDTH)-bird.x*float(QLState.NUM_TILES_X)/float(WIN_WIDTH))
		self.y = int(pipes[0].bottom_pipe_end_y*float(QLState.NUM_TILES_Y)/float(WIN_HEIGHT) - bird.y*float(QLState.NUM_TILES_Y)/float(WIN_HEIGHT))

	def short(self):
		return (self.x,self.y)

	def __str__(self):
		return 'Bird({},{}) '.format(self.x, self.y)

	def __lt__(self, other):
		return True

class Qvalue:
	# ETA = 0.6
	GAMMA = 1.0

	def __init__(self, gamma):
		self.Q = Counter()
		if gamma is not None:
		    self.GAMMA = gamma

	def update(self,state,action,reward,nextState,N):
		# if reward!= -1000:
		# 	reward = 100/(abs(state[1])+1)
		ETA = 1/math.sqrt(N+1)
		self.Q[(state,action)] = (1-ETA)*self.Q[(state,action)] +\
		 ETA*(reward + Qvalue.GAMMA*max(self.Q[(nextState,'jump')],self.Q[(nextState,'stay')]))

	def policy(self, state):
		if self.Q[(state,'jump')] > self.Q[(state,'stay')]:
			return 'jump'
		else:
			return 'stay'


def epsilon_greedy(Qvalue,epsilon,state):
	if epsilon > random.uniform(0,1):
		return random.choice(['jump','stay'])
	else:
		return Qvalue.policy(state.short())


