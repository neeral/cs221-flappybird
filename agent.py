from init import *
from game_objects import *

def bangbang(bird_y, pipe_y, bird_height):
	error = (bird_y + bird_height/2) - pipe_y
	print (bird_y + bird_height/2, pipe_y, error)
	return 1 if error > 0 else 0


class FlappySearch:
	def __init__(self,start):
		self.start= start
		self.delta_frames = 1

	# Return the start state.
	def startState(self):
		return self.start

	# Return whether |state| is a goal state or not.
	def isGoal(self, state):
		return WIN_WIDTH == state.bird.x 

	# Return a list of (action, newState, cost) tuples corresponding to edges
	# coming out of |state|.
	def succAndCost(self, state): 
		newStateList = []
		for action in ['jump','stay']:
			if action == 'stay':
				bird = state.bird
				newbird = Bird(bird.x,bird.y,bird.msec_to_climb,(bird._img_wingup, bird._img_wingdown))
				
				newbird.update(self.delta_frames)
				newbird.x += ANIMATION_SPEED * frames_to_msec(self.delta_frames)

				newState = FlappyState(newbird,state.pipes)
				if newState.isCollide():
					newStateList.append((action,newState,float('Inf')))
				else:
					newStateList.append((action,newState,euclideanDistance(state,newState)))

			elif action == 'jump':
				bird = state.bird
				newbird = Bird(bird.x,bird.y,Bird.CLIMB_DURATION,(bird._img_wingup, bird._img_wingdown))
				newbird.update(self.delta_frames)
				newbird.x += ANIMATION_SPEED * frames_to_msec(self.delta_frames)

				newState = FlappyState(newbird,state.pipes)
				if newState.isCollide():
					newStateList.append((action,newState,float('Inf')))
				else:
					newStateList.append((action,newState,euclideanDistance(state,newState)))

		return newStateList


def euclideanDistance(state1,state2):

	return (state1.bird.x-state2.bird.x)**2 + (state1.bird.y-state2.bird.y)**2


class FlappyState:
	def __init__(self,bird,pipes):
		self.bird = bird
		self.pipes = pipes  # queue of pipe pairs objects

	def isCollide(self):
		for pipePair in self.pipes:
			x = self.bird.x
			y = self.bird.y
			# pipePair.bottom_pipe_end_y
			# pipePair.top_pipe_end_y
			# PipePair.WIDTH
			# pipePair.x
			w = WIN_WIDTH
			h = WIN_HEIGHT

			if x + Bird.WIDTH >=pipePair.x and x <= pipePair.x+ PipePair.WIDTH:
				if y <= 0 or y + Bird.HEIGHT >= w:
					return True
				elif y <= pipePair.top_pipe_end_y or y + Bird.HEIGHT>= pipePair.bottom_pipe_end_y:
					return True		
		return False



 
		





