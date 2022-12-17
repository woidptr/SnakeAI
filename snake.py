import math
import pygame
from pygame import Vector2
from enum import Enum

import fruit

cell_size = 15
cell_number = 40

class Directions(Enum):
    DOWN = Vector2(0, 1)
    UP = Vector2(0, -1)
    LEFT = Vector2(-1, 0)
    RIGHT = Vector2(1, 0)


def distance(x1, x2, y1, y2):
    """Calculating distance using the vector distance formula."""

    return int(math.sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2))) - 1


class Snake():
    """
    Snake object
    """

    def __init__(self, screen):
        self.screen = screen
        self.body = [Vector2(7, 10), Vector2(6, 10), Vector2(5, 10)]
        self.direction = Vector2(1, 0)
        self.x = None
        self.y = None
        self.size = len(self.body[:-1])
        self.score = 0
        self.new_block = False
        self.failed = False
        self.fruit = fruit.Fruit(screen)

    def draw_snake(self):
        """
        Drawing snake body
        """

        for i, block in enumerate(self.body):
            block_rect = pygame.Rect(block.x * cell_size, block.y * cell_size, cell_size, cell_size)
            if i == 0:
                pygame.draw.rect(self.screen, (96, 125, 139), block_rect)
            else:
                pygame.draw.rect(self.screen, (144, 164, 174), block_rect)
            self.x = block_rect.x
            self.y = block_rect.y
        
        # self.draw_debug_lines()
    
    def draw_debug_lines(self):
        # North border vision
        start_pos = Vector2(self.body[0].x * cell_size + 10, self.body[0].y * cell_size)
        end_pos = Vector2(self.body[0].x * cell_size + 10, 0)
        pygame.draw.line(self.screen, (87, 242, 135), start_pos, end_pos, 3)

        # South border vision
        start_pos = Vector2(self.body[0].x * cell_size - cell_size + 10, self.body[0].y * cell_size)
        end_pos = Vector2(self.body[0].x * cell_size - cell_size + 10, cell_number * cell_size)
        pygame.draw.line(self.screen, (87, 242, 135), start_pos, end_pos, 3)

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
    
    def update(self):
        """Update snake position."""

        self.move_snake()
        #self.check_collision()
        self.check_fail()

    def draw_elements(self):
        """Render elements (snake and fruit)"""
        self.fruit.draw_fruit()
        self.draw_snake()

    def check_collision(self):
        """Check for snake collision with fruit."""

        if self.fruit.pos == self.body[0]:
            self.fruit.reposition()
            self.new_block = True

            self.score += 1

            return True
        return False

    def check_fail(self):
        """Check if snake is outside the border or inside it's tail."""

        if not 0 <= self.body[0].x < cell_number or not 0 <= self.body[0].y < cell_number:
            self.failed = True

        for block in self.body[1:]:
            if block == self.body[0]:
                self.failed = True

    def vision(self):
        # output = []

        # if self.direction == Directions.DOWN.value:
        #     # Getting the distance to the food
        #     output.append(self.body[0].x - self.fruit.pos.x - 1)    # looking for the food to it's right
        #     if self.fruit.pos.x <= (self.body[0].x - 1) and self.fruit.pos.y >= (self.body[0].y + 1):
        #         output.append(self.body[0].x - 1, self.fruit.pos.x, self.body[0].y + 1, self.fruit.pos.y)
        
        global cell_number

        fruit = self.fruit      # getting fruit object

        default_dist = cell_number / 2

        # Obstacles vision
        obstacles = [-1, -1, -1]    # Ahead, Left, Right

        # Tail vision
        for segment in self.body[1:]:
            if self.direction == Vector2(0, 1):        # if snake is moving down
                if (self.body[0].y + default_dist) >= segment.y and self.body[0].x == segment.x and self.body[0].y < segment.y:    # looking ahead for the tail segment
                    if obstacles[0] == -1 or obstacles[0] > abs(self.body[0].y - segment.y):
                        obstacles[0] = abs(self.body[0].y - segment.y)
                if (self.body[0].x + default_dist) >= segment.x and self.body[0].y == segment.y and self.body[0].x < segment.x:   # looking left for the tail segment
                    if obstacles[1] == -1 or obstacles[1] > abs(self.body[0].x - segment.x):
                        obstacles[1] = abs(self.body[0].x - segment.x)
                if (self.body[0].x - default_dist) <= segment.x and self.body[0].y == segment.y and self.body[0].x > segment.x:    # looking right for the tail segment
                    if obstacles[2] == -1 or obstacles[2] > abs(self.body[0].x - segment.x):
                        obstacles[2] = abs(self.body[0].x - segment.x)
            elif self.direction == Vector2(0, -1):     # if self is moving up
                if (self.body[0].y - default_dist) <= segment.y and self.body[0].x == segment.x and self.body[0].y > segment.y:    # looking ahead for the tail segment
                    if obstacles[0] == -1 or obstacles[0] > abs(self.body[0].y - segment.y):
                        obstacles[0] = abs(self.body[0].y - segment.y)
                if (self.body[0].x - default_dist) <= segment.x and self.body[0].x > segment.x:    # looking left for the tail segment
                    if obstacles[1] == -1 or obstacles[1] > abs(self.body[0].x - segment.x):
                        obstacles[1] == abs(self.body[0].x - segment.x)
                if (self.body[0].x + default_dist) >= segment.x and self.body[0].y == segment.y and self.body[0].x < segment.x:    # looking right for the tail segment
                    if obstacles[2] == -1 or obstacles[2] > abs(self.body[0].x - segment.x):
                        obstacles[2] == abs(self.body[0].x - segment.x)
            elif self.direction == Vector2(-1, 0):     # if self is moving left
                if (self.body[0].x - default_dist) <= segment.x and self.body[0].y == segment.y and self.body[0].x > segment.x:
                    if obstacles[0] == -1 or obstacles[0] > abs(self.body[0].x - segment.x):   # looking ahead for the tail segment
                        obstacles[0] = abs(self.body[0].x - segment.x)
                if (self.body[0].y + default_dist) >= segment.y and self.body[0].x == segment.x and self.body[0].y < segment.y:
                    if obstacles[1] == -1 or obstacles[1] > abs(self.body[0].y - segment.y):   # looking left for the tail segment
                        obstacles[1] = abs(self.body[0].y - segment.y)
                if (self.body[0].y - default_dist) <= segment.y and self.body[0].x == segment.x and self.body[0].y > segment.y:
                    if obstacles[2] == -1 or obstacles[2] > abs(self.body[0].y - segment.y):   # looking right for the tail segment
                        obstacles[2] = abs(self.body[0].y - segment.y)
            elif self.direction == Vector2(1, 0):      # if self is moving right
                if (self.body[0].x + default_dist) >= segment.x and self.body[0].y == segment.y and self.body[0].x < segment.x:
                    if obstacles[0] == -1 or obstacles[0] > abs(self.body[0].x - segment.x):   # looking ahead for the tail segment
                        obstacles[0] = abs(self.body[0].x - segment.x)
                if (self.body[0].y - default_dist) <= segment.y and self.body[0].x == segment.x and self.body[0].y > segment.y:
                    if obstacles[1] == -1 or obstacles[1] > abs(self.body[0].y - segment.y):   # looking left for the tail segment
                        obstacles[1] = abs(self.body[0].y - segment.y)
                if (self.body[0].y + default_dist) >= segment.y and self.body[0].x == segment.x and self.body[0].y < segment.y:
                    if obstacles[2] == -1 or obstacles[1] > abs(self.body[0].y - segment.y):   # looking right for the tail segment
                        obstacles[2] = abs(self.body[0].y - segment.y)

        # Border vision
        borders = [-1, -1, -1] # Ahead, Left, Right

        if self.direction == Vector2(0, 1):    # if self is moving down
            borders[0] = self.body[0].y - 1
            borders[1] = self.body[0].x - 1
            borders[2] = cell_number - self.body[0].x
        elif self.direction == Vector2(0, -1):     # if self is moving up
            borders[0] = cell_number - self.body[0].y
            borders[1] = cell_number - self.body[0].x
            borders[2] = self.body[0].x - 1
        elif self.direction == Vector2(-1, 0):     # if self is moving left
            borders[0] = self.body[0].x - 1
            borders[1] = cell_number - self.body[0].y
            borders[2] = self.body[0].y - 1
        elif self.direction == Vector2(1, 0):      # if self is moving right
            borders[0] = cell_number - self.body[0].x
            borders[1] = cell_number - self.body[0].y
            borders[2] = self.body[0].y - 1

        for i, border in enumerate(borders):
            if border != -1 and obstacles[i] == -1:
                obstacles[i] = border

        # Fruit vision
        dir_fruit = [-1, -1, -1]    # Ahead, Left, Right
        fruit_dist = Vector2(abs(self.body[0].x - fruit.pos.x), abs(self.body[0].y - self.body[0].y))
        blocked = [-1, -1, -1]      # Blocked by body (Ahead, Left, Right)

        if self.direction == Vector2(0, 1):    # self is moving down
            if self.body[0].y < fruit.pos.y:
                if obstacles[0] < fruit_dist.y and obstacles[0] != -1:
                    blocked[0] = 1
                else:
                    dir_fruit[0] = 1
            elif self.body[0].y > fruit.pos.y and self.body[0].x == fruit.pos.x:
                dir_fruit[1] == 1
                dir_fruit[2] == 1
            if self.body[0].x < fruit.pos.x:
                if obstacles[1] < fruit_dist.x and obstacles[1] != -1:
                    blocked[1] = 1
                else:
                    dir_fruit[1] = 1
            if self.body[0].x > fruit.pos.x:
                if obstacles[2] < fruit_dist.x and obstacles[2] != -1:
                    blocked[2] = 1
                else:
                    dir_fruit[2] = 1

        elif self.direction == Vector2(0, -1):     # self is moving up
            if self.body[0].y > fruit.pos.y:
                if obstacles[0] < fruit_dist.y and obstacles[0] != -1:
                    blocked[0] = 1
                else:
                    dir_fruit[0] = 1
            elif self.body[0].y < fruit.pos.y and self.body[0].x == fruit.pos.x:
                dir_fruit[1] = 1
                dir_fruit[2] = 1
            if self.body[0].x > fruit.pos.x:
                if obstacles[1] < fruit_dist.x and obstacles[1] != -1:
                    blocked[1] = 1
                else:
                    dir_fruit[1] = 1
            if self.body[0].x < fruit.pos.x:
                if obstacles[2] < fruit_dist.x and obstacles[2] != -1:
                    blocked[2] = 1
                else:
                    dir_fruit[2] = 1

        elif self.direction == Vector2(-1, 0):     # if self is moving left
            if self.body[0].x > fruit.pos.x:
                if obstacles[0] < fruit_dist.x and obstacles[0] != -1:
                    blocked[0] = 1
                else:
                    dir_fruit[0] = 1
            elif self.body[0].x < fruit.pos.x and self.body[0].y == fruit.pos.y:
                dir_fruit[1] = 1
                dir_fruit[2] = 1
            if self.body[0].y < fruit.pos.y:
                if obstacles[1] < fruit_dist.y and obstacles[1] != -1:
                    blocked[1] = 1
                else:
                    dir_fruit[1] = 1
            if self.body[0].y > fruit.pos.y:
                if obstacles[2] < fruit_dist.y and obstacles[2] != -1:
                    blocked[2] = 1
                else:
                    dir_fruit[2] = 1

        elif self.direction == Vector2(1, 0):      # if self is moving right
            if self.body[0].x < fruit.pos.x:
                if obstacles[0] < fruit_dist.x and obstacles[0] != -1:
                    blocked[0] = 1
                else:
                    dir_fruit[0] = 1
            elif self.body[0].x > fruit.pos.x and self.body[0].y == fruit.pos.y:
                dir_fruit[1] = 1
                dir_fruit[2] = 1
            if self.body[0].y > fruit.pos.y:
                if obstacles[1] < fruit_dist.y and obstacles[1] != -1:
                    blocked[1] = 1
                else:
                    dir_fruit[1] = 1
            if self.body[0].y < fruit.pos.y:
                if obstacles[2] < fruit_dist.y and obstacles[2] != -1:
                    blocked[2] = 1
                else:
                    dir_fruit[2] = 1

        # if -1 not in obstacles:
        #     dir_fruit = [-1, -1, -1]
        #     for i in range(len(obstacles)):
        #         dir_fruit[obstacles.index(max(obstacles))] = 1

        # elif sum(blocked) > -2 or (1 in blocked and 1 in borders):
        #     dir_fruit = [-1, -1, -1]
        #     dir_fruit[obstacles.index(-1)] = 1

        return obstacles + dir_fruit