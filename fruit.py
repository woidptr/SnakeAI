import random
import pygame
from pygame import Vector2

cell_size = 15
cell_number = 40


class Fruit():
    """
    Fruit object
    """

    def __init__(self, screen):
        self.screen = screen
        self.reposition()

    def draw_fruit(self):
        """
        Drawing fruit
        """
        fruit_rect = pygame.Rect(self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size)
        pygame.draw.rect(self.screen, (255, 255, 255), fruit_rect)

    def reposition(self):
        """
        Place fruit in a random spot on the map
        """
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)