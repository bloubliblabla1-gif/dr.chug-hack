import pygame
import Images

class object:
    def __init__(self, type, main_screen_manager, x, y):
        self.type = object_type
        self.main_screen_manager = main_screen_manager
        self.image = Images.images[self.object_type]
        
    def update(self,):
        self.main_screen_manager.blit(self.x, self.y, self.image)
        if self.object_type == "meteor":
            self.y += 1
            look_for_collisons(5)

    def should_delete(self):
        if self.should_delete_var:
            return True