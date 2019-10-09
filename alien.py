import pygame
from pygame.sprite import Sprite
from timer import Timer


class Alien(Sprite):
    """ A class to represent a single alien in the fleet """

    def __init__(self, ai_settings, screen, image):
        """ Initialize the alien and set its starting position """
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.counter = 0

        # Load the alien image and set its rect attribute
        self.image = image
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact position
        self.x = float(self.rect.x)

    def blitme(self):
        """ Draw the alien at its current location """
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        """ Return True if alien is at edge of screen """
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """ Move the alien right or left """
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x

        # Increment counter to only update index every 10 ticks, then
        # Increment index for alien image list. If index larger than list, index back to 0
        self.counter += 1
        if self.counter == 10:
            self.counter = 0
            self.index += 1

        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]


class Alien1(Alien):
    def __init__(self, ai_settings, screen):
        self.images = []
        self.index = 0
        self.images.append(pygame.transform.scale(pygame.image.load('images/Alien1_1.png'), (50, 50)))
        self.images.append(pygame.transform.scale(pygame.image.load('images/Alien1_2.png'), (50, 50)))
        super().__init__(ai_settings, screen, self.images[self.index])


class Alien2(Alien):
    def __init__(self, ai_settings, screen):
        self.images = []
        self.index = 0
        self.images.append(pygame.transform.scale(pygame.image.load('images/Alien2_1.png'), (50, 60)))
        self.images.append(pygame.transform.scale(pygame.image.load('images/Alien2_2.png'), (50, 60)))
        super().__init__(ai_settings, screen, self.images[self.index])


class Alien3(Alien):
    def __init__(self, ai_settings, screen):
        self.images = []
        self.index = 0
        self.images.append(pygame.transform.scale(pygame.image.load('images/Alien3_1.png'), (50, 50)))
        self.images.append(pygame.transform.scale(pygame.image.load('images/Alien3_2.png'), (50, 50)))
        super().__init__(ai_settings, screen, self.images[self.index])
