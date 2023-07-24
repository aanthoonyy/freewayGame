import random
import pygame


class Traffic(pygame.sprite.Sprite):

    def __init__(self, lastLaneSpawned, vec):
        pygame.sprite.Sprite.__init__(self)
        x = random.randint(1, 31)
        lastSprite = x
        if lastSprite == x:
            x = random.randint(1, 31)
        self.image = pygame.image.load(f'data/assets/traffic/traffic{x}.png')
        self.rect = self.image.get_rect()
        self.lane = 0
        self.lastLane = -1
        self.passed = False
        self.spawnTraffic()
        self.lane_center_x = [85, 182, 273]
        self.pos = vec(0, 0)
        self.acc = vec(0, 0)  # Acceleration of the traffic car

    def update(self):
        if self.rect.bottom > 750:
            self.kill()
            print("killed a traffic car")

    def mergeLanes(self):
        current_lane_index = self.get_nearest_lane()

        if current_lane_index == 1:
            target_lane_index = random.choice([0, 2])
        else:
            left_lane_distance = abs(self.pos.x - self.lane_center_x[current_lane_index - 1])
            right_lane_distance = abs(self.pos.x - self.lane_center_x[current_lane_index + 1])

            if left_lane_distance < right_lane_distance:
                target_lane_index = current_lane_index - 1
            else:
                target_lane_index = current_lane_index + 1

        target_lane_x = self.lane_center_x[target_lane_index]

        lane_distance = target_lane_x - self.pos.x

        lane_assist = lane_distance * 0.02 #0.01

        self.acc.x += lane_assist

    def get_nearest_lane(self):
        lane_distances = [abs(self.pos.x - lane_x) for lane_x in self.lane_center_x]
        nearest_lane_index = lane_distances.index(min(lane_distances))
        return nearest_lane_index

    def spawnTraffic(self):
        while True:
            self.lane = random.randint(0, 2)
            if self.lane != self.lastLane:
                break

        if self.lane == 0:
            self.rect.center = (85, -150)
        elif self.lane == 1:
            self.rect.center = (182, -150)
        elif self.lane == 2:
            self.rect.center = (273, -150)
        print("LAST lANE" + str(self.lastLane))
        print("THIS lANE" + str(self.lane))
        print("------------" + str(self.lane))
        self.lastLane = self.lane
        return self.lastLane


