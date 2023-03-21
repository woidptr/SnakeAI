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
            self.screen.fill((66, 69, 73))   # drawing the background

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
                # Rendering text
                generation_label = FontRepository.fixel_20.render(f"Generation: {self.brain.generation}", True, (255, 255, 255))
                self.screen.blit(generation_label, (5, 5))

                highscore_label = FontRepository.fixel_20.render(f"Highscore: {self.brain.highscore}", True, (255, 255, 255))
                self.screen.blit(highscore_label, (5, 25))

            """ for i, snake in enumerate(self.brain.snakes):
                output = self.brain.nets[i].activate(snake.vision())     # activating the neural network

                controls(snake, output)      # controls game based on the output from the neural network

                snake.update()

                if snake.score > highscore:
                    highscore = snake.score

                if snake.check_collision():
                    self.brain.genomes[i][1].fitness += 100      # increase the fitness (fruit eaten)
                    self.brain.frames[i] = 0
                        
                self.brain.frames[i] += 1
                if self.brain.frames[i] >= 100 and len(snake.body) <= 5:
                    snake.failed = True

                if snake.failed:
                    self.brain.genomes[i][1].fitness -= 1000     # lower the fitness (fail)
                    self.brain.snakes.pop(i)
                    self.brain.nets.pop(i) """