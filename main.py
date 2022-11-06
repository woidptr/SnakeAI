import os.path

import neat.nn
import pygame
from pygame.math import Vector2
import random
import sys

from menu import menu


class Snake():
    def __init__(self):
        self.body = [Vector2(7, 10), Vector2(6, 10), Vector2(5, 10)]
        self.direction = Vector2(1, 0)
        self.x = None
        self.y = None
        self.size = len(self.body[:-1])
        self.new_block = False

    def draw_snake(self):
        for block in self.body:
            block_rect = pygame.Rect(block.x * cell_size, block.y * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, (114, 137, 218), block_rect)
            self.x = block_rect.x
            self.y = block_rect.y

    def move_snake(self):
        if self.new_block:
            self.new_block = False
            body_copy = self.body[:]
        else:
            body_copy = self.body[:-1]
        body_copy.insert(0, body_copy[0] + self.direction)
        self.body = body_copy[:]

    def forward(self):
        pass


class Fruit():
    def __init__(self):
        self.reposition()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, (255, 255, 255), fruit_rect)

    def reposition(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)


class Game():
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()
        self.failed = False

    def update(self):
        self.snake.move_snake()
        #self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.reposition()
            self.snake.new_block = True

            return True
        return False

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.failed = True

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.failed = True


def vision(game):
    snake = game.snake
    fruit = game.fruit

    # Border vision
    border_n = snake.body[0].y - 1
    border_s = cell_number - snake.body[0].y
    border_w = snake.body[0].x - 1
    border_e = cell_number - snake.body[0].x

    # Tail vision
    tail_n = snake.body[0].y - 1

    # Direction vision
    direction_n = 1 if snake.direction == Vector2(0, 1) else 0
    direction_s = 1 if snake.direction == Vector2(0, -1) else 0
    direction_w = 1 if snake.direction == Vector2(-1, 0) else 0
    direction_e = 1 if snake.direction == Vector2(1, 0) else 0

    # Size vision
    size = len(snake.body[:-1])

    # Fruit distance
    fruit_dist = snake.body[0].x


    return [border_n, border_s, border_w, border_e,
            direction_n, direction_s, direction_w, direction_e,
            fruit_dist]


def controls(game, output):
    if max(output) == output[0]:
        game.snake.direction = Vector2(0, 1)
    if max(output) == output[1]:
        game.snake.direction = Vector2(0, 1)
    if max(output) == output[2]:
        game.snake.direction = Vector2(0, 1)


def run(genomes, config):
    global init, generation

    generation += 1

    pause = False

    if not init:
        init = True
        menu(screen)

    games = []
    nets = []

    for i, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        g.fitness = 0

        games.append(Game())

    font = pygame.font.SysFont("Arial", 20)
    #game = Game()

    font = pygame.font.Font(os.path.join("resources", "fonts", "Monocraft.otf"), 20)

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
            if event.type == SCREEN_UPDATE:
                if not pause:
                    for j, game in enumerate(games):
                        game.update()

                        if game.check_collision():
                            genomes[j][1].fitness += 5      # increase the fitness (fruit eaten)

                        if game.failed:
                            genomes[j][1].fitness -= 10     # lower the fitness (fail)
                            games.pop(j)
                            nets.pop(j)

                # Controls
                    for i, game in enumerate(games):
                        output = nets[i].activate(vision(game))

                        if max(output) == output[0]:
                            game.snake.direction = Vector2(0, 1)    # Up
                        elif max(output) == output[1]:
                            game.snake.direction = Vector2(0, -1)   # Down
                        elif max(output) == output[2]:
                            game.snake.direction = Vector2(-1, 0)   # Left
                        elif max(output) == output[3]:
                            game.snake.direction = Vector2(1, 0)    # Right

        if not pause:
            screen.fill((66, 69, 73))

            # Rendering text
            label = font.render(f"Generation: {generation}", True, (255, 255, 255))
            screen.blit(label, (5, 5))

            score = font.render(f"Score: 0", True, (255, 255, 255))
            screen.blit(score, (5, 25))

        # score_label = font.render("Score: 0", True, (196, 196, 196))
        # screen.blit(score_label, (50, 50))

        for game in games:
            game.draw_elements()

        if len(games) == 0:
            break

        pygame.display.update()
        clock.tick(60)


# Entry point
if __name__ == "__main__":
    # Setting up NEAT
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, config_path)

    p = neat.Population(config)

    # Setting up pygame
    pygame.init()
    cell_size = 20
    cell_number = 30
    screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
    pygame.display.set_caption("Snake AI")
    clock = pygame.time.Clock()

    # Global vars
    init = False
    generation = 0

    # game = Game()
    # fruit = Fruit()
    # snake = Snake()

    SCREEN_UPDATE = pygame.USEREVENT
    pygame.time.set_timer(SCREEN_UPDATE, 150)

    p.run(run)
