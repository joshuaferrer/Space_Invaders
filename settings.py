class Settings:
    """ A class to store all settings for Alien Invasion """

    def __init__(self):
        """ Initialize the game's static settings """
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 700
        self.bg_color = (20, 20, 20)

        # Ship settings
        self.ship_limit = 3

        # Bullet settings
        self.bullet_width = 15
        self.bullet_height = 30
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 5

        # Alien settings
        self.fleet_drop_speed = 20

        # How quickly the game speeds up
        self.speedup_scale = 1.15
        # How quickly the alien point values increase
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """ Initialize settings that change throughout the game """
        self.ship_speed_factor = 3.5
        self.bullet_speed_factor = 10.0
        self.alien_speed_factor = 3.0

        # fleet direction of 1 represents right; -1 represents left
        self.fleet_direction = 1

        # Scoring
        self.alien1_points = 40
        self.alien2_points = 20
        self.alien3_points = 10
        self.ufo_points = 500

    def increase_speed(self):
        """ Increase speed settings and alien point values """
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien1_points = int(self.alien1_points * self.score_scale)
        self.alien2_points = int(self.alien2_points * self.score_scale)
        self.alien3_points = int(self.alien3_points * self.score_scale)
