from init import *
from game_objects import *

def bangbang(bird_y, pipe_y, bird_height):
	error = (bird_y + bird_height/2) - pipe_y
	return 1 if error > 0 else 0


class FlappySearch:
	def __init__(self,start):
		self.start = start
		self.delta_frames = 1

	# Return the start state.
	def startState(self):
		return self.start

	# Return whether |state| is a goal state or not.
	def isGoal(self, state):
		return WIN_WIDTH <= state.bird.x

	# Return a list of (action, newState, cost) tuples corresponding to edges
	# coming out of |state|.
	def succAndCost(self, state):
		newStateList = []
		bird = state.bird
		for action in ['jump','stay']:
			if action == 'stay':
				newbird = Bird(bird.x, bird.y, bird.msec_to_climb, (bird._img_wingup, bird._img_wingdown) )
				newbird.update(self.delta_frames)  # only updates y-position
				newbird.x += ANIMATION_SPEED * frames_to_msec(self.delta_frames)

				newState = FlappyState(newbird, state.pipes)
				if newState.isCollide():
					newStateList.append( (action, newState, float('Inf')) )
				else:
					newStateList.append( (action, newState, euclideanDistance_state(state,newState) \
						+ euclideanDistance((state.bird.x,state.bird.y),(WIN_WIDTH,WIN_HEIGHT/2.)) ) )



			elif action == 'jump':
				newbird = Bird(bird.x, bird.y, Bird.CLIMB_DURATION, (bird._img_wingup, bird._img_wingdown) )
				newbird.update(self.delta_frames)  # only updates y-position
				newbird.x += ANIMATION_SPEED * frames_to_msec(self.delta_frames)

				newState = FlappyState(newbird, state.pipes)
				if newState.isCollide():
					newStateList.append( (action, newState, float('Inf')) )
				else:
					newStateList.append( (action, newState, euclideanDistance_state(state,newState) \
						+ euclideanDistance((state.bird.x,state.bird.y),(WIN_WIDTH,WIN_HEIGHT/2.)) ) )


		return newStateList


def euclideanDistance_state(state1,state2):
	return (state1.bird.x-state2.bird.x)**2 + (state1.bird.y-state2.bird.y)**2

def euclideanDistance(x1,x2):
	return (x1[0]-x2[0])**2 + (x1[1]-x2[1])**2




class FlappyState:
	def __init__(self, bird, pipes):
		self.bird = bird
		self.pipes = pipes  # queue of pipe pairs objects

	def isCollide(self):
		x = self.bird.x
		y = self.bird.y
		if y <= 0 or y + Bird.HEIGHT >= WIN_HEIGHT:
			return True  # gone off the top or bottom of the screen

		for pipePair in self.pipes:
			# pipePair: bottom_pipe_end_y, top_pipe_end_y, x
			# PipePair.WIDTH
			if x + Bird.WIDTH >= pipePair.x and x <= pipePair.x + PipePair.WIDTH and \
			(y <= pipePair.top_pipe_end_y or y + Bird.HEIGHT >= pipePair.bottom_pipe_end_y):
				return True  # collided with a pipe
		return False

	def __str__(self):
		return 'Bird({},{}) with {}ms to climb, {} pipes'.format(self.bird.x, self.bird.y, self.bird.msec_to_climb, len(self.pipes))

	def __lt__(self, other):
		return True
