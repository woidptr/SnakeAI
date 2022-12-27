import os.path

import neat.nn
from neat import checkpoint
import pygame
from pygame.math import Vector2
import pickle
import heapq
import sys

from snake import Snake


def controls(snake, output):
    """Controls snake based on the neural network output."""

    if max(output) == output[0]:    # Left
        if snake.direction == Vector2(0, 1):
            snake.direction = Vector2(1, 0)
        elif snake.direction == Vector2(0, -1):
            snake.direction = Vector2(-1, 0)
        elif snake.direction == Vector2(-1, 0):
            snake.direction = Vector2(0, 1)
        elif snake.direction == Vector2(1, 0):
            snake.direction = Vector2(0, -1)
    if max(output) == output[1]:    # Right
        if snake.direction == Vector2(0, 1):
            snake.direction = Vector2(-1, 0)
        elif snake.direction == Vector2(0, -1):
            snake.direction = Vector2(1, 0)
        elif snake.direction == Vector2(-1, 0):
            snake.direction = Vector2(0, -1)
        elif snake.direction == Vector2(1, 0):
            snake.direction = Vector2(0, 1)
    if max(output) == output[2]:    # Forward
        pass


def replay_genome(config, model="model.pkl"):
    global replay

    replay = True

    with open(model, "rb") as f:
        genome = pickle.load(f)
    
    genomes = [(1, genome)]

    run(genomes, config)


def run(genomes, config):
    global init, generation, highscore
    global debug_menu
    global max_fitness, best_genome
    global replay

    generation += 1

    pause = False

    snakes = []
    nets = []
    frames = []

    for id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0
        frames.append(0)

        snakes.append(Snake(screen))

    font = pygame.font.Font(os.path.join("resources", "fonts", "FixelMedium.ttf"), 20)
    debug_font = pygame.font.Font(os.path.join("resources", "fonts", "FixelMedium.ttf"), 15)

    # Game loop
    while len(snakes) > 0:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause = not pause
                if event.key == pygame.K_g:
                    debug_menu = not debug_menu
            if event.type == SCREEN_UPDATE:
                if not pause:
                    screen.fill((66, 69, 73))   # drawing the background

                    for snake in snakes:
                        snake.draw_elements()
                        break

                    screen_rect = screen.get_rect()

                    if replay:
                        replay_label = font.render(f"Replay Mode", True, (255, 255, 255))
                        replay_label_rect = replay_label.get_rect()
                        screen.blit(replay_label, (screen_rect.centerx - (replay_label_rect.width / 2), 5))

                        score = snakes[0].score
                        score_label = font.render(f"Score: {score}", True, (255, 255, 255))
                        screen.blit(score_label, (5, 25))
                    else:
                        # Rendering text
                        generation_label = font.render(f"Generation: {generation}", True, (255, 255, 255))
                        screen.blit(generation_label, (5, 5))

                        highscore_label = font.render(f"Highscore: {highscore}", True, (255, 255, 255))
                        screen.blit(highscore_label, (5, 25))

                    for i, snake in enumerate(snakes):
                        output = nets[i].activate(snake.vision())     # activating the neural network

                        controls(snake, output)      # controls game based on the output from the neural network

                        snake.update()

                        if snake.score > highscore:
                            highscore = snake.score

                        if snake.check_collision():
                            genomes[i][1].fitness += 100      # increase the fitness (fruit eaten)
                            frames[i] = 0
                        
                        frames[i] += 1
                        if frames[i] >= 100 and len(snake.body) <= 5:
                            snake.failed = True

                        if snake.failed:
                            genomes[i][1].fitness -= 1000     # lower the fitness (fail)
                            snakes.pop(i)
                            nets.pop(i)

        pygame.display.update()
        clock.tick(60)


# Entry point
if __name__ == "__main__":
    # Setting up NEAT
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, config_path)

    p = neat.Population(config)     # creating population

    # Setting up pygame
    pygame.init()
    cell_size = 15
    cell_number = 40
    screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
    pygame.display.set_caption("Snake AI")
    clock = pygame.time.Clock()

    # Global vars
    init = False
    generation = 0
    highscore = 0
    max_fitness = 0
    best_genome = 0
    replay = False

    # Ingame settings
    debug_menu = False

    SCREEN_UPDATE = pygame.USEREVENT
    pygame.time.set_timer(SCREEN_UPDATE, 10)

    winner = p.run(run)      # jumping to the run function and getting the winner

    with open("model.pkl", "wb") as f:
        pickle.dump(winner, f)
        f.close()
    
    # replay_genome(config)
