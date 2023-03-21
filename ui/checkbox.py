import pygame

from screens.font_repo import FontRepository


class Checkbox:
    def __init__(self, label: str, pos, size, display):
        self.label = label
        self.pos = pos
        self.size = size
        self.display = display
    
    def draw(self) -> bool:
        return False