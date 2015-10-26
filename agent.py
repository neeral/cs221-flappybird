def bangbang(bird_y, pipe_y, bird_height):
    error = (bird_y + bird_height/2) - pipe_y
    print (bird_y + bird_height/2, pipe_y, error)
    return 1 if error > 0 else 0
