import random
import pygame
import Images

class object:
    def __init__(self, object_type, main_screen_manager, x, y, player):
        self.object_type = object_type
        self.main_screen_manager = main_screen_manager
        self.image = Images.images[self.object_type]
        self.mask = pygame.mask.from_surface(self.image)
        self.player = player
        self.x = x
        self.y = y
        if self.object_type == "meteor":
            self.x = random.randint(0, main_screen_manager.width - self.image.get_width())
            self.y = 0
            self.damage = 1
    

    def update(self):
        self.main_screen_manager.blit(self.x, self.y, self.image)
        if self.object_type == "meteor":
            self.y += 1
            self.look_for_collisons()


    def look_for_collisons(self):
        if self.mask.overlap(self.player.mask, (self.x - self.player.x, self.y - self.player.y)):
            self.should_delete = True
            self.player.health -= self.damage
        if self.y < 0 or self.y > self.main_screen_manager.height:
            self.should_delete = True
        if self.x < 0 or self.x > self.main_screen_manager.width:
            self.should_delete = True