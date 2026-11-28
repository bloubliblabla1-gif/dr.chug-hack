from Images import images
import pygame
class dr:
    def __init__(self, main_screen_manager,game):
        self.main_screen_manager = main_screen_manager
        self.image = images["File_explorer"]
        self.x=100
        self.y=100
        self.mask = pygame.mask.from_surface(self.image)
        self.game = game

    def update(self):
        self.main_screen_manager.blit(self.x, self.y, self.image)
        walk_speed_mult = 2
        if self.y > 0 + self.game.delta_multiplier * walk_speed_mult:
            if self.game.keys[pygame.K_W]:
                self.y -= self.game.delta_multiplier * walk_speed_mult

        if self.main_screen_manager.screen_Y > self.y + self.game.delta_multiplier * walk_speed_mult:
            if self.game.keys[pygame.K_S]:
                self.y += self.game.delta_multiplier * walk_speed_mult

        if self.x > 0 + self.game.delta_multiplier * walk_speed_mult:
            if self.game.keys[pygame.K_A]:
                self.x -= self.game.delta_multiplier * walk_speed_mult

        if self.main_screen_manager.screen_X > self.x + self.game.delta_multiplier * walk_speed_mult:
            if self.game.keys[pygame.K_D]: 
                self.x += self.game.delta_multiplier * walk_speed_mult