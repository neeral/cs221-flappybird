#! /usr/bin/env python3

"""Flappy Bird, implemented using Pygame."""

from init import *
from game_objects import *
import agent
import search
import QLearning
from collections import Counter
import sys

import time
import timeit

def main(maxGames, gamma, epsilon, bird_has_learned, q_values_counter):
    """The application's entry point.

    If someone executes this module (instead of importing it, for
    example), this function is called.
    """
    counter = 0
    QL = QLearning.Qvalue(gamma)

    if bird_has_learned ==1:
        QL.Q = q_values_counter

    reward = 10
    reward_die = -1000
    reward_pass = 1
    reward_ingap = 200
    scoreList = []
    avgScore = []

    filename_prefix = './q-attempt-auto-Fn-'
    filename = filename_prefix + str(gamma) + '-' + str(epsilon)
    
    if bird_has_learned ==1:
        filename = filename + '-Run.txt'
    else:
        filename = filename + '-Train.txt'

    f = open(filename, 'w+')

    pygame.init()

    while counter < maxGames:

        episode = []

        display_surface = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption('Pygame Flappy Bird')

        clock = pygame.time.Clock()
        score_font = pygame.font.SysFont(None, 32, bold=True)  # default font
        images = load_images()

        # the bird stays in the same x position, so bird.x is a constant
        # center bird on screen
        bird = Bird(50, int(WIN_HEIGHT/2 - Bird.HEIGHT/2), 2,
                    (images['bird-wingup'], images['bird-wingdown']))

        pipes = deque()

        nextPipes = deque()
        agent_y = None
        agent_status = True
        time_taken = []
        ActionList = []
        lastPipes = 0
        fcounter = 0


        frame_clock = 0  # this counter is only incremented if the game isn't paused
        score = 0
        done = paused = False
        while not done:
            clock.tick(FPS)

            # Handle this 'manually'.  If we used pygame.time.set_timer(),
            # pipe addition would be messed up when paused.
            if not (paused or frame_clock % msec_to_frames(PipePair.ADD_INTERVAL)):
                pp = PipePair(images['pipe-end'], images['pipe-body'])
                pipes.append(pp)
                nextPipes.append(pp)

            for e in pygame.event.get():
                if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
                    done = True
                    break
                elif e.type == KEYUP and e.key in (K_PAUSE, K_p):
                    paused = not paused
                elif e.type == MOUSEBUTTONUP or (e.type == KEYUP and
                        e.key in (K_UP, K_RETURN, K_SPACE)):
                    bird.msec_to_climb = Bird.CLIMB_DURATION


            ###############################  RL CODE ####################################################


            ######################################################################################################
            ####### QLearning
            ######################################################################################################
            if (fcounter%(FPS/4) == 0):
                newState = QLearning.QLState(bird,pipes)
                if bird_has_learned==1:
                    newAction = QLearning.epsilon_greedy(QL, 0.0, newState)
                else:
                    newAction = QLearning.epsilon_greedy(QL, min(0.1, epsilon/float(counter+1)), newState)
                if newAction == 'jump':
                    bird.msec_to_climb = Bird.CLIMB_DURATION
                episode.append((newState.short(),newAction))
            fcounter+=1

            if paused:
                continue  # don't draw anything

            # check for collisions
            pipe_collision = any(p.collides_with(bird) for p in pipes)
            if pipe_collision or 0 >= bird.y or bird.y >= WIN_HEIGHT - Bird.HEIGHT:
                done = True

            for x in (0, WIN_WIDTH / 2):
                display_surface.blit(images['background'], (x, 0))

            ############################## display predicted path ###################

            # for state in predState:
            #     display_surface.blit(state.bird.image,state.bird.rect)
            # predState.pop(0)
            ##########################################################################
            while pipes and not pipes[0].visible:
                pipes.popleft()

            for p in pipes:
                p.update()
                display_surface.blit(p.image, p.rect)

            bird.update()
            display_surface.blit(bird.image, bird.rect)

            # update and display score
            for p in pipes:
                if p.x + PipePair.WIDTH < bird.x and not p.score_counted:
                    score += 1
                    p.score_counted = True
                    nextPipes.popleft()

            score_surface = score_font.render(str(score), True, (255, 255, 255))
            score_x = WIN_WIDTH/2 - score_surface.get_width()/2
            display_surface.blit(score_surface, (score_x, PipePair.PIECE_HEIGHT))

            pygame.display.flip()
            frame_clock += 1

        if bird_has_learned != 1:            
            for i in range(len(episode)-2):
                if episode[i+1][0][1] >= 0 and episode[i+1][0][1] <= 3:
                    QL.update(episode[i][0],episode[i][1],reward_ingap,episode[i+1][0],counter)
                else:
                    QL.update(episode[i][0],episode[i][1],reward,episode[i+1][0],counter)

            QL.update(episode[len(episode)-2][0],episode[len(episode)-2][1],reward_die,episode[len(episode)-1][0],counter)
        print('Game over! Score: %i\tnum states:%i\tnum games:%i' % (score, len(QL.Q), counter))#        print(QL.Q)
        counter+=1
        if len(avgScore) == 0:
            avgScore.append(score)
        else:
            avgScore.append((avgScore[-1]*(counter-1)+ score)/float(counter))
        scoreList.append(score)


    pygame.quit()
    print(scoreList)
    print(avgScore)
    f.write(str(avgScore))
    f.write('\n')
    f.write(str(scoreList))
    f.write('\n')
    f.write(str(QL.Q))
    f.write('\n')
    
    return QL.Q

if __name__ == '__main__':
    # If this module had been imported, __name__ would be 'flappybird'.
    # It was executed (e.g. by double-clicking the file), so call main.

    maxGames = 2#000
    gamma = 0.6
    epsilon = float(sys.argv[1])

    print 'now running for training: main(maxGames=%d, gamma=%f, epsilon=fn(%f), learning=0, None)' % (maxGames, gamma, epsilon)
    Qvalues = main(maxGames, gamma, epsilon, 0, None)
    maxGames = 2#500
    print 'now running for test: main(maxGames=%d, gamma=%f, epsilon=fn(%f), learning=1, Qvalues)' % (maxGames, gamma, epsilon)
    main(maxGames, gamma, epsilon, 1, Qvalues)
