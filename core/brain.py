import os
import random
import pickle
import neat.nn

from entities.snake import Snake
from screens.screen_stack import ScreenStack
from screens.end_screen import EndScreen
# from screens.start_screen import StartScreen


# This class should hold all the values needed for the rendering
class Brain:
    def __init__(self, population, screen, replay: bool = False):
        self.generation = 0
        self.snakes = []
        self.nets = []
        self.frames = []
        self.loop = 0
        self.frames = []
        self.population = population
        self.screen = screen

        self.replay = replay

        # Information
        self.highscore = 0
    
    def init(self):
        # self.population.run(self.eval, 10)
        self.winner = self.population.run(self.eval)

        # Dump the winner into the database
        with open("model.pkl", "wb") as f:
            data = (self.generation, self.population, random.getstate())
            pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)
        
        ScreenStack.push_screen(EndScreen(self.screen, self))

    def eval(self, genomes, config):
        self.genomes = genomes

        self.frames.clear()

        for id, genome in genomes:
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            self.nets.append(net)
            genome.fitness = 0
            self.frames.append(0)

            self.snakes.append(Snake(self.screen))
        
        while len(self.snakes) > 0:
            continue

        self.generation += 1
            
        """ for i, snake in enumerate(self.snakes):
                self.output = self.nets[i].activate(snake.vision())

                snake.tick()

                if snake.score > self.highscore:
                    self.highscore = snake.score

                if snake.check_collision():
                    self.genomes[i][1].fitness += 100      # increase the fitness (fruit eaten)
                    self.frames[i] = 0

                # This antiloop system is an absolute garbage
                self.frames[i] += 1
                if self.frames[i] >= 100 and len(snake.body) <= 5:
                    snake.failed = True

                if snake.failed:
                    self.genomes[i][1].fitness -= 1000     # lower the fitness (fail)
                    self.snakes.pop(i)
                    self.nets.pop(i) """
    
    def tick(self):
        if len(self.snakes) > 0:
            self.loop += 1

            for i, snake in enumerate(self.snakes):
                output = self.nets[i].activate(snake.fruit_vision())

                snake.tick(output)

                """ if self.loop == 1:
                    snake.loop_size = snake.size

                if self.loop == 200:
                    self.loop = 0
                    if snake.size == snake.loop_size:
                        snake.failed = True """

                if snake.score > self.highscore:
                    self.highscore = snake.score

                if snake.check_collision():
                    self.genomes[i][1].fitness += 100      # increase the fitness (fruit eaten)
                    self.frames[i] = 0

                # This antiloop system is an absolute garbage
                self.frames[i] += 1
                if self.frames[i] >= 250 and len(snake.body) <= 5:
                    snake.failed = True

                if snake.failed:
                    self.genomes[i][1].fitness -= 1000     # lower the fitness (fail)
                    self.snakes.pop(i)
                    self.nets.pop(i)