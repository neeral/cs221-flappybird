#! /usr/bin/env python3

"""Flappy Bird, implemented using Pygame."""

from init import *
from game_objects import *
import agent
import search
import QLearning
from collections import Counter

import time
import timeit

# End of 10000 games
# Counter({((4, 1), 'jump'): 200.49885471754072, ((2, 1), 'jump'): -600.0, ((4, 0), 'jump'): -794.9080960990837, ((4, -1), 'jump'): -799.0, ((2, 0), 'stay'): -1000.0, ((2, -2), 'jump'): -1000.0, ((4, -1), 'stay'): -1000.0, ((2, -1), 'stay'): -1000.0, ((2, -1), 'jump'): -1000.0, ((2, 1), 'stay'): -1000.0, ((2, 0), 'jump'): -1000.0, ((4, 0), 'stay'): -1192.857736741889, ((4, 1), 'stay'): -1799.87417088})

def main():
    """The application's entry point.

    If someone executes this module (instead of importing it, for
    example), this function is called.
    """
    counter = 0 
    maxGames = 500
    QL = QLearning.Qvalue()
    # QL.Q = Counter({((7, 1), 'jump'): 7.857272463519327, ((7, 1), 'stay'): 7.741245285312653, ((9, 1), 'jump'): 6.974197946538579, ((9, 3), 'stay'): 2.4728502681599998, ((4, -2), 'jump'): 1.6991999999999998, ((7, 4), 'jump'): 1.656, ((4, -2), 'stay'): 1.6416, ((9, -2), 'jump'): 1.1663999999999999, ((4, 6), 'jump'): 0.96, ((2, -2), 'stay'): 0.9359999999999999, ((4, 6), 'stay'): 0.9359999999999999, ((2, 7), 'jump'): 0.6, ((7, -2), 'jump'): 0.6, ((5, 4), 'stay'): 0.6, ((9, -1), 'stay'): -80.54968253005099, ((9, 0), 'jump'): -97.33756762163051, ((5, 1), 'jump'): -99.28331164679123, ((-1, 2), 'jump'): -100.7318714988479, ((9, 0), 'stay'): -105.70532659645818, ((5, -1), 'stay'): -116.91400116117696, ((0, 1), 'stay'): -120.35252404640816, ((7, 0), 'stay'): -130.22648878053943, ((5, 1), 'stay'): -133.71809218288863, ((5, 0), 'jump'): -148.9099124363754, ((-3, 1), 'stay'): -154.4543708087079, ((7, 0), 'jump'): -156.57084541134142, ((5, 0), 'stay'): -162.0850310531728, ((4, 1), 'jump'): -171.2932661473332, ((4, 0), 'jump'): -179.7965693246642, ((-1, 2), 'stay'): -182.8699917288755, ((2, 1), 'jump'): -186.62179477555162, ((0, 0), 'jump'): -192.10570383523043, ((4, 0), 'stay'): -193.63696553046788, ((7, -2), 'stay'): -199.4327808, ((-1, 0), 'stay'): -202.9226452728635, ((-3, 0), 'jump'): -209.71099375511983, ((9, 2), 'jump'): -211.6669386541629, ((-1, 1), 'stay'): -216.87973668175724, ((0, 0), 'stay'): -217.877507717578, ((2, 0), 'stay'): -222.32663278238968, ((7, 2), 'stay'): -246.34051949020602, ((2, 1), 'stay'): -246.74031192502184, ((1, 0), 'jump'): -257.4947922630647, ((-1, 1), 'jump'): -257.66471443706297, ((1, 1), 'stay'): -262.18436199797634, ((1, 1), 'jump'): -268.6598699141706, ((-3, 1), 'jump'): -269.1352608305162, ((5, -2), 'stay'): -274.63086373166846, ((0, 1), 'jump'): -282.6151560499842, ((2, 0), 'jump'): -284.34034051851995, ((4, 5), 'jump'): -300.6624, ((9, 2), 'stay'): -345.8247595834438, ((9, -1), 'jump'): -348.47208661575024, ((5, 4), 'jump'): -356.20995840000006, ((2, 6), 'stay'): -359.15999999999997, ((2, 6), 'jump'): -359.4, ((9, 1), 'stay'): -359.8062183772605, ((4, -1), 'stay'): -400.5373431989693, ((7, -1), 'stay'): -415.27671308280446, ((9, 3), 'jump'): -466.85968987967163, ((9, -2), 'stay'): -481.6451347036986, ((-1, 0), 'jump'): -505.0351877771873, ((2, -2), 'jump'): -560.6256, ((4, 5), 'stay'): -576.9926399999999, ((1, 6), 'jump'): -600.0, ((1, 7), 'stay'): -600.0, ((1, -2), 'jump'): -600.0, ((7, -1), 'jump'): -603.1319891393689, ((-3, 0), 'stay'): -638.8181874316656, ((-3, 2), 'stay'): -665.6193584360807, ((4, 1), 'stay'): -706.3801965210189, ((-3, 2), 'jump'): -711.8758049693784, ((5, -1), 'jump'): -736.2986304823946, ((4, 4), 'stay'): -800.0267886182401, ((2, -1), 'stay'): -804.4422906834702, ((1, 0), 'stay'): -838.2476058673772, ((1, -3), 'stay'): -840.0, ((4, -1), 'jump'): -852.0242460274835, ((7, 4), 'stay'): -860.9277966754564, ((7, 3), 'stay'): -865.0574039234211, ((4, 4), 'jump'): -865.9002218495999, ((7, 3), 'jump'): -878.6417536488161, ((2, 5), 'jump'): -888.9302400000001, ((2, 5), 'stay'): -888.9456, ((4, 3), 'stay'): -934.4293978218991, ((1, 6), 'stay'): -936.0, ((2, 4), 'stay'): -956.7407422463999, ((5, 3), 'jump'): -972.1059646694266, ((1, -2), 'stay'): -974.4000000000001, ((1, 5), 'jump'): -974.4000000000001, ((7, 2), 'jump'): -984.7275651949986, ((5, 2), 'jump'): -988.945812073332, ((5, 3), 'stay'): -992.5832848500062, ((5, 2), 'stay'): -995.5538804111354, ((1, 5), 'stay'): -995.904, ((2, -1), 'jump'): -997.512428804205, ((4, 2), 'jump'): -997.6603770175502, ((4, 2), 'stay'): -997.9212840472369, ((4, 3), 'jump'): -997.9374335860218, ((2, 4), 'jump'): -998.88964786176, ((2, 2), 'stay'): -998.9614614721633, ((2, 3), 'jump'): -998.9974237927165, ((2, 2), 'jump'): -998.9982333417834, ((2, 3), 'stay'): -998.9994806521587, ((1, -1), 'jump'): -999.95805696, ((1, 4), 'stay'): -999.9932891136, ((1, 4), 'jump'): -999.998926258176, ((1, 2), 'stay'): -999.9997408910938, ((1, 3), 'jump'): -999.9999725122093, ((1, 2), 'jump'): -999.9999992963126, ((1, 3), 'stay'): -999.999999718525, ((1, -1), 'stay'): -1049.2908903268349})
    
    reward = 10
    reward_die = -1000
    reward_pass = 10
    scoreList = []
    avgScore = []

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
            
            if (fcounter%(FPS/8) == 0):
                newState = QLearning.QLState(bird,pipes)
                if counter%10 == 0:
                    newAction = QLearning.epsilon_greedy(QL,0,newState)
                else:
                    newAction = QLearning.epsilon_greedy(QL,min(0.6,10/math.sqrt(counter+1)),newState)
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

        for i in range(len(episode)-2):
            if episode[i+1][0][1] >= 0 and episode[i+1][0][1] <= 3:
                QL.update(episode[i][0],episode[i][1],reward_pass,episode[i+1][0],counter)
            else:
                QL.update(episode[i][0],episode[i][1],reward,episode[i+1][0],counter)
        QL.update(episode[len(episode)-2][0],episode[len(episode)-2][1],reward_die,episode[len(episode)-1][0],counter)
        print('Game over! Score: %i' % score)
#        print(QL.Q)
        counter+=1

        print(counter)
        if (counter-1) == 0:
            avgScore.append(score)
        elif((counter-1)%10 == 0):
            avgScore.append(avgScore[-1]*(counter-1)/counter + score/counter)
        if (counter-1)%10==0:
            scoreList.append(score)
>>>>>>> Stashed changes


    pygame.quit()
    print(scoreList)
    print(avgScore)


if __name__ == '__main__':
    # If this module had been imported, __name__ would be 'flappybird'.
    # It was executed (e.g. by double-clicking the file), so call main.
    main()
