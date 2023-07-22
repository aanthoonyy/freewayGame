import random
import pygame
import time
from pygame.locals import *
from moviepy.editor import *
from config import Config
from pygame import mixer
import src.components.car
import src.components.explosion



vec = pygame.math.Vector2

# Initialize Pygame
pygame.init()

# Define screen dimensions
screen_width = Config.WIDTH
screen_height = Config.HEIGHT

# Define colors
black = (0, 0, 0)
white = (255, 255, 255)

# Define car dimensions and initial position
car_width = 50
car_height = 50
car_x = (screen_width - car_width) // 2
car_y = screen_height - car_height - 10  # Place the car at the bottom of the screen

# Define car movement variables
max_speed = 500  # Base speed of the car

# Set up the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Freeway Driving")

# Load font for speed display
font = pygame.font.SysFont("Arial", 24)

# Load background image
background_image = pygame.image.load("data/assets/background.png").convert()





selector = 0
score = 0
traffic_frequency = 800 #milliseconds
scroll_speed = 300
def TrafficFrequency():
    global selector
    selector = random.randint(0, 5)
    if selector == 0:
        return 100
    else:
        return 1000


# Define Car class
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


#define traffic
lastLaneSpawned = -1
class Traffic(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('data/assets/traffic.png')
        self.rect = self.image.get_rect()
        self.lane = 0
        self.lastLane = -1
        self.passed = False
        self.spawnTraffic()
        self.lane_center_x = [85, 182, 273]
        self.pos = vec(0, 0)
        self.acc = vec(0, 0)  # Acceleration of the traffic car

    def update(self):
        global score
        global traffic_frequency
        global scroll_speed
        if not self.passed and self.rect.y > car.rect.y - car_height + 4:
            self.passed = True
            score += 1
            #mixer.music.load('Notification.mp3')
            #mixer.music.play(0)
            if score < 50:
                traffic_frequency -= 5
                scroll_speed += 5
            if score > 50 and score < 75:
                traffic_frequency -= 2.5
                scroll_speed += 2.5
            if score > 75 and score < 150:
                traffic_frequency -= 1.25
                scroll_speed += 1.25
            if score > 150 and score < 200:
                traffic_frequency -= 0.75
                scroll_speed += 0.75
            if score > 200 and score < 250:
                traffic_frequency -= 0.325
                scroll_speed += 0.325
            else:
                traffic_frequency -= 0.15
                scroll_speed += 0.15

            print("Score:", score)
            print("scroll_speed:", scroll_speed)
            print("traffic_frequency:", traffic_frequency)


        #self.rect.y += scroll_y / 10
        if self.rect.bottom > 750:
            self.kill()
            print("killed a traffic car")

    def mergeLanes(self):
        current_lane_index = self.get_nearest_lane()

        if current_lane_index == 1:  # In the middle lane
            target_lane_index = random.choice([0, 2])  # Randomly choose left or right lane
        else:  # In one of the side lanes
            left_lane_distance = abs(self.pos.x - self.lane_center_x[current_lane_index - 1])
            right_lane_distance = abs(self.pos.x - self.lane_center_x[current_lane_index + 1])

            if left_lane_distance < right_lane_distance:  # Left lane is closer
                target_lane_index = current_lane_index - 1
            else:  # Right lane is closer or equal
                target_lane_index = current_lane_index + 1

        # Calculate the target X-coordinate of the lane to merge into
        target_lane_x = self.lane_center_x[target_lane_index]

        # Calculate the distance between the car's current X-coordinate and the target lane's X-coordinate
        lane_distance = target_lane_x - self.pos.x

        # Calculate the lane assist force
        lane_assist = lane_distance * 0.02  # Adjust the value to control the strength of the assist

        # Apply the lane assist force to the car's X-coordinate
        self.acc.x += lane_assist

    def get_nearest_lane(self):
        lane_distances = [abs(self.pos.x - lane_x) for lane_x in self.lane_center_x]
        nearest_lane_index = lane_distances.index(min(lane_distances))
        return nearest_lane_index


    def spawnTraffic(self):
        global lastLaneSpawned
        self.lane = random.randint(0, 2)  # Only 3 lanes available (0, 1, 2)

        while self.lane == lastLaneSpawned:
            self.lane = random.randint(0, 2)

        if self.lane == 0:
            self.rect.center = (85, -150)
        elif self.lane == 1:
            self.rect.center = (182, -150)
        elif self.lane == 2:
            self.rect.center = (273, -150)

        lastLaneSpawned = self.lane




class Explosion(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.images = []
		for num in range(1, 6):
			img = pygame.image.load(f"data/assets/explosion/exp{num}.png")
			img = pygame.transform.scale(img, (100, 100))
			self.images.append(img)
		self.index = 0
		self.image = self.images[self.index]
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.counter = 0

	def update(self):
		explosion_speed = 4
		#update explosion animation
		self.counter += 1

		if self.counter >= explosion_speed and self.index < len(self.images) - 1:
			self.counter = 0
			self.index += 1
			self.image = self.images[self.index]

		#if the animation is complete, reset animation index
		if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
			self.kill()



explosion_group = pygame.sprite.Group()

# Create car sprite
car = Car()
car_group = pygame.sprite.Group(car)
traffic = Traffic()
traffic_group = pygame.sprite.Group(traffic)
traffic.kill()

# Game loop
clock = pygame.time.Clock()
fps = Config.FPS
running = True
speed = 2  # Current speed of the car
scroll_y = 0  # Y-coordinate for scrolling the background
car_has_hit_550 = False
should_spawn_traffic = False
game_over = False
last_scroll_time = pygame.time.get_ticks()
last_traffic = pygame.time.get_ticks() - traffic_frequency

double_traffic = 0

while running:
    clock.tick(fps)
    elapsed_time = clock.get_time() / 1000.0  # Calculate elapsed time in seconds

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #if event.type == pygame.key.get_pressed(K_SPACE):
            #main()
            #print("joe mama")

    # Generate new traffic
    if car_has_hit_550 and car.lockoutW and should_spawn_traffic:
        timenow = pygame.time.get_ticks()
        if timenow - last_traffic > traffic_frequency:
            traffic = Traffic()
            traffic_group.add(traffic)
            if TrafficFrequency() == 100 and double_traffic <= 0:
                traffic = Traffic()
                traffic_group.add(traffic)
                double_traffic = 3
            last_traffic = timenow
            should_spawn_traffic = False
            double_traffic -= 1
            print(double_traffic)
            # Randomly select a car from the car group
            random_traffic = random.choice(traffic_group.sprites())

            # Apply lane merging logic to the random car
            random_traffic.mergeLanes()

            # Access the nearest lane index of the random car
            nearest_lane_index = random_traffic.get_nearest_lane()

            # Print the nearest lane index
            #print("Nearest Lane Index:", nearest_lane_index)



    # Handle car movement
    speed = car.update(elapsed_time)

    if car.pos.y <= 450 or car_has_hit_550 == True:
        speed = scroll_speed
        car.pos.y = 450
        car_has_hit_550 = True
        car.lockoutW = True
        should_spawn_traffic = True

    # Calculate scroll distance based on elapsed time and scroll speed

    scroll_distance = scroll_speed * elapsed_time

    # Update the scroll position
    scroll_y += scroll_distance

    # Wrap the scroll_y value to create an infinite scrolling effect
    if scroll_y >= screen_height:
        scroll_y = 0



    # Update the traffic cars' positions based ona the scroll distance
    for traffic_car in traffic_group:
        traffic_car.rect.y += scroll_distance

    if pygame.sprite.groupcollide(car_group, traffic_group, False, True):
        game_over = True
        explosion = Explosion(car.pos.x, car.pos.y)
        explosion_group.add(explosion)
        car.kill()
        mixer.music.load('Boop.mp3')
        mixer.music.play(0)

    if game_over == True:
        print("over")

    # Update the screen
    screen.fill(white)

    # Draw the background image
    screen.blit(background_image, (0, scroll_y))
    screen.blit(background_image, (0, scroll_y - screen_height))

    # Draw the car
    car_group.draw(screen)
    traffic_group.draw(screen)
    explosion_group.draw(screen)

    explosion_group.update()
    traffic_group.update()
    pygame.display.update()

# Quit the game
pygame.quit()
