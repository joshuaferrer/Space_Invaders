import pygame
from pygame.sprite import Sprite


class Bunker(Sprite):
    """ Class to represent single bunker to shield the ship from enemies """

    def __init__(self, ai_settings, screen):
        """ Initialize bunker and set its starting position """
        super(Bunker, self).__init__()
        self.ai_settings = ai_settings
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        # Load bunker image and scale
        self.image = pygame.transform.scale(pygame.image.load('images/bunker.png'), (120, 120))
        self.rect = self.image.get_rect()


    def blitme(self):
        """ Draw the bunker at its current location """
        self.screen.blit(self.image, self.rect)
