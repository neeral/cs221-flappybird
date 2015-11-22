#! /usr/bin/env python3

"""Flappy Bird, implemented using Pygame."""

from init import *
from game_objects import *
import agent
import search


import time
import timeit


def main():
    """The application's entry point.

    If someone executes this module (instead of importing it, for
    example), this function is called.
    """

    pygame.init()

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


        ###############################  AGENT CODE ####################################################

        ########################################################################
        #### Bangbang controller
        ########################################################################
        # if agent_y != None and agent_y - bird.y > 10:
        #     agent_status = True
        #
        # if agent_y == None or agent_y - bird.y > 10 or agent_status:
        #     if agent.bangbang(bird.y, nextPipes[0].bottom_pipe_end_y, Bird.HEIGHT) == 1:
        #         bird.msec_to_climb = Bird.CLIMB_DURATION
        #         agent_y = bird.y
        #         agent_status = False


        ########################################################################
        #### UniformCostSearch
        ########################################################################
        

        if  len(pipes)-lastPipes >= 1 or len(ActionList) == 0:
            flappyProblem = agent.FlappySearch(agent.FlappyState(bird, pipes))
            ucs = search.UniformCostSearch()
            start_time = time.time()
            ucs.solve(flappyProblem)
            time_taken.append(time.time() - start_time)
            ActionList = ucs.actions
            predState = ucs.optStates
        currAction = ActionList.pop(0)
        if currAction == 'jump':
            bird.msec_to_climb = Bird.CLIMB_DURATION

        lastPipes = len(pipes)
        ######################################################################################################


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
                print('Times: total=%fs from %i iterations. Average=%fs' % (sum(time_taken), len(time_taken), (sum(time_taken)/len(time_taken))))

        score_surface = score_font.render(str(score), True, (255, 255, 255))
        score_x = WIN_WIDTH/2 - score_surface.get_width()/2
        display_surface.blit(score_surface, (score_x, PipePair.PIECE_HEIGHT))

        pygame.display.flip()
        frame_clock += 1

    print('Game over! Score: %i' % score)
    pygame.quit()


if __name__ == '__main__':
    # If this module had been imported, __name__ would be 'flappybird'.
    # It was executed (e.g. by double-clicking the file), so call main.
    main()
