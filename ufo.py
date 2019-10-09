import pygame
from pygame.sprite import Sprite


class UFO(Sprite):
    def __init__(self, ai_settings, screen):
        super(UFO, self).__init__()
        """ Initialize the UFO """
        self.ai_settings = ai_settings
        self.screen = screen

        # Load UFO image and get it's rect
        self.images = []
        self.index = 0
        self.images.append(pygame.transform.scale(pygame.image.load('images/UFO.png'), (80, 80)))
        self.images.append(pygame.transform.scale(pygame.image.load('images/UFO_point.png'), (100, 100)))

        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Start each new ufo left of the top left of the screen
        self.rect.x = self.rect.width - 200
        self.rect.y = self.rect.height

        # Store the alien's exact position
        self.x = float(self.rect.x)

    def blitme(self):
        """ Draw the ufo at its current location """
        self.screen.blit(self.image, self.rect)

    def update(self):
        """ Move the UFO to the right """
        # UFO speed is 2x alien speed
        self.x += (self.ai_settings.alien_speed_factor * 2)
        self.rect.x = self.x
