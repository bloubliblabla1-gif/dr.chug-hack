import pygame
import images
class tile:
    def __init__(self,type,main_screen_manager,x,y):
        self.type = type
        self.main_screen_manager = main_screen_manager
        self.x = x * images.tile_size
        self.y = y * images.tile_size
        if self.type == "spawn":
            self.image = images.spawn_tile_surface
            self.max_dura = "N/a"
        elif self.type == "spike":
            self.image = images.spike_tile_surface
            self.max_dura = "N/a"
        elif images.get_random_surface_from_desktop() is not None:
            if self.type == "weak":
                self.image = images.get_random_surface_from_desktop()
                self.max_dura = 2
            if self.type == "strong":
                self.image = images.get_random_surface_from_desktop()
                self.max_dura = 5
        self.current_dura = self.max_dura
    def update(self, camera):
        self.main_screen_manager.blit(self.x - camera.x, self.y - camera.y, self.image)
