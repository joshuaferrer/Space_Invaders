import pygame
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Play, HighScore, Back
from ship import Ship
from menu import Menu
import game_functions as gf
from pygame.sprite import Group


def run_game():
    # Initialize pygame, settings, and create a screen object
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # Make an instance of Play button and high scores button
    play_button = Play(ai_settings, screen, "Play Space Invaders")
    high_scores = HighScore(ai_settings, screen, "High Scores")
    home_button = Back(ai_settings, screen, "Back to Home")
    main_menu = Menu(ai_settings, screen)

    # Create an instance to store game statistics and create a scoreboard
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # Make a ship, group of bullets, and group of aliens
    ship = Ship(ai_settings, screen)
    bullets = Group()
    alien1 = Group()
    alien2 = Group()
    alien3 = Group()
    bunkers = Group()
    ufo = Group()

    # Create a fleet of aliens
    gf.create_fleet(ai_settings=ai_settings, screen=screen, ship=ship, alien1=alien1, alien2=alien2, alien3=alien3)

    # Create bunkers
    gf.create_bunker_row(ai_settings=ai_settings, screen=screen, bunkers=bunkers)

    # Set up sounds
    pygame.mixer.music.load('sounds/bg_music.wav')
    music_playing = False

    # Start the main loop for the game
    while True:
        if not music_playing:
            pygame.mixer.music.play(-1, 0.0)
            music_playing = True
        gf.check_events(ai_settings=ai_settings, screen=screen, main_menu=main_menu,
                        stats=stats, sb=sb, play_button=play_button, high_scores=high_scores, home_button=home_button,
                        ship=ship, alien1=alien1, alien2=alien2, alien3=alien3, bullets=bullets)
        if stats.game_active:
            gf.create_ufo(ai_settings=ai_settings, screen=screen, ufo=ufo)
            ship.update()
            gf.update_bullets(ai_settings=ai_settings, screen=screen, stats=stats, sb=sb,
                              ship=ship, alien1=alien1, alien2=alien2, alien3=alien3,
                              bullets=bullets, bunkers=bunkers, ufo=ufo)
            gf.update_aliens(ai_settings=ai_settings, screen=screen, stats=stats, sb=sb,
                             ship=ship, alien1=alien1, alien2=alien2, alien3=alien3,
                             ufo=ufo, bullets=bullets, music_playing=music_playing)

        gf.update_screen(ai_settings=ai_settings, screen=screen, stats=stats, sb=sb, ship=ship,
                         bunkers=bunkers, alien1=alien1, alien2=alien2, alien3=alien3, ufo=ufo,
                         bullets=bullets, main_menu=main_menu, high_scores=high_scores)


run_game()

