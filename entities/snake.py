import math
import pygame
from pygame import Vector2
from enum import Enum

from entities import fruit

cell_size = 15
cell_number = 40

class Directions(Enum):
    DOWN = Vector2(0, 1)
    UP = Vector2(0, -1)
    LEFT = Vector2(-1, 0)
    RIGHT = Vector2(1, 0)


def distance(x1, x2, y1, y2) -> int:
    """Calculating distance using the vector distance formula."""

    return int(math.sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2))) - 1

def valid(x, y) -> bool:
    if 0 <= x <= 40 and 0 <= y <= 40:
        return True
    return False


# Snake entity
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
        self.loop_size = 0
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

    def _controls(self, output):
        """Controls snake based on the neural network output."""

        if max(output) == output[0]:    # Left
            if self.direction == Vector2(0, 1):
                self.direction = Vector2(1, 0)
            elif self.direction == Vector2(0, -1):
                self.direction = Vector2(-1, 0)
            elif self.direction == Vector2(-1, 0):
                self.direction = Vector2(0, 1)
            elif self.direction == Vector2(1, 0):
                self.direction = Vector2(0, -1)
        if max(output) == output[1]:    # Right
            if self.direction == Vector2(0, 1):
                self.direction = Vector2(-1, 0)
            elif self.direction == Vector2(0, -1):
                self.direction = Vector2(1, 0)
            elif self.direction == Vector2(-1, 0):
                self.direction = Vector2(0, -1)
            elif self.direction == Vector2(1, 0):
                self.direction = Vector2(0, 1)
        if max(output) == output[2]:    # Forward
            pass

    def _tick_movement(self):
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
    
    def _check_fail(self):
        """Check if snake is outside the border or inside it's tail."""

        if not 0 <= self.body[0].x < cell_number or not 0 <= self.body[0].y < cell_number:
            self.failed = True

        for block in self.body[1:]:
            if block == self.body[0]:
                self.failed = True

    def tick(self, output):
        """Update snake position."""

        self._controls(output)
        self._tick_movement()
        #self.check_collision()
        self._check_fail()

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

        return obstacles # + dir_fruit
    
    def fruit_vision(self):
        output = []

        if self.direction == Vector2(0, 1):
            output.append(self.body[0].x - self.fruit.pos.x - 1)    # Looking right for the fruit

            if self.fruit.pos.x <= (self.body[0].x - 1) and self.fruit.pos.y >= (self.body[0].y + 1):
                output.append(distance(self.body[0].x - 1, self.fruit.pos.x, self.body[0].y + 1, self.fruit.pos.y))
            else:
                output.append(- distance(self.body[0].x - 1, self.fruit.pos.x, self.body[0].y + 1, self.fruit.pos.y))
            
            output.append(self.fruit.pos.y - self.body[0].y - 1)

            if self.fruit.pos.x >= (self.body[0].x + 1) and self.fruit.pos.y >= (self.body[0].y + 1):
                output.append(distance(self.body[0].x + 1, self.fruit.pos.x, self.body[0].y + 1, self.fruit.pos.x))
            else:
                output.append(- distance(self.body[0].x - 1, self.fruit.pos.x, self.body[0].y + 1, self.fruit.pos.x))
            
            output.append(self.fruit.pos.x - self.body[0].x - 1)

            d = 100
            x = self.body[0].x - 1
            y = self.body[0].y
            run = True

            while valid(x, y) and run:
                for i in range(1, len(self.body[1:]) + 1):
                    if x == self.body[i].x and y == self.body[i].y:
                        d = self.body[0].x - x - 1
                        run = False
                        break
                x -= 1
            output.append(min(d, self.body[0].x))
            # 8(ForwardRight)
            d = 100
            x = self.body[0].x - 1
            y = self.body[0].y + 1
            run = True

            while valid(x, y) and run:
                for i in range(1, len(self.body[1:]) + 1):
                    if x == self.body[i].x and y == self.body[i].y:
                        d = distance(self.body[0].x, x, self.body[0].y, y)
                        run = False
                        break
                y += 1
                x -= 1
            output.append(min(d, (distance(self.body[0].x, 0, self.body[0].y, 40))))
            # 7(Forward)
            d = 100
            x = self.body[0].x
            y = self.body[0].y + 1
            run = True

            while valid(x, y) and run:
                for i in range(1, len(self.body[1:]) + 1):
                    if x == self.body[i].x and y == self.body[i].y:
                        d = y - self.body[0].y - 1
                        run = False
                        break
                y += 1
            output.append(min(d, (40 - self.body[0].y - 1)))
            # (ForwardLeft)
            d = 100
            x = self.body[0].x + 1
            y = self.body[0].y + 1
            run = True

            while valid(x, y) and run:
                for i in range(1, len(self.body[1:]) + 1):
                    if x == self.body[i].x and y == self.body[i].y:
                        d = distance(self.body[0].x, x, self.body[0].y, y)
                        run = False
                        break
                x += 1
                y += 1
            output.append(min(d, (distance(self.body[0].x, 40, self.body[0].y, 40))))
            # (Left)
            d = 100
            x = self.body[0].x + 1
            y = self.body[0].y
            run = True

            while valid(x, y) and run:
                for i in range(1, len(self.body[1:]) + 1):
                    if x == self.body[i].x and y == self.body[i].y:
                        d = x - (self.body[0].x + 1)
                        run = False
                        break
                x += 1
            output.append(min((40 - self.body[0].x - 1), d))
        
        elif self.direction == Vector2(-1, 0):
            output.append(self.body[0].y - self.fruit.pos.y - 1)

            if self.fruit.pos.x <= (self.body[0].x - 1) and self.fruit.pos.y <= (self.body[0].y - 1):
                output.append(distance(self.body[0].x - 1, self.fruit.pos.x, self.body[0].y - 1, self.fruit.pos.y))
            else:
                output.append(- distance(self.body[0].x - 1, self.fruit.pos.x, self.body[0].y - 1, self.fruit.pos.y))
            
            output.append(self.body[0].x - self.fruit.pos.x - 1)

            if self.fruit.pos.x <= (self.body[0].x - 1) and self.fruit.pos.y >= (self.body[0].y + 1):
                output.append(distance(self.body[0].x - 1, self.fruit.pos.x, self.body[0].y + 1, self.fruit.pos.y))
            else:
                output.append(- distance(self.body[0].x - 1, self.fruit.pos.x, self.body[0].y + 1, self.fruit.pos.y))
            
            output.append(self.fruit.pos.y - self.body[0].y - 1)

            # Distance to the nearest obstacle
            # (Right)
            d = 100
            x = self.body[0].x
            y = self.body[0].y - 1
            run = True

            while valid(x, y) and run:
                for i in range(1, len(self.body[1:]) + 1):
                    if x == self.body[i].x and y == self.body[i].y:
                        d = self.body[0].y - y - 1
                        run = False
                        break
                y -= 1
            output.append(min(d, self.body[0].y))

            # (Forward Right)
            d = 100
            x = self.body[0].x - 1
            y = self.body[0].y - 1
            run = True

            while valid(x, y) and run:
                for i in range(1, len(self.body[1:]) + 1):
                    if x == self.body[i].x and y == self.body[i].y:
                        d = distance(self.body[0].x, x, self.body[0].y, y)
                        run = False
                        break
                x -= 1
                y -= 1
            output.append(min(d, (distance(self.body[0].x, 0, self.body[0].y, 0))))

            # (Forward)
            d = 100
            x = self.body[0].x - 1
            y = self.body[0].y
            run = True

            while valid(x, y) and run:
                for i in range(1, len(self.body[1:]) + 1):
                    if x == self.body[i].x and y == self.body[i].y:
                        d = self.body[0].x - x - 1
                        run = False
                        break
                x -= 1
            output.append(min(d, self.body[0].x))

            # (Forward Left)
            d = 100
            x = self.body[0].x - 1
            y = self.body[0].y + 1
            run = True

            while valid(x, y) and run:
                for i in range(1, len(self.body[1:]) + 1):
                    if x == self.body[i].x and y == self.body[i].y:
                        d = distance(self.body[0].x, x, self.body[0].y, y)
                        run = False
                        break
                y += 1
                x -= 1
            output.append(min(d, (distance(self.body[0].x, 0, self.body[0].y, 40))))

            # (Left)
            d = 100
            x = self.body[0].x
            y = self.body[0].y + 1
            run = True

            while valid(x, y) and run:
                for i in range(1, len(self.body[1:]) + 1):
                    if x == self.body[i].x and y == self.body[i].y:
                        d = y - self.body[0].y - 1
                        run = False
                        break
                y += 1
            output.append(min(d, (40 - self.body[0].y - 1)))
        
        elif self.direction == Vector2(1, 0):
            output.append(self.fruit.pos.y - self.body[0].y - 1)

            if self.fruit.pos.x >= (self.body[0].x + 1) and self.fruit.pos.y >= (self.body[0].y + 1):
                output.append(distance(self.body[0].x + 1, self.fruit.pos.x, self.body[0].y + 1, self.fruit.pos.y))
            else:
                output.append(- distance(self.body[0].x + 1, self.fruit.pos.x, self.body[0].y + 1, self.fruit.pos.y))
            
            output.append(self.fruit.pos.x - self.body[0].x - 1)

            if self.fruit.pos.x >= (self.body[0].x + 1) and self.fruit.pos.y <= (self.body[0].y - 1):
                output.append(distance(self.body[0].x + 1, self.fruit.pos.x, self.body[0].y - 1, self.fruit.pos.y))
            else:
                output.append(- distance(self.body[0].x + 1, self.fruit.pos.x, self.body[0].y - 1, self.fruit.pos.y))
            
            output.append(self.body[0].y - self.fruit.pos.y - 1)

            # Distance to the nearest object
            # 7(Right)
            d = 100
            x = self.body[0].x
            y = self.body[0].y + 1
            run = True

            while valid(x, y) and run:
                for i in range(1, len(self.body[1:]) + 1):
                    if x == self.body[i].x and y == self.body[i].y:
                        d = y - self.body[0].y - 1
                        run = False
                        break
                y += 1
            output.append(min(d, (40 - self.body[0].y - 1)))

            # 8(Forward Right)
            d = 100
            x = self.body[0].x + 1
            y = self.body[0].y + 1
            run = True

            while valid(x, y) and run:
                for i in range(1, len(self.body[1:]) + 1):
                    if x == self.body[i].x and y == self.body[i].y:
                        d = distance(self.body[0].x, x, self.body[0].y, y)
                        run = False
                        break
                y += 1
                x += 1
            output.append(min(d, (distance(self.body[0].x, 0, self.body[0].y, 40))))

            # 5(Forward)
            d = 100
            x = self.body[0].x + 1
            y = self.body[0].y
            run = True

            while valid(x, y) and run:
                for i in range(1, len(self.body[1:]) + 1):
                    if x == self.body[i].x and y == self.body[i].y:
                        d = x - self.body[0].x - 1
                        run = False
                        break
                x += 1
            output.append(min(d, (40 - self.body[0].x - 1)))

            # 4(Forward Left)
            d = 100
            x = self.body[0].x + 1
            y = self.body[0].y - 1
            run = True

            while valid(x, y) and run:
                for i in range(1, len(self.body[1:]) + 1):
                    if x == self.body[i].x and y == self.body[i].y:
                        d = distance(self.body[0].x, x, self.body[0].y, y)
                        run = False
                        break
                y -= 1
                x += 1
            output.append(min(d, (distance(self.body[0].x, 40, self.body[0].y, 0))))

            # 3(Left)
            d = 100
            x = self.body[0].x
            y = self.body[0].y - 1
            run = True

            while valid(x, y) and run:
                for i in range(1, len(self.body[1:]) + 1):
                    if x == self.body[i].x and y == self.body[i].y:
                        d = self.body[0].y - y - 1
                        run = False
                        break
                y -= 1
            output.append(min(d, self.body[0].y))
        
        elif self.direction == Vector2(0, -1):
            output.append(self.fruit.pos.x - self.body[0].x - 1)

            if self.fruit.pos.x >= (self.body[0].x + 1) and self.fruit.pos.y <= (self.body[0].y - 1):
                output.append(distance(self.body[0].x + 1, self.fruit.pos.x, self.body[0].y - 1, self.fruit.pos.y))
            else:
                output.append(- distance(self.body[0].x + 1, self.fruit.pos.x, self.body[0].y - 1, self.fruit.pos.y))
            
            output.append(self.body[0].y - self.fruit.pos.y - 1)

            if self.fruit.pos.x <= (self.body[0].x - 1) and self.fruit.pos.x <= (self.body[0].y - 1):
                output.append(distance(self.body[0].x - 1, self.fruit.pos.x, self.body[0].y - 1, self.fruit.pos.y))
            else:
                output.append(- distance(self.body[0].x - 1, self.fruit.pos.x, self.body[0].y - 1, self.fruit.pos.y))
            
            output.append(self.body[0].x - self.fruit.pos.x - 1)

            # Distance to the nearest object
            # 5(Right)
            d = 100
            x = self.body[0].x + 1
            y = self.body[0].y
            run = True

            while valid(x, y) and run:
                for i in range(1, len(self.body[1:]) + 1):
                    if x == self.body[i].x and y == self.body[i].y:
                        d = x - self.body[0].x - 1
                        run = False
                        break
                x += 1
            output.append(min(d, (40 - self.body[0].x - 1)))

            # (Forward Right)
            d = 100
            x = self.body[0].x + 1
            y = self.body[0].y - 1
            run = True

            while valid(x, y) and run:
                for i in range(1, len(self.body[1:]) + 1):
                    if x == self.body[i].x and y == self.body[i].y:
                        d = distance(self.body[0].x, x, self.body[0].y, y)
                        run = False
                        break
                y -= 1
                x += 1
            output.append(min(d, (distance(self.body[0].x, 40, self.body[0].y, 0))))

            # (Forward)
            d = 100
            x = self.body[0].x
            y = self.body[0].y - 1
            run = True

            while valid(x, y) and run:
                for i in range(1, len(self.body[1:]) + 1):
                    if x == self.body[i].x and y == self.body[i].y:
                        d = self.body[0].y - y - 1
                        run = False
                        break
                y -= 1
            output.append(min(d, self.body[0].y))

            # (Forward Left)
            d = 100
            x = self.body[0].x - 1
            y = self.body[0].y - 1
            run = True

            while valid(x, y) and run:
                for i in range(1, len(self.body[1:]) + 1):
                    if x == self.body[i].x and y == self.body[i].y:
                        d = distance(self.body[0].x, x, self.body[0].y, y)
                        run = False
                        break
                x -= 1
                y -= 1
            output.append(min(d, (distance(self.body[0].x, 0, self.body[0].y, 0))))

            # (Left)
            d = 100
            x = self.body[0].x - 1
            y = self.body[0].y
            run = True

            while valid(x, y) and run:
                for i in range(1, len(self.body[1:]) + 1):
                    if x == self.body[i].x and y == self.body[i].y:
                        d = self.body[0].x - x - 1
                        run = False
                        break
                x -= 1
            output.append(min(d, self.body[0].x))
        
        return output

