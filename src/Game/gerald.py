from Images import images
import random
class gerald:
    def __init__(self, main_screen_manager,game):
        self.main_screen_manager = main_screen_manager
        self.game = game
        self.image = images["gerald_idle"]
        self.x = main_screen_manager.width / 2 - self.image.get_width() / 2
        self.y = main_screen_manager.height / 2 - self.image.get_height() / 2
        self.phase = "idle"
        self.phase_lengths = {
            "idle": 90,
            "sun": 150,
            "zone_cutoff": 210,
            "ray": 210,
            "moon": 150,
            "falling_from_sky": 270,
        }
        self.time_since_last_phase = 0
        self.phases_images = {
            "idle": images["idle"],
            "sun": images["sun"],
            "zone_cutoff": images["zone_cutoff"],
            "ray": images["ray"],
            "moon": images["moon"],
            "falling_from_sky": images["falling_from_sky"],
        }
    def update(self,delta_multiplier):
        self.main_screen_manager.blit(self.x, self.y, self.image)
        self.time_since_last_phase += (1/60) * delta_multiplier
        if self.time_since_last_phase >= self.phase_lengths[self.phase]:
            self.time_since_last_phase = 0
            self.phase = random.choice(list(self.phases_images.keys()))
            self.image = self.phases_images[self.phase]
        if self.phase == "falling_from_sky" and self.time_since_last_phase >= 30:
            if round(self.time_since_last_phase) % 30 == 0:
                self.game.summon_meteor()
        if self.phase == "moon" and self.time_since_last_phase >= 30:
            if round(self.time_since_last_phase) % 20 == 0:
                self.game.summon_moon()
        if self.phase == "ray" and self.time_since_last_phase >= 30:
            if round(self.time_since_last_phase) == 31:
                self.game.summon_ray()
        if self.phase == "zone_cutoff" and self.time_since_last_phase >= 30:
            if (round(self.time_since_last_phase) - 30) % 60 == 0:
                self.game.summon_zone_cutoff()
        if self.phase == "sun" and self.time_since_last_phase >= 30:
            if round(self.time_since_last_phase) % 20 == 0:
                self.game.summon_sun()