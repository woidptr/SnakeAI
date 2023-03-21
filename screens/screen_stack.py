from .screen import Screen


class ScreenStack:
    screen = Screen
    
    @staticmethod
    def push_screen(new_screen: Screen):
        ScreenStack.screen = new_screen
    
    @staticmethod
    def get_current_screen() -> Screen:
        return ScreenStack.screen