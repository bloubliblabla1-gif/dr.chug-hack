print("hello world")
def main():
    from ScreenManager import screen_manager
    from Game import game
    import pygame
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    main_screen_manager = screen_manager(screen)
    main_game = game(main_screen_manager)
    delta_multiplier = 1

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main_screen_manager.display_text("nope",100,100,time=5)
        keys = pygame.key.get_pressed()
        if clock.get_fps() > 0:
            delta_multiplier = 60 / clock.get_fps()
        main_screen_manager.update_screen(keys,delta_multiplier)
        main_game.update(keys,delta_multiplier)
        clock.tick(60)
if __name__ == "__main__":
    main()
