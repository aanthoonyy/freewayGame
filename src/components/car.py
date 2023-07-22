import random
import pygame
import time
from pygame.locals import *
from moviepy.editor import *
from config import Config

class Car(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("data/assets/car.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (car_x, car_y)
        self.acc = vec(0, 0)
        self.velocity = vec(0, 0)
        self.pos = vec((180, 650))
        self.player_position = vec(0, 0)
        self.lockoutW = False #stops the W key from being used after initial launch
        self.lane_center_x = [85, 182, 273]

    def update(self, elapsed_time):
        self.acc = vec(0, 0)
        deceleration_factor = 90
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.acc.x -= Config.ACC
        if keys[pygame.K_d]:
            self.acc.x += Config.ACC
        if keys[pygame.K_w] and self.lockoutW == False:
            self.acc.y -= Config.ACC

       #if keys[pygame.K_s]:
            #self.acc.y += (Config.ACC)
            #self.velocity *= 0.995


        if not keys[pygame.K_w]:
            deceleration_factor = 0.999 # Adjust this value (0.0 to 1.0) for slower speed loss when 'W' is released
        else:
            deceleration_factor = 0.95  # Adjust this value (0.0 to 1.0) for normal deceleration when 'W' is pressed

        lane_distance = self.pos.x - self.lane_center_x[self.get_nearest_lane()]
        #lane_assist = lane_distance * 0.0001  # Adjust the value to control the strength of the assist
        lane_assist = lane_distance * 0.001  # Adjust the value to control the strength of the assist
        #Lane Assist Values
        # I really like 0.001 for like a mid level

        self.acc.x -= lane_assist


        self.velocity *= deceleration_factor

        self.acc.x += self.velocity.x * Config.FRIC * Config.FRICADJUSTMENT
        #self.acc.y += self.velocity.y * Config.FRIC

        self.velocity += self.acc
        self.pos += self.velocity + 0.5 * self.acc

        self.player_position = self.pos.copy()

        # Limit the maximum speed
        max_speed = 100  # Adjust the maximum speed value as needed
        self.velocity.x = max(-max_speed, min(self.velocity.x, max_speed))
        self.velocity.y = max(-max_speed, min(self.velocity.y, max_speed))

        if self.pos.x > Config.WIDTH:
            self.pos.x = Config.WIDTH
        if self.pos.x < 0:
            self.pos.x = 0
        if self.pos.y > Config.HEIGHT:
            self.pos.y = Config.HEIGHT

        if self.pos.x < 45:
            self.pos.x = 45

        if self.pos.x > 315:
            self.pos.x = 315

        self.rect.center = self.pos

        return -1*(self.velocity.y)




    def get_nearest_lane(self):
        lane_distances = [abs(self.pos.x - lane_x) for lane_x in self.lane_center_x]
        nearest_lane_index = lane_distances.index(min(lane_distances))
        return nearest_lane_index