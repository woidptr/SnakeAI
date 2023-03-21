from .screen import Screen

# Inspired by minecraft (my sanity is probably lost...)
class ScreenStack:
    screen = Screen
    
    # yes, this is python
    @staticmethod
    def push_screen(new_screen: Screen):
        ScreenStack.screen = new_screen
    
    # yep, this is still python
    @staticmethod
    def get_current_screen() -> Screen:
        return ScreenStack.screen