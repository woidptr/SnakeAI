from abc import ABC, abstractmethod


class Screen(ABC):
    """Abstract screen class"""

    def __init__(self, screen, brain):
        """Constructing our screen with pygame one included"""
        self.screen = screen
        self.brain = brain

    @abstractmethod
    def render(self):
        pass