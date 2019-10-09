import pygame.font


class Button:

    def __init__(self, ai_settings, screen, msg, window_x, window_y):
        """ Initialize button attributes """
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Set the dimensions and properties of the button
        self.width, self.height = 325, 50
        self.button_color = (20, 20, 20)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Build the button's rect object
        self.rect = pygame.Rect(window_x, window_y, self.width, self.height)

        # The button message needs to be prepped only once
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """ Turn msg into a rendered image and center text on the button """
        self.msg_image = self.font.render(msg, True, self.text_color,
                                          self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # Draw blank button and then draw message
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)


class Play(Button):
    """ Play button to inherit from Button class and start the game """
    def __init__(self, ai_settings, screen, msg):
        super().__init__(ai_settings, screen, msg, 425, 540)


class Back(Button):
    """ Play button to inherit from Button class and start the game """
    def __init__(self, ai_settings, screen, msg):
        super().__init__(ai_settings, screen, msg, 0, 0)


class HighScore(Button):
    """ High Score button to inherit from Button Class and list the high scores """
    def __init__(self, ai_settings, screen, msg):
        super().__init__(ai_settings, screen, msg, 425, 595)
        self.high_score = False
