import pygame
#from src.services.drawTextService import drawtext
import src.services.drawTextService
from src.utils.config import Config
from src.components.score import readHighScore
pygame.init()

class drawMenu():
    def draw_menu(self, screen, scroll_y):
        screen.fill((255, 255, 255))
        background_image = pygame.image.load("data/assets/menuBackground.png").convert()
        screen.blit(background_image, (0, scroll_y + Config.HEIGHT * 2))
        screen.blit(background_image, (0, scroll_y))

        # drawText(self, screen, color, txtSize, msg):
        src.services.drawTextService.drawtext.drawText(screen, (0, 0, 0), 60, ("FREEWAY"), (Config.WIDTH / 2),
                                                       (Config.HEIGHT / 2) - 185)
        src.services.drawTextService.drawtext.drawText(screen, (0, 0, 0), 60, ("RUNNER"), (Config.WIDTH / 2),
                                                       (Config.HEIGHT / 2) - 131)
        src.services.drawTextService.drawtext.drawText(screen, (255, 255, 255), 60, ("FREEWAY"), (Config.WIDTH / 2),
                                                       (Config.HEIGHT / 2) - 189)
        src.services.drawTextService.drawtext.drawText(screen, (255, 255, 255), 60, ("RUNNER"), (Config.WIDTH / 2),
                                                       (Config.HEIGHT / 2) - 135)

        src.services.drawTextService.drawtext.drawText(screen, (0, 0, 0), 24, ("Press any key!"), (Config.WIDTH / 2),
                                                       (Config.HEIGHT / 2))
        src.services.drawTextService.drawtext.drawText(screen, (255, 255, 255), 24, ("Press any key!"),
                                                       (Config.WIDTH / 2) - 2, (Config.HEIGHT / 2) - 2)

        src.services.drawTextService.drawtext.drawText(screen, (0, 0, 0), 22,
                                                       ("High Score: " + src.components.score.readHighScore()), 100 + int(len(src.components.score.readHighScore())), 610)

        src.services.drawTextService.drawtext.drawText(screen, (255, 255, 255), 22,
                                                       ("High Score: " + src.components.score.readHighScore()), 98 + int(len(src.components.score.readHighScore())), 608)