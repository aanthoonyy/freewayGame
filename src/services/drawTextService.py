import pygame
from src.utils.config import Config
class drawtext():

    def drawText(screen, color, txtSize, msg, posx, posy):
        font = pygame.font.Font('data/assets/VCR_OSD_MONO_1.001.ttf', txtSize)
        text = font.render(msg, True, color, None)
        textRect = text.get_rect()
        textRect.center = (posx, posy)
        screen.blit(text, textRect)
