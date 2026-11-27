import pygame

class screen_manager:
    def __init__(self,screen):
        self.screen = screen
        self.screen_X = screen.get_width()
        self.screen_Y = screen.get_height()
        self.texts = []

    def blit(self, x, y, surface):
        self.screen.blit(surface, (x, y))
    def display_text(self, text, x, y, size, time):
        text = text(text, x, y, size, basetime=time)
        self.texts.append(text)

    def update_screen_manager(self):
        pass

class text():
    def __init__(self, text, x, y, size, basetime=2):
        self.text = text



        
        self.font1 = pygame.font.SysFont(None, size)
        text_surface = self.font1.render(self.text, True, (0, 0, 0))
        self.screen.blit(text_surface, (35, 385))
