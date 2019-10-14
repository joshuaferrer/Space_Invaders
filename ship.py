import pygame
from pygame.sprite import Sprite
from timer import Timer


class Ship(Sprite):

    def __init__(self, ai_settings, screen):
        """ Initialize the ship and set its starting position """
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.counter = 0
        self.index = 0

        # Load the ship image and get its rect
        self.image = pygame.transform.scale(pygame.image.load('images/spaceship.png'), (80, 80))
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.images = []


        # Start each new ship at the bottom center of screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Store a decimal value for ship's center
        self.center = float(self.rect.centerx)

        # Movement flags
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """ Update the ship's position based on the movement flag """
        # Update the ship's center value, not the rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        # Update the rect object from self.center
        self.rect.centerx = self.center

    def blitme(self):
        """ Draw the ship at its current location """
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """ Center the ship on the screen """
        self.center = self.screen_rect.centerx

    def ship_explosion(self):
        self.images.append(pygame.transform.scale(pygame.image.load('images/spaceship_explosion1.png'), (50, 50)))
        self.images.append(pygame.transform.scale(pygame.image.load('images/spaceship_explosion2.png'), (50, 50)))
        self.images.append(pygame.transform.scale(pygame.image.load('images/spaceship_explosion3.png'), (50, 50)))
        self.images.append(pygame.transform.scale(pygame.image.load('images/spaceship_explosion4.png'), (50, 50)))
        self.images.append(pygame.transform.scale(pygame.image.load('images/spaceship_explosion5.png'), (50, 50)))
        self.images.append(pygame.transform.scale(pygame.image.load('images/spaceship_explosion6.png'), (50, 50)))

        # Increment counter to only update index every 10 ticks, then
        # Increment index for ship image list. If index larger than list, index back to 0
        self.counter += 1
        if self.counter == 10:
            self.counter = 0
            self.index += 1

        if self.index >= len(self.images):
            self.index = 0
            self.image = self.images[2]
        self.screen.blit(self.image, self.rect)
