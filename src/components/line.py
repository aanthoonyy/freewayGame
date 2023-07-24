import pygame

class lineHitbox(pygame.sprite.Sprite):
    def __init__(self, color, start_pos, end_pos, width):
        super().__init__()
        self.image = pygame.Surface((abs(end_pos[0] - start_pos[0]), width))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = start_pos
        #self.name = name
    def update(self):
        return None