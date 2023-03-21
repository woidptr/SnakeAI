import os
import neat
import pygame
from pygame import Vector2
from threading import Thread

from ui.button import Button

from core.brain import Brain
from .screen_stack import ScreenStack
from .screen import Screen
from .hud_screen import HudScreen

from core.replay import ReplayHandler


class StartScreen(Screen):
    def start_new_process(self):
        # Pushing new screen to the stack
        ScreenStack.push_screen(HudScreen(self.screen, self.brain))

        # Running the brain evolution in a different thread
        thread = Thread(target=self.brain.init)
        thread.start()
    
    def start_replay(self):
        p = neat.Checkpointer.restore_checkpoint(f"neat-checkpoint-0")
        self.brain = Brain(p, self.screen, True)

        ScreenStack.push_screen(HudScreen(self.screen, self.brain))

        thread = Thread(target=self.brain.init)
        thread.start()

    def render(self):
        self.screen.fill((66, 69, 73))

        screen_rect = self.screen.get_rect()

        start_button = Button(
            "New Process",
            Vector2((screen_rect.width / 2) - (400 / 2), (screen_rect.height / 6) - (40 / 6)),
            Vector2(400, 40),
            (106, 117, 155),
            self.screen,
            lambda: self.start_new_process()
        )

        from_checkpoint = Button(
            "From Checkpoint",
            Vector2((screen_rect.width / 2) - (400 / 2), (screen_rect.height / 6 + 60) - (40 / 6)),
            Vector2(400, 40),
            (106, 117, 155) if os.path.exists("model.pkl") else (107, 107, 107),
            self.screen,
            lambda: self.start_replay()
        )

        start_button.draw()
        from_checkpoint.draw()