import pygame.font
from button import HighScore, Play, Back
import json


class Menu:

    def __init__(self, ai_settings, screen):
        """ Initialize screen attributes """
        self.ai_settings = ai_settings
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.home = True

        # Set menu attributes
        self.bg_color = (20, 20, 20)
        self.text1_color = (255, 255, 255)
        self.text2_color = (0, 255, 0)
        self.header_font = pygame.font.SysFont(None, 100)
        self.body_font = pygame.font.SysFont(None, 48)
        self.width, self.height = 300, 100

    def draw_main_menu(self):
        self.screen.fill(self.bg_color)

        # Draw Title
        self.title1 = self.header_font.render("SPACE", True, self.text1_color, self.bg_color)
        self.title1_rect = self.title1.get_rect()
        self.title1_rect.centerx = self.screen_rect.centerx
        self.title1_rect.centery = 90
        self.screen.blit(self.title1, self.title1_rect)
        self.title2 = self.header_font.render("INVADERS", True, self.text2_color, self.bg_color)
        self.title2_rect = self.title2.get_rect()
        self.title2_rect.centerx = self.screen_rect.centerx
        self.title2_rect.centery = 150
        self.screen.blit(self.title2, self.title2_rect)

        # Draw Alien types and scores
        self.enemy3 = pygame.transform.scale(pygame.image.load('images/Alien3_1.png'), (100, 100))
        self.enemy2 = pygame.transform.scale(pygame.image.load('images/Alien2_1.png'), (100, 120))
        self.enemy1 = pygame.transform.scale(pygame.image.load('images/Alien1_1.png'), (100, 100))
        self.ufo = pygame.transform.scale(pygame.image.load('images/ufo.png'), (100, 100))
        self.screen.blit(self.enemy3, (400, 190))
        self.screen.blit(self.enemy2, (400, 270))
        self.screen.blit(self.enemy1, (400, 350))
        self.screen.blit(self.ufo, (400, 440))
        self.score3 = self.body_font.render(" =    10 PTS", True, self.text1_color, self.bg_color)
        self.score2 = self.body_font.render(" =    20 PTS", True, self.text1_color, self.bg_color)
        self.score1 = self.body_font.render(" =    40 PTS", True, self.text1_color, self.bg_color)
        self.score_ufo = self.body_font.render(" =     ???", True, self.text1_color, self.bg_color)
        self.screen.blit(self.score3, (530, 230))
        self.screen.blit(self.score2, (530, 310))
        self.screen.blit(self.score1, (530, 390))
        self.screen.blit(self.score_ufo, (530, 470))

        # Button to start gameplay
        play_button = Play(self.ai_settings, self.screen, "Play Space Invaders")
        play_button.draw_button()

        # Button to view High scores
        high_scores = HighScore(self.ai_settings, self.screen, "High Scores")
        high_scores.draw_button()

    def draw_high_scores(self):
        self.screen.fill(self.bg_color)
        scores_height = 150
        number = 1

        # play button and back to home screen
        play_button = Back(self.ai_settings, self.screen, "Back to Home")
        play_button.draw_button()

        # Display Header
        header = self.header_font.render("High Scores", True, (255, 255, 255), (20, 20, 20))
        screen_rect = self.screen.get_rect()
        header_rect = header.get_rect()
        header_rect.centerx = screen_rect.centerx
        header_rect.centery = 90
        self.screen.blit(header, header_rect)

        # Display scores saved from JSON file
        high_scores = self.get_high_scores()
        for score in high_scores:
            display_names = self.body_font.render(json.dumps(score["name"]), True, (255, 0, 0), (20, 20, 20))
            display_scores = self.body_font.render(json.dumps(score["score"]), True, (255, 0, 0), (20, 20, 20))
            display_number = self.body_font.render(str(number) + '.', True, (255, 255, 255), (20, 20, 20))
            names_rect = display_names.get_rect()
            scores_rect = display_scores.get_rect()
            number_rect = display_number.get_rect()
            names_rect.centerx = screen_rect.centerx - 100
            scores_rect.centerx = screen_rect.centerx + 100
            number_rect.centerx = screen_rect.centerx - 225
            names_rect.centery = scores_height
            scores_rect.centery = scores_height
            number_rect.centery = scores_height
            scores_height += 55
            number += 1
            self.screen.blit(display_names, names_rect)
            self.screen.blit(display_scores, scores_rect)
            self.screen.blit(display_number, number_rect)


    def get_high_scores(self):
        with open('high_scores.json') as file:
            scores = json.load(file)
        return scores

