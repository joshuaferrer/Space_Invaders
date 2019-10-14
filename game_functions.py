import pygame, sys, random
import json
from time import sleep
from bullet import Bullet
from alien import Alien, Alien1, Alien2, Alien3
from menu import Menu
from bunkers import Bunker
from ufo import UFO
import pygame.font
from pygame.sprite import Group


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """ Respond to keypresses """
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings=ai_settings, screen=screen, ship=ship, bullets=bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    """ Respond to key releases """
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, main_menu, stats, sb, play_button, high_scores, home_button,
                 ship, alien1, alien2, alien3, bullets):
    """ Respond to keypresses and mouse events """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event=event, ai_settings=ai_settings, screen=screen, ship=ship, bullets=bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event=event, ship=ship)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings=ai_settings, screen=screen, stats=stats, sb=sb, play_button=play_button,
                              high_scores=high_scores, ship=ship, alien1=alien1, alien2=alien2, alien3=alien3,
                              bullets=bullets, mouse_x=mouse_x, mouse_y=mouse_y)
            check_scores_button(stats=stats, main_menu=main_menu, high_scores=high_scores, mouse_x=mouse_x, mouse_y=mouse_y)
            check_home_button(stats=stats, main_menu=main_menu, home_button=home_button, high_scores=high_scores, mouse_x=mouse_x, mouse_y=mouse_y)


def check_play_button(ai_settings, screen, stats, sb, play_button, high_scores, ship,
                      alien1, alien2, alien3, bullets, mouse_x, mouse_y):
    """ Start a new game when the player clicks Play """
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active and not high_scores.high_score:
        # Reset the game settings
        ai_settings.initialize_dynamic_settings()

        # Hide the mouse cursor
        pygame.mouse.set_visible(False)

        # Reset the game statistics
        stats.reset_stats()
        stats.game_active = True

        # Reset the scoreboard images
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # Empty the list of aliens and bullets
        alien1.empty()
        alien2.empty()
        alien3.empty()
        bullets.empty()

        # Create a new fleet and center the ship
        create_fleet(ai_settings=ai_settings, screen=screen, ship=ship, alien1=alien1, alien2=alien2, alien3=alien3)
        ship.center_ship()


def check_scores_button(stats, main_menu, high_scores, mouse_x, mouse_y):
    """ List high scores if button clicked """
    button_clicked = high_scores.rect.collidepoint(mouse_x, mouse_y)

    # if high scores button clicked, set flag to True to take to high scores screen
    if button_clicked and not stats.game_active:
        high_scores.high_score = True
        main_menu.home = False


def check_home_button(stats, main_menu, home_button, high_scores, mouse_x, mouse_y):
    """ Go back to the main menu """
    button_clicked = home_button.rect.collidepoint(mouse_x, mouse_y)

    if button_clicked and not stats.game_active:
        main_menu.home = True
        high_scores.high_score = False

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, alien1, alien2, alien3, bullets, bunkers, ufo):
    """ Respond to bullet-alien collisions """

    die = pygame.mixer.Sound('sounds/kill.wav')

    # Remove any bullets and aliens that have collided
    collisions_1 = pygame.sprite.groupcollide(bullets, alien1, True, True)
    collisions_2 = pygame.sprite.groupcollide(bullets, alien2, True, True)
    collisions_3 = pygame.sprite.groupcollide(bullets, alien3, True, True)
    collisions_bunkers = pygame.sprite.groupcollide(bullets, bunkers, True, True)
    collisions_ufo = pygame.sprite.groupcollide(bullets, ufo, True, True)

    if collisions_1:
        die.play()
        for aliens in collisions_1.values():
            stats.score += ai_settings.alien1_points * len(aliens)
            sb.prep_score()
        check_high_score(stats=stats, sb=sb)
    if collisions_2:
        die.play()
        for aliens in collisions_2.values():
            stats.score += ai_settings.alien2_points * len(aliens)
            sb.prep_score()
        check_high_score(stats=stats, sb=sb)
    if collisions_3:
        die.play()
        for aliens in collisions_3.values():
            stats.score += ai_settings.alien3_points * len(aliens)
            sb.prep_score()
        check_high_score(stats=stats, sb=sb)
    if collisions_ufo:
        die.play()
        for aliens in collisions_ufo.values():
            stats.score += ai_settings.ufo_points * len(aliens)
            sb.prep_score()
        check_high_score(stats=stats, sb=sb)

    if len(alien1) == 0 and len(alien2) == 0 and len(alien3) == 0:
        # If entire fleet is destroyed, start new level
        # Destroy existing bullets, speed up game, and create new fleet
        bullets.empty()
        ufo.empty()
        ai_settings.increase_speed()

        # Increase level
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings=ai_settings, screen=screen, ship=ship, alien1=alien1, alien2=alien2, alien3=alien3)


def check_fleet_edges(ai_settings, alien1, alien2, alien3):
    """ Respond appropriately if any aliens have reached an edge """
    direction = ai_settings.fleet_direction
    for alien in alien1.sprites():
        if alien.check_edges() and direction == ai_settings.fleet_direction:
            change_fleet_direction(ai_settings=ai_settings, alien1=alien1, alien2=alien2, alien3=alien3)
            break
    for alien in alien2.sprites():
        if alien.check_edges() and direction == ai_settings.fleet_direction:
            change_fleet_direction(ai_settings=ai_settings, alien1=alien1, alien2=alien2, alien3=alien3)
            break
    for alien in alien3.sprites():
        if alien.check_edges() and direction == ai_settings.fleet_direction:
            change_fleet_direction(ai_settings=ai_settings, alien1=alien1, alien2=alien2, alien3=alien3)
            break


def change_fleet_direction(ai_settings, alien1, alien2, alien3):
    """ Drop the entire fleet and change the fleet's direction """
    for alien in alien1.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    for alien in alien2.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    for alien in alien3.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, alien1, alien2, alien3, bullets, music_playing):
    """ Check if any aliens have reached the bottom of the screen """
    screen_rect = screen.get_rect()
    for alien in alien1.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit
            ship_hit(ai_settings=ai_settings, screen=screen, stats=stats, sb=sb, ship=ship,
                     alien1=alien1, alien2=alien2, alien3=alien3, bullets=bullets, music_playing=music_playing)
            break
    for alien in alien2.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit
            ship_hit(ai_settings=ai_settings, screen=screen, stats=stats, sb=sb, ship=ship,
                     alien1=alien1, alien2=alien2, alien3=alien3, bullets=bullets, music_playing=music_playing)
            break
    for alien in alien3.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit
            ship_hit(ai_settings=ai_settings, screen=screen, stats=stats, sb=sb, ship=ship,
                     alien1=alien1, alien2=alien2, alien3=alien3, bullets=bullets, music_playing=music_playing)
            break


def create_alien(ai_settings, screen, alien1, alien2, alien3, alien_number, row_number):
    """ Create an alien and place it in the row """
    if row_number < 2:
        alien = Alien1(ai_settings=ai_settings, screen=screen)
    elif 2 <= row_number < 4:
        alien = Alien2(ai_settings=ai_settings, screen=screen)
    else:
        alien = Alien3(ai_settings=ai_settings, screen=screen)

    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 50 * row_number

    # place created alien in appropriate group
    if row_number < 2:
        alien1.add(alien)
    elif 2 <= row_number < 4:
        alien2.add(alien)
    else:
        alien3.add(alien)


def check_high_score(stats, sb):
    """ Check to see if there's a new high score """
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def create_fleet(ai_settings, screen, ship, alien1, alien2, alien3):
    """ Create a full fleet of aliens. """
    # Create an alien and find the number of aliens in a row
    # Spacing between each alien is equal to one alien width
    alien = Alien1(ai_settings=ai_settings, screen=screen)
    number_aliens_x = get_number_aliens_x(ai_settings=ai_settings, alien_width=alien.rect.width)
    number_rows = get_number_rows(ai_settings=ai_settings, ship_height=ship.rect.height, alien_height=alien.rect.height)

    # Create the fleet of aliens
    for row_number in range(number_rows):
        if row_number < 2:
            for alien_number in range(number_aliens_x):
                create_alien(ai_settings=ai_settings, screen=screen, alien1=alien1, alien2=alien2, alien3=alien3,
                             alien_number=alien_number, row_number=row_number)
        elif 2 <= row_number < 4:
            for alien_number in range(number_aliens_x):
                create_alien(ai_settings=ai_settings, screen=screen, alien1=alien1, alien2=alien2, alien3=alien3,
                             alien_number=alien_number, row_number=row_number)
        else:
            for alien_number in range(number_aliens_x):
                create_alien(ai_settings=ai_settings, screen=screen, alien1=alien1, alien2=alien2, alien3=alien3,
                             alien_number=alien_number, row_number=row_number)


def create_bunker(ai_settings, screen, bunkers, bunker_number):
    """ Create a bunker """
    # Spacing between bunkers is equal to two bunker widths
    bunker = Bunker(ai_settings=ai_settings, screen=screen)
    bunker_width = bunker.rect.width
    bunker.x = bunker_width + 2.25 * bunker_width * bunker_number
    bunker.rect.x = bunker.x
    bunker.rect.y = 515
    bunkers.add(bunker)


def create_bunker_row(ai_settings, screen, bunkers):
    """ Create a row of bunkers """
    # Spacing between bunkers is equal to two bunker widths
    bunker = Bunker(ai_settings=ai_settings, screen=screen)
    number_bunkers = get_number_bunkers(ai_settings=ai_settings, bunker_width=bunker.rect.width)
    for bunker_number in range(number_bunkers):
        create_bunker(ai_settings=ai_settings, screen=screen, bunkers=bunkers, bunker_number=bunker_number)


def create_ufo(ai_settings, screen, ufo):
    interval = random.randint(0, 500)
    if interval == 10:
        ufo_random = UFO(ai_settings=ai_settings, screen=screen)
        if len(ufo) < 1:
            ufo.add(ufo_random)


def fire_bullet(ai_settings, screen, ship, bullets):
    """ Fire a bullet if limit not reached """
    # sounds for bullets
    shoot = pygame.mixer.Sound('sounds/laser.wav')

    # Create a new bullet and add it to the bullets group
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings=ai_settings, screen=screen, ship=ship)
        bullets.add(new_bullet)
        shoot.play()

def get_number_aliens_x(ai_settings, alien_width):
    """ Determine the number of aliens that fit in a row """
    available_space_x = ai_settings.screen_width - 5 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_bunkers(ai_settings, bunker_width):
    """ Determine the number of bunkers that fit in a row """
    available_space = ai_settings.screen_width - 2 * bunker_width
    number_bunkers = int(available_space / (2 * bunker_width))
    return number_bunkers


def get_number_rows(ai_settings, ship_height, alien_height):
    """ Determine the number of rows of aliens that fit on the screen """
    available_space_y = (ai_settings.screen_height -
                         (2 * alien_height) - ship_height)
    number_rows = int(available_space_y / (1.5 * alien_height))
    return number_rows


def ship_hit(ai_settings, screen, stats, sb, ship, alien1, alien2, alien3, bullets, bunkers, ufo, music_playing):
    """ Respond to ship being hit by alien """
    explosion = pygame.mixer.Sound('sounds/explosion.wav')
    pygame.mixer.music.stop()
    music_playing = False
    if stats.ships_left > 0:
        # Decrement ships_left
        stats.ships_left -= 1

        # Update scoreboard
        sb.prep_ships()

        # Empty the list of aliens and bullets
        alien1.empty()
        alien2.empty()
        alien3.empty()
        ufo.empty()
        bullets.empty()

        # Create a new fleet and center the ship
        create_fleet(ai_settings=ai_settings, screen=screen, ship=ship, alien1=alien1, alien2=alien2, alien3=alien3)
        create_bunker_row(ai_settings=ai_settings, screen=screen, bunkers=bunkers)
        ship.center_ship()

        # Pause
        explosion.play()
        sleep(1.0)
        pygame.mixer.music.play(-1, 0.0)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def update_screen(ai_settings, screen, stats, sb, ship, bunkers,
                  alien1, alien2, alien3, ufo, bullets, main_menu, high_scores):
    """ Update images on the screen and flip to the new screen """
    # Redraw the screen during each pass through the loop
    screen.fill(ai_settings.bg_color)

    # Redraw all bullets behind ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    ufo.draw(screen)
    alien1.draw(screen)
    alien2.draw(screen)
    alien3.draw(screen)

    # Draw the bunkers
    bunkers.draw(screen)

    # Draw the score information
    sb.show_score()

    # Draw the play button if the game is inactive
    if not stats.game_active and not high_scores.high_score and main_menu.home == True:
        main_menu.draw_main_menu()

    if not stats.game_active and high_scores.high_score:
        main_menu.draw_high_scores()

    # Make the most recently drawn screen visible
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, alien1, alien2, alien3,
                   bullets, bunkers, ufo):
    """ Update position of bullets and get rid of old bullets """
    # Update bullet positions
    bullets.update()

    # Get rid of bullets that have disappeared
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings=ai_settings,screen=screen, stats=stats, sb=sb, ship=ship,
                                  alien1=alien1, alien2=alien2, alien3=alien3, bullets=bullets, bunkers=bunkers, ufo=ufo)


def update_aliens(ai_settings, screen, stats, sb, ship, alien1, alien2, alien3, ufo, bullets, bunkers, music_playing):
    """ Check if the fleet is at an edge,
        and then update the positions of all aliens in the fleet """
    check_fleet_edges(ai_settings=ai_settings, alien1=alien1, alien2=alien2, alien3=alien3)
    alien1.update()
    alien2.update()
    alien3.update()
    ufo.update()

    # Get rid of ufos that are outside of the screen
    for ufos in ufo.copy():
        if ufos.rect.left > ai_settings.screen_width:
            ufo.remove(ufos)

    # Look for alien-ship collisions
    if pygame.sprite.spritecollideany(ship, alien1):
        ship_hit(ai_settings=ai_settings, screen=screen, stats=stats, sb=sb, ship=ship, bunkers=bunkers,
                 alien1=alien1, alien2=alien2, alien3=alien3, bullets=bullets, ufo=ufo, music_playing=music_playing)
    if pygame.sprite.spritecollideany(ship, alien2):
        ship_hit(ai_settings=ai_settings, screen=screen, stats=stats, sb=sb, ship=ship, bunkers=bunkers,
                 alien1=alien1, alien2=alien2, alien3=alien3, bullets=bullets, ufo=ufo, music_playing=music_playing)
    if pygame.sprite.spritecollideany(ship, alien3):
        ship_hit(ai_settings=ai_settings, screen=screen, stats=stats, sb=sb, ship=ship, bunkers=bunkers,
                 alien1=alien1, alien2=alien2, alien3=alien3, bullets=bullets, ufo=ufo, music_playing=music_playing)

    # Look for aliens hitting the bottom of the screen
    check_aliens_bottom(ai_settings=ai_settings, screen=screen, stats=stats, sb=sb, ship=ship,
                        alien1=alien1, alien2=alien2, alien3=alien3, bullets=bullets, music_playing=music_playing)


