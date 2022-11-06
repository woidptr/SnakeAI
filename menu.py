import os.path
import pygame
import sys


class Button:
    def __init__(self, screen, pos, text):
        self.font = pygame.font.Font(os.path.join("resources", "fonts", "Monocraft.otf"), 20)
        self.screen = screen
        self.x, self.y = pos
        screen_rect = self.screen.get_rect()
        self.screen_center = screen_rect.center
        self.rect = pygame.Rect(self.x, self.y, 300, 70)
        self.rect.center = self.screen_center
        self.text = text

    def draw(self):
        pygame.draw.rect(self.screen, (114, 137, 218), self.rect, 2, 3)
        label = self.font.render(self.text, True, (255, 255, 255))
        label_rect = label.get_rect()
        label_rect.center = self.screen_center
        self.screen.blit(label, (label_rect.center))

    def click(self, event):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
                    print("Test")


def menu(screen):
    while True:
        screen.fill((66, 69, 73))

        mx, my = pygame.mouse.get_pos()

        screen_rect = screen.get_rect()
        screen_center = screen_rect.center

        button = Button(screen, (5, 5), "Start")
        button.draw()

        if button.rect.collidepoint((mx, my)):
            if click:
                break

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()


if __name__ == "__main__":
    menu()