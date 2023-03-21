import os
import pygame


# I spent too much time reversing minecraft
class FontRepository:
    fixel_20 = None
    fixel_15 = None

    @staticmethod
    def init():
        FontRepository.fixel_20 = pygame.font.Font(os.path.join("resources", "fonts", "FixelMedium.ttf"), 20)
        FontRepository.fixel_15 = pygame.font.Font(os.path.join("resources", "fonts", "FixelMedium.ttf"), 15)