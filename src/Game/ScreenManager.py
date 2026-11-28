import pygame
from Images import images


class screen_manager:
    def __init__(self, screen):
        self.screen = screen
        self.screen_X = screen.get_width()
        self.screen_Y = screen.get_height()
        self.texts = []
        self.gui_elements = [gui(self, "play"), gui(self, "busy"), gui(self, "banner")]

    def blit(self, x, y, surface):
        self.screen.blit(surface, (x, y))

    def display_text(self, text, x, y, size, time):
        text = text(text, x, y, size, basetime=time)
        self.texts.append(text)

    def update_screen_manager(self,delta_multiplier,game):
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        for text in self.texts:
            if text.update(delta_multiplier) == True:
                self.texts.remove(text)


class text:
    def __init__(self, text, x, y, size, basetime=2):
        self.text = text
        self.x = x
        self.y = y
        self.basetime = basetime
        self.font1 = pygame.font.SysFont(None, size)
        text_surface = self.font1.render(self.text, True, (0, 0, 0))
        self.screen.blit(text_surface, (35, 385))
    def update(self, delta_multiplier):
        self.basetime -= (1/60) * delta_multiplier
        if self.basetime <= 0:
            return True
        else:
            text_surface = self.font1.render(self.text, True, (0, 0, 0))
            self.screen.blit(text_surface, (self.x, self.y))
            return False


class gui:
    def __init__(self, screen_manager,object_type):
        self.screen_manager = screen_manager
        self.image = images[object_type]
        self.mask = pygame.mask.from_surface(self.image)
        self.object_type = object_type
        if object_type == "play":
            self.x = 100
            self.y = 300
        if object_type == "busy":
            self.x = 600
            self.y = 300
        if object_type == "banner":
            self.x = 100
            self.y = 100
        self.screen_manager = screen_manager

    def update(self,game):
        self.screen_manager.blit(self.x, self.y, self.image)
        if self.object_type == "play":
            if self.mask.overlap(self.screen_manager.get_pressed(), (self.x - self.screen_manager.mouse_x, self.y - self.screen_manager.mouse_y)):
                game.start_game()
        if self.object_type == "busy":
            if self.mask.overlap(self.screen_manager.get_pressed(), (self.x - self.screen_manager.mouse_x, self.y - self.screen_manager.mouse_y)):
                game.delay_game()