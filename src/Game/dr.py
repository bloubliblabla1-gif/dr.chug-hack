from Images import images
import pygame
class dr:
    def __init__(self, main_screen_manager):
        self.main_screen_manager = main_screen_manager
        self.image = images["File_explorer"]
        self.x=100
        self.y=100
        self.mask = pygame.mask.from_surface(self.image)
