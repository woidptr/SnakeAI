import os.path

import neat.nn
import pygame
from pygame.math import Vector2
import heapq
import math
import random
import sys

from menu import menu


class Snake():
    """
    Snake object
    """

    def __init__(self):
        self.body = [Vector2(7, 10), Vector2(6, 10), Vector2(5, 10)]
        self.direction = Vector2(1, 0)
        self.x = None
        self.y = None
        self.size = len(self.body[:-1])
        self.new_block = False

    def draw_snake(self):
        """
        Drawing snake body
        """

        for i, block in enumerate(self.body):
            block_rect = pygame.Rect(block.x * cell_size, block.y * cell_size, cell_size, cell_size)
            if i == 0:
                pygame.draw.rect(screen, (96, 125, 139), block_rect)
            else:
                pygame.draw.rect(screen, (144, 164, 174), block_rect)
            self.x = block_rect.x
            self.y = block_rect.y
        
        # self.draw_debug_lines()
    
    def draw_debug_lines(self):
        # North border vision
        start_pos = Vector2(self.body[0].x * cell_size + 10, self.body[0].y * cell_size)
        end_pos = Vector2(self.body[0].x * cell_size + 10, 0)
        pygame.draw.line(screen, (87, 242, 135), start_pos, end_pos, 3)

        # South border vision
        start_pos = Vector2(self.body[0].x * cell_size - cell_size + 10, self.body[0].y * cell_size)
        end_pos = Vector2(self.body[0].x * cell_size - cell_size + 10, cell_number * cell_size)
        pygame.draw.line(screen, (87, 242, 135), start_pos, end_pos, 3)

    def move_snake(self):
        """
        Move snake in 'self.direction'
        """
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
    """
    Fruit object
    """

    def __init__(self):
        self.reposition()

    def draw_fruit(self):
        """
        Drawing fruit
        """
        fruit_rect = pygame.Rect(self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, (255, 255, 255), fruit_rect)

    def reposition(self):
        """
        Place fruit in a random spot on the map
        """
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)


class Game():
    """Game object. Combines snake and fruit objects in it."""

    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()
        self.failed = False

    def update(self):
        """Update snake position."""

        self.snake.move_snake()
        #self.check_collision()
        self.check_fail()

    def draw_elements(self):
        """Render elements (snake and fruit)"""
        self.fruit.draw_fruit()
        self.snake.draw_snake()

    def check_collision(self):
        """Check for snake collision with fruit."""

        if self.fruit.pos == self.snake.body[0]:
            self.fruit.reposition()
            self.snake.new_block = True

            return True
        return False

    def check_fail(self):
        """Check if snake is outside the border or inside it's tail."""

        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.failed = True

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.failed = True


def vision(game) -> list:
    """Snake vision or it's sensors."""

    global cell_number

    snake = game.snake      # getting snake object
    fruit = game.fruit      # getting fruit object

    default_dist = cell_number / 2

    # Obstacles vision
    obstacles = [-1, -1, -1]    # Ahead, Left, Right
    dist_body = [-1, -1, -1]    # Ahead, Left, Right

    # border_n = snake.body[0].y - 1
    # border_s = cell_number - snake.body[0].y
    # border_w = snake.body[0].x - 1
    # border_e = cell_number - snake.body[0].x

    # print(f"North border: {border_n}")
    # print(f"South border: {border_s}")
    # print(f"West border: {border_w}")
    # print(f"East border: {border_e}")

    # Tail vision
    for segment in snake.body[1:]:
        if snake.direction == Vector2(0, 1):        # if snake is moving down
            if (snake.body[0].y + default_dist) >= segment.y and snake.body[0].x == segment.x and snake.body[0].y < segment.y:    # looking ahead for the tail segment
                if obstacles[0] == -1 or obstacles[0] > abs(snake.body[0].y - segment.y):
                    obstacles[0] = abs(snake.body[0].y - segment.y)
                    if obstacles[0] == 1:
                        dist_body[0] = 1
            if (snake.body[0].x + default_dist) >= segment.x and snake.body[0].y == segment.y and snake.body[0].x < segment.x:   # looking left for the tail segment
                if obstacles[1] == -1 or obstacles[1] > abs(snake.body[0].x - segment.x):
                    obstacles[1] = abs(snake.body[0].x - segment.x)
                    if obstacles[1] == 1:
                        dist_body[1] = 1
            if (snake.body[0].x - default_dist) <= segment.x and snake.body[0].y == segment.y and snake.body[0].x > segment.x:    # looking right for the tail segment
                if obstacles[2] == -1 or obstacles[2] > abs(snake.body[0].x - segment.x):
                    obstacles[2] = abs(snake.body[0].x - segment.x)
                    if obstacles[2] == 1:
                        dist_body[1] = 1
        elif snake.direction == Vector2(0, -1):     # if snake is moving up
            if (snake.body[0].y - default_dist) <= segment.y and snake.body[0].x == segment.x and snake.body[0].y > segment.y:    # looking ahead for the tail segment
                if obstacles[0] == -1 or obstacles[0] > abs(snake.body[0].y - segment.y):
                    obstacles[0] = abs(snake.body[0].y - segment.y)
                    if obstacles[0] == 1:
                        dist_body[0] = 1
            if (snake.body[0].x - default_dist) <= segment.x and snake.body[0].x > segment.x:    # looking left for the tail segment
                if obstacles[1] == -1 or obstacles[1] > abs(snake.body[0].x - segment.x):
                    obstacles[1] == abs(snake.body[0].x - segment.x)
                    if obstacles[1] == 1:
                        dist_body[1] = 1
            if (snake.body[0].x + default_dist) >= segment.x and snake.body[0].y == segment.y and snake.body[0].x < segment.x:    # looking right for the tail segment
                if obstacles[2] == -1 or obstacles[2] > abs(snake.body[0].x - segment.x):
                    obstacles[2] == abs(snake.body[0].x - segment.x)
                    if obstacles[2] == 1:
                        dist_body[2] = 1
        elif snake.direction == Vector2(-1, 0):     # if snake is moving left
            if (snake.body[0].x - default_dist) <= segment.x and snake.body[0].y == segment.y and snake.body[0].x > segment.x:
                if obstacles[0] == -1 or obstacles[0] > abs(snake.body[0].x - segment.x):   # looking ahead for the tail segment
                    obstacles[0] = abs(snake.body[0].x - segment.x)
                    if obstacles[0] == 1:
                        dist_body[0] = 1
            if (snake.body[0].y + default_dist) >= segment.y and snake.body[0].x == segment.x and snake.body[0].y < segment.y:
                if obstacles[1] == -1 or obstacles[1] > abs(snake.body[0].y - segment.y):   # looking left for the tail segment
                    obstacles[1] = abs(snake.body[0].y - segment.y)
                    if obstacles[1] == 1:
                        dist_body[1] = 1
            if (snake.body[0].y - default_dist) <= segment.y and snake.body[0].x == segment.x and snake.body[0].y > segment.y:
                if obstacles[2] == -1 or obstacles[2] > abs(snake.body[0].y - segment.y):   # looking right for the tail segment
                    obstacles[2] = abs(snake.body[0].y - segment.y)
                    if obstacles[2] == 1:
                        dist_body[2] = 1
        elif snake.direction == Vector2(1, 0):      # if snake is moving right
            if (snake.body[0].x + default_dist) >= segment.x and snake.body[0].y == segment.y and snake.body[0].x < segment.x:
                if obstacles[0] == -1 or obstacles[0] > abs(snake.body[0].x - segment.x):   # looking ahead for the tail segment
                    obstacles[0] = abs(snake.body[0].x - segment.x)
                    if obstacles[0] == 1:
                        dist_body[0] = 1
            if (snake.body[0].y - default_dist) <= segment.y and snake.body[0].x == segment.x and snake.body[0].y > segment.y:
                if obstacles[1] == -1 or obstacles[1] > abs(snake.body[0].y - segment.y):   # looking left for the tail segment
                    obstacles[1] = abs(snake.body[0].y - segment.y)
                    if obstacles[1] == 1:
                        dist_body[1] = 1
            if (snake.body[0].y + default_dist) >= segment.y and snake.body[0].x == segment.x and snake.body[0].y < segment.y:
                if obstacles[2] == -1 or obstacles[1] > abs(snake.body[0].y - segment.y):   # looking right for the tail segment
                    obstacles[2] = abs(snake.body[0].y - segment.y)
                    if obstacles[2] == 1:
                        dist_body[2] = 1

    # Border vision
    borders = [-1, -1, -1] # Ahead, Left, Right

    if snake.direction == Vector2(0, 1):    # if snake is moving down
        borders[0] = snake.body[0].y - 1
        borders[1] = snake.body[0].x - 1
        borders[2] = cell_number - snake.body[0].x
    elif snake.direction == Vector2(0, -1):     # if snake is moving up
        borders[0] = cell_number - snake.body[0].y
        borders[1] = cell_number - snake.body[0].x
        borders[2] = snake.body[0].x - 1
    elif snake.direction == Vector2(-1, 0):     # if snake is moving left
        borders[0] = snake.body[0].x - 1
        borders[1] = cell_number - snake.body[0].y
        borders[2] = snake.body[0].y - 1
    elif snake.direction == Vector2(1, 0):      # if snake is moving right
        borders[0] = cell_number - snake.body[0].x
        borders[1] = cell_number - snake.body[0].y
        borders[2] = snake.body[0].y - 1
    
    for i, border in enumerate(borders):
        if border != -1 and obstacles[i] == -1:
            obstacles[i] = border

    # Fruit vision
    dir_fruit = [-1, -1, -1]    # Ahead, Left, Right
    fruit_dist = Vector2(abs(snake.body[0].x - fruit.pos.x), abs(snake.body[0].y - snake.body[0].y))
    blocked = [-1, -1, -1]      # Blocked by body (Ahead, Left, Right)

    if snake.direction == Vector2(0, 1):    # snake is moving down
        if snake.body[0].y < fruit.pos.y:
            if obstacles[0] < fruit_dist.y and obstacles[0] != -1:
                blocked[0] = 1
            else:
                dir_fruit[0] = 1
        elif snake.body[0].y > fruit.pos.y and snake.body[0].x == fruit.pos.x:
            dir_fruit[1] == 1
            dir_fruit[2] == 1
        if snake.body[0].x < fruit.pos.x:
            if obstacles[1] < fruit_dist.x and obstacles[1] != -1:
                blocked[1] = 1
            else:
                dir_fruit[1] = 1
        if snake.body[0].x > fruit.pos.x:
            if obstacles[2] < fruit_dist.x and obstacles[2] != -1:
                blocked[2] = 1
            else:
                dir_fruit[2] = 1
    
    elif snake.direction == Vector2(0, -1):     # snake is moving up
        if snake.body[0].y > fruit.pos.y:
            if obstacles[0] < fruit_dist.y and obstacles[0] != -1:
                blocked[0] = 1
            else:
                dir_fruit[0] = 1
        elif snake.body[0].y < fruit.pos.y and snake.body[0].x == fruit.pos.x:
            dir_fruit[1] = 1
            dir_fruit[2] = 1
        if snake.body[0].x > fruit.pos.x:
            if obstacles[1] < fruit_dist.x and obstacles[1] != -1:
                blocked[1] = 1
            else:
                dir_fruit[1] = 1
        if snake.body[0].x < fruit.pos.x:
            if obstacles[2] < fruit_dist.x and obstacles[2] != -1:
                blocked[2] = 1
            else:
                dir_fruit[2] = 1
    
    elif snake.direction == Vector2(-1, 0):     # if snake is moving left
        if snake.body[0].x > fruit.pos.x:
            if obstacles[0] < fruit_dist.x and obstacles[0] != -1:
                blocked[0] = 1
            else:
                dir_fruit[0] = 1
        elif snake.body[0].x < fruit.pos.x and snake.body[0].y == fruit.pos.y:
            dir_fruit[1] = 1
            dir_fruit[2] = 1
        if snake.body[0].y < fruit.pos.y:
            if obstacles[1] < fruit_dist.y and obstacles[1] != -1:
                blocked[1] = 1
            else:
                dir_fruit[1] = 1
        if snake.body[0].y > fruit.pos.y:
            if obstacles[2] < fruit_dist.y and obstacles[2] != -1:
                blocked[2] = 1
            else:
                dir_fruit[2] = 1
    
    elif snake.direction == Vector2(1, 0):      # if snake is moving right
        if snake.body[0].x < fruit.pos.x:
            if obstacles[0] < fruit_dist.x and obstacles[0] != -1:
                blocked[0] = 1
            else:
                dir_fruit[0] = 1
        elif snake.body[0].x > fruit.pos.x and snake.body[0].y == fruit.pos.y:
            dir_fruit[1] = 1
            dir_fruit[2] = 1
        if snake.body[0].y > fruit.pos.y:
            if obstacles[1] < fruit_dist.y and obstacles[1] != -1:
                blocked[1] = 1
            else:
                dir_fruit[1] = 1
        if snake.body[0].y < fruit.pos.y:
            if obstacles[2] < fruit_dist.y and obstacles[2] != -1:
                blocked[2] = 1
            else:
                dir_fruit[2] = 1
    
    if -1 not in obstacles:
        dir_fruit = [-1, -1, -1]
        for i in range(len(obstacles)):
            dir_fruit[obstacles.index(max(obstacles))] = 1

    elif sum(blocked) > -2 or (1 in blocked and 1 in borders):
        dir_fruit = [-1, -1, -1]
        dir_fruit[obstacles.index(-1)] = 1

    fruit_n = 1 if snake.body[0].y < fruit.pos.y else -1
    fruit_s = 1 if snake.body[0].y > fruit.pos.y else -1
    fruit_w = 1 if snake.body[0].x > fruit.pos.x else -1
    fruit_e = 1 if snake.body[0].x < fruit.pos.x else -1
    fruit_dist = math.sqrt(pow(fruit.pos.x - snake.body[0].x, 2) + pow(fruit.pos.y - snake.body[0].y, 2))

    # Size vision
    size = len(snake.body[:-1])

    return obstacles + dir_fruit + [size]

    """ return obstacles + [# border_n, border_s, border_w, border_e,
            # border_forward, border_left, border_right,
            # direction_n, direction_s, direction_w, direction_e,
            fruit_n, fruit_s, fruit_w, fruit_e, # fruit_dist,
            ] """


def controls(game, output):
    """Controls snake based on the neural network output."""

    if max(output) == output[0]:    # Left
        if game.snake.direction == Vector2(0, 1):
            game.snake.direction = Vector2(1, 0)
        elif game.snake.direction == Vector2(0, -1):
            game.snake.direction = Vector2(-1, 0)
        elif game.snake.direction == Vector2(-1, 0):
            game.snake.direction = Vector2(0, 1)
        elif game.snake.direction == Vector2(1, 0):
            game.snake.direction = Vector2(0, -1)
    if max(output) == output[1]:    # Right
        if game.snake.direction == Vector2(0, 1):
            game.snake.direction = Vector2(-1, 0)
        elif game.snake.direction == Vector2(0, -1):
            game.snake.direction = Vector2(1, 0)
        elif game.snake.direction == Vector2(-1, 0):
            game.snake.direction = Vector2(0, -1)
        elif game.snake.direction == Vector2(1, 0):
            game.snake.direction = Vector2(0, 1)
    if max(output) == output[2]:    # Forward
        pass


def run(genomes, config):
    global init, generation, highscore
    global debug_menu

    generation += 1

    pause = False

    # if not init:
    #     init = True
    #     menu(screen)

    games = []
    nets = []
    frames = []

    for i, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        g.fitness = 0
        frames.append(0)

        games.append(Game())

    font = pygame.font.Font(os.path.join("resources", "fonts", "FixelMedium.ttf"), 20)
    debug_font = pygame.font.Font(os.path.join("resources", "fonts", "FixelMedium.ttf"), 15)

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
                if not pause:
                    for i, game in enumerate(games):
                        game.update()

                        if game.check_collision():
                            genomes[i][1].fitness += 1      # increase the fitness (fruit eaten)
                            frames[i] = 0
                        
                        frames[i] += 1
                        if frames[i] >= 100 and len(game.snake.body) <= 5:
                            game.failed = True
                        # else:
                        #     if frames > 10:
                        #         genomes[j][1].fitness -= 10     # lower the fitness (assuming it is loop)

                        if game.failed:
                            genomes[i][1].fitness -= 10     # lower the fitness (fail)
                            games.pop(i)
                            nets.pop(i)
                    
                    # Weird, but somehow fixes "index out of range" so idc
                    for i, game in enumerate(games):
                        output = nets[i].activate(vision(game))     # activating the neural network

                        controls(game, output)      # controls game based on the output from the neural network

                        # if max(output) == output[0]:
                        #     game.snake.direction = Vector2(0, 1)    # Up
                        # elif max(output) == output[1]:
                        #     game.snake.direction = Vector2(0, -1)   # Down
                        # elif max(output) == output[2]:
                        #     game.snake.direction = Vector2(-1, 0)   # Left
                        # elif max(output) == output[3]:
                        #     game.snake.direction = Vector2(1, 0)    # Right

        # display_game = max(net[1].fitness)

        if not pause:
            screen.fill((66, 69, 73))

            # Rendering text
            label = font.render(f"Generation: {generation}", True, (255, 255, 255))
            screen.blit(label, (5, 5))

            score = font.render(f"Score: 0", True, (255, 255, 255))
            screen.blit(score, (5, 25))

            genomes_set = {}
            for i, genome in enumerate(genomes):
                genomes_set.update({
                    "id": i + 1,
                    "genome": genome,
                    "fitness": genome[1].fitness
                })
            
            print(genomes_set)

            best_genomes = heapq.nlargest(5, genomes)
            if debug_menu:
                text_pos = 5
                for i, genome in enumerate(best_genomes):
                    net_info = debug_font.render(f"ID: {i}, Fitness: {genomes[i][1].fitness}", True, (255, 255, 255))
                    net_info_rect = net_info.get_rect()
                    screen_rect = screen.get_rect()
                    screen.blit(net_info, (screen_rect.right - 120, text_pos))
                    text_pos += 20
                    if i == 5:
                        break
        
        for game in games:
            game.draw_elements()
            break

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

    p = neat.Population(config)     # creating population

    # Setting up pygame
    pygame.init()
    cell_size = 15
    cell_number = 40
    top_bar = 150
    screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
    pygame.display.set_caption("Snake AI")
    clock = pygame.time.Clock()

    # Global vars
    init = False
    generation = 0
    highscore = 0

    # Ingame settings
    debug_menu = False

    SCREEN_UPDATE = pygame.USEREVENT
    pygame.time.set_timer(SCREEN_UPDATE, 10)

    p.run(run)      # jumping to the run function and getting the winner
