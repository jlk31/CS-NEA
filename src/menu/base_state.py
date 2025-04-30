import pygame

class BaseState:
    def __init__(self, screen):
        self.screen = screen
        
    def event_handler(self, events):
        pass

    def update(self):
        pass

    def render(self):
        pass