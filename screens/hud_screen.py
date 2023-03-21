import os
import pygame
from pygame import Vector2

from .screen import Screen
from .font_repo import FontRepository


def controls(snake, output):
    """Controls snake based on the neural network output."""

    if max(output) == output[0]:    # Left
        if snake.direction == Vector2(0, 1):
            snake.direction = Vector2(1, 0)
        elif snake.direction == Vector2(0, -1):
            snake.direction = Vector2(-1, 0)
        elif snake.direction == Vector2(-1, 0):
            snake.direction = Vector2(0, 1)
        elif snake.direction == Vector2(1, 0):
            snake.direction = Vector2(0, -1)
    if max(output) == output[1]:    # Right
        if snake.direction == Vector2(0, 1):
            snake.direction = Vector2(-1, 0)
        elif snake.direction == Vector2(0, -1):
            snake.direction = Vector2(1, 0)
        elif snake.direction == Vector2(-1, 0):
            snake.direction = Vector2(0, -1)
        elif snake.direction == Vector2(1, 0):
            snake.direction = Vector2(0, 1)
    if max(output) == output[2]:    # Forward
        pass


class HudScreen(Screen):
    def render(self):
        if not False:
            self.screen.fill((66, 69, 73))

            for snake in self.brain.snakes:
                snake.draw_elements()
                break

            screen_rect = self.screen.get_rect()

            if self.brain.replay:
                replay_label = FontRepository.fixel_20.render(f"Replay Mode", True, (255, 255, 255))
                replay_label_rect = replay_label.get_rect()
                self.screen.blit(replay_label, (screen_rect.centerx - (replay_label_rect.width / 2), 5))

                """ score = self.brain.snakes[0].score
                score_label = FontRepository.fixel_20.render(f"Score: {score}", True, (255, 255, 255))
                self.screen.blit(score_label, (5, 25)) """
            else:
                generation_label = FontRepository.fixel_20.render(f"Generation: {self.brain.generation}", True, (255, 255, 255))
                self.screen.blit(generation_label, (5, 5))

                highscore_label = FontRepository.fixel_20.render(f"Highscore: {self.brain.highscore}", True, (255, 255, 255))
                self.screen.blit(highscore_label, (5, 25))