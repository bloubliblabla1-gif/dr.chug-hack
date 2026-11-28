import Tiles
class game:
    def __init__(self, screen_manager):
        self.screen_manager = screen_manager
        self.survived_time = 0
        self.objects = []

    def update_game(self, keys, delta_multiplier):
        # Game update logic here
        self.survived_time += (1/60) * delta_multiplier
        if self.survived_time >= 3600:
            self.remove_virus()

        for obj in self.objects:
            obj.update()
            if obj.should_delete():
                self.objects.remove(obj)

    def update(self, keys, delta_multiplier):
        if self.game_started:
            self.update_game(keys, delta_multiplier)

    def start_game(self):
        self.game_started = True

    def delay_game(self):
        # gerald will figure it out
        pass

    def remove_virus(self):
        # u got this, u dont have to remove it just make it shut up
        pass

    def summon_meteor(self):
        self.objects.append(Tiles.object("meteor", self.screen_manager, 0, 0, self.player))

    def summon_moon(self):
        self.objects.append(Tiles.object("moon", self.screen_manager, 0, 0, self.player))

    def summon_ray(self):
        self.objects.append(Tiles.object("ray", self.screen_manager, 0, 0, self.player))

    def summon_zone(self):
        self.objects.append(Tiles.object("zone", self.screen_manager, 0, 0, self.player))

    def summon_sun(self):
        self.objects.append(Tiles.object("sun", self.screen_manager, 0, 0, self.player))