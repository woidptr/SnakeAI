import pygame
import random
import pickle
import os
from threading import Thread

import neat
from neat.population import Population

from core.brain import Brain

from screens.screen_stack import ScreenStack


class ReplayHandler:
    def __init__(self, screen):
        self.screen = screen

        """ p = neat.Checkpointer.restore_checkpoint(f"neat-checkpoint-32")

        brain = Brain(p, screen)
        thread = Thread(target=brain.init)
        thread.start() """

        if os.path.exists("model.pkl"):
            with open("model.pkl", "rb") as f:
                generation, population, rndstate = pickle.load(f)
                random.setstate(rndstate)

                local_dir = os.path.dirname(__file__)
                config_path = os.path.join(local_dir, "config-feedforward.txt")
                config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                            neat.DefaultStagnation, config_path)

                self.population = Population(config, (population, generation))

                brain = Brain(population, self.screen)
                brain.init()