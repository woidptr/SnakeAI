from pygame import Vector2

from screens.screen import Screen
from screens.screen_stack import ScreenStack
from screens import start_screen
from screens.font_repo import FontRepository

from ui.button import Button


class EndScreen(Screen):
    def render(self):
        self.screen.fill((66, 69, 73))

        screen_rect = self.screen.get_rect()

        if not self.brain.replay:
            line_1 = FontRepository.fixel_20.render("Training finished successfully!", True, (255, 255, 255))
            line_2 = FontRepository.fixel_20.render("Saved the data to the 'checkpoint.pickle'", True, (255, 255, 255))

            self.screen.blit(line_1, ((screen_rect.width / 2) - (line_1.get_size()[0] / 2), 200))
            self.screen.blit(line_2, ((screen_rect.width / 2) - (line_2.get_size()[0] / 2), 230))
        else:
            line_1 = FontRepository.fixel_20.render("Replay has ended!", True, (255, 255, 255))

            self.screen.blit(line_1, ((screen_rect.width / 2) - (line_1.get_size()[0] / 2), 230))

        back_button = Button(
            "Back",
            Vector2((screen_rect.width / 2) - (400 / 2), (screen_rect.height / 2) - (40 / 2)),
            Vector2(400, 40),
            (106, 117, 155),
            self.screen,
            lambda: ScreenStack.push_screen(start_screen.StartScreen(self.screen, self.brain))
        )

        back_button.draw()