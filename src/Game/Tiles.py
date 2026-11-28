import random
import pygame
from Images import images, gfos

class object:
    def __init__(self, object_type, main_screen_manager, x, y, player):
        self.object_type = object_type
        self.main_screen_manager = main_screen_manager
        self.base_image = images[self.object_type]
        self.image = images[self.object_type]
        self.mask = pygame.mask.from_surface(self.image)
        self.player = player
        self.x = x
        self.y = y
        if self.object_type == "meteor":
            self.x = random.randint(0, main_screen_manager.width - self.image.get_width())
            self.y = 0
            self.damage = 1
            self.speed = gfos(60)
        if self.object_type == "moon":
            rand = random.randint(1,4)
            match rand:
                case 1:
                    self.x = (main_screen_manager.screenX)
                    self.y = random.randint(0,main_screen_manager.screenY)
                case 2:
                    self.x = 0
                    self.y = random.randint(0,main_screen_manager.screenY)
                case 3:
                    self.x = random.randint(main_screen_manager.screenX)
                    self.y = (main_screen_manager.screenY)
                case 4:
                    self.x = random.randint(main_screen_manager.screenX)
                    self.y = 0
            self.x
            self.y
            self.image =
            self.mask =
            if self.x < 10 and self.y<10 and self.x > -10 and self.y > -10:
                self.should_delete = True

    def update(self,delta_multiplier):
        self.main_screen_manager.blit(self.x, self.y, self.image)
        if self.object_type == "meteor":
            self.y += self.speed * delta_multiplier
        if self.object_type == "moon":
            self.y += gfos(30) * delta_multiplier
        self.look_for_collisons()


    def look_for_collisons(self):
        if self.mask.overlap(self.player.mask, (self.x - self.player.x, self.y - self.player.y)):
            self.should_delete = True
            self.player.health -= self.damage
        if self.y < 0 or self.y > self.main_screen_manager.height:
            self.should_delete = True
        if self.x < 0 or self.x > self.main_screen_manager.width:
            self.should_delete = True