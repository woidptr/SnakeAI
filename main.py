import os.path

import neat.nn
from neat import checkpoint
import pygame
from pygame.math import Vector2
import pickle
import heapq
import sys

# from entities.snake import Snake

from screens.screen_stack import ScreenStack
from screens.start_screen import StartScreen
from screens.hud_screen import HudScreen
from core.brain import Brain
from screens.font_repo import FontRepository


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


def run():
    global init, generation, highscore
    global debug_menu
    global max_fitness, best_genome
    global replay

    generation += 1

    pause = False

    snakes = []
    nets = []
    frames = []

    # Setting up NEAT
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, config_path)

    p = neat.Population(config)     # creating population
    p.add_reporter(neat.Checkpointer(1, 5))

    brain = Brain(p, screen)

    """ for id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0
        frames.append(0)

        snakes.append(Snake(screen)) """

    font = pygame.font.Font(os.path.join("resources", "fonts", "FixelMedium.ttf"), 20)
    debug_font = pygame.font.Font(os.path.join("resources", "fonts", "FixelMedium.ttf"), 15)
    FontRepository.init()

    ScreenStack.push_screen(StartScreen(screen, brain))

    # Game loop
    while True:
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
                # Making the brain tick

                current_screen = ScreenStack.get_current_screen()

                if (isinstance(current_screen, HudScreen)):
                    current_screen.brain.tick()

        # Calling the render function of the current screen
        ScreenStack.get_current_screen().render()

        # Updating the screen in 60 FPS
        pygame.display.update()
        clock.tick(60)


# Entry point
if __name__ == "__main__":
    # Setting up pygame
    pygame.init()
    cell_size = 15
    cell_number = 40
    screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
    pygame.display.set_caption("Snake AI")
    clock = pygame.time.Clock()

    # start_screen(screen)

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
    pygame.time.set_timer(SCREEN_UPDATE, 20)

    run()

    """ winner = p.run(run)      # jumping to the run function and getting the winner

    with open("model.pkl", "wb") as f:
        pickle.dump(winner, f)
        f.close() """
    
    # replay_genome(config)
