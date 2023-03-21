import pygame

from screens.font_repo import FontRepository


class Button:
    def __init__(self, text, pos, size, color, display, onclick):
        self.pos = pos
        self.size = size
        self.text = text
        self.color = color
        self.display = display
        self.onclick = onclick

        self.surface = pygame.Surface(size)
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)
    
    def draw(self):
        self.surface.fill(self.color)

        label = FontRepository.fixel_20.render(self.text, True, (255, 255, 255))
        self.surface.blit(label, [
            self.rect.width / 2 - label.get_rect().width / 2,
            self.rect.height / 2 - label.get_rect().height / 2
        ])

        self.display.blit(self.surface, self.rect)

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if self.rect.collidepoint(mouse):
            if click[0]:
                self.onclick()