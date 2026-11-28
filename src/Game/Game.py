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

    def start_game(self):
        print("Game started")

    def delay_game(self):
        # gerald will figure it out
        pass

    def remove_virus(self):
        # u got this, u dont have to remove it just make it shut up
        pass

    def summon_meteor(self):
        self.objects.append(Tiles.object("meteor", self.screen_manager, 0, 0, self.player))