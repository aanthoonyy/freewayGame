import random
import pygame

import src.services.musicService
import src.services.drawTextService
from src.utils.config import Config
from game import playGame
from src.components.score import readHighScore
from src.services.musicService import MusicService
#import src.components.drawMenuClass
from src.components.drawMenuClass import drawMenu

pygame.init()

screen = pygame.display.set_mode((Config.WIDTH, Config.HEIGHT))
pygame.display.set_caption("Highway Runner - Menu")

def main_menu():
    running = True
    scroll_y = 0
    clock = pygame.time.Clock()

    while running:

        elapsed_time = clock.tick(Config.FPS) / 1000
        scroll_distance = -20 * elapsed_time

        scroll_y += scroll_distance


        if scroll_y >= Config.HEIGHT *2:
            scroll_y = 0

        #play_rect = src.components.drawMenuClass.drawtext(screen, scroll_y)
        play_rect = src.components.drawMenuClass.drawMenu.draw_menu(None, screen, scroll_y)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:

                src.services.musicService.MusicService.getMenuClickSound()
                playGame()

        pygame.display.update()
main_menu()

pygame.quit()
