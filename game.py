import random
from time import sleep
import pygame
from src.utils.config import Config
from src.components.carClass import Car
from src.components.explosionClass import Explosion
from src.components.trafficClass import Traffic
import src.services.trafficFreq
import src.components.score
from src.components.line import lineHitbox
from src.services.musicService import MusicService
from src.components.score import scoreBoard
import main

def playGame():
    vec = pygame.math.Vector2
    lastLaneSpawned = -1

    pygame.init()

    screen_width = Config.WIDTH
    screen_height = Config.HEIGHT

    #define colors
    black = (0, 0, 0)
    white = (255, 255, 255)

    max_speed = 500  # base speed of the car


    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Freeway Runner - Game")


    font = pygame.font.SysFont("Arial", 24)


    background_image = pygame.image.load("data/assets/background.png").convert()

    car_width = 50
    car_height = 50
    car_x = (screen_width - car_width) // 2
    car_y = screen_height - car_height - 10
    car_instance = Car(car_x, car_y, vec)
    traffic_instance = Traffic(lastLaneSpawned, vec)
    explosion_instance = Explosion(0, 0)

    car = car_instance
    traffic = traffic_instance



    car_group = pygame.sprite.Group(car)
    traffic_group = pygame.sprite.Group(traffic)
    explosion_group = pygame.sprite.Group()
    traffic.kill()

    #Game loop

    selector = 0
    score = 0
    traffic_frequency = 800 #milliseconds
    scroll_speed = 300
    clock = pygame.time.Clock()

    fps = Config.FPS
    running = True
    speed = 2
    scroll_y = 0
    car_has_hit_550 = False
    should_spawn_traffic = False
    game_over = False
    last_scroll_time = pygame.time.get_ticks()
    last_traffic = pygame.time.get_ticks() - traffic_frequency

    double_traffic = 0
    gameoverTimer = 1


    while running:
        clock.tick(fps)
        elapsed_time = clock.get_time() / 1000.0  # seconds

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Generate new traffic
        if car_has_hit_550 and car.lockoutW and should_spawn_traffic:
            timenow = pygame.time.get_ticks()
            if timenow - last_traffic > traffic_frequency:
                traffic = Traffic(lastLaneSpawned, vec)
                traffic_group.add(traffic)
                if src.services.trafficFreq.TrafficFrequency() == 100 and double_traffic <= 0:
                    traffic = Traffic(lastLaneSpawned, vec)
                    #lastLaneSpawned = traffic.spawnTraffic()
                    traffic_group.add(traffic)
                    double_traffic = 3
                    print("double traffic")
                last_traffic = timenow
                should_spawn_traffic = False
                double_traffic -= 1

                #randomly select a car from the car group
                #random_traffic = random.choice(traffic_group.sprites())

                #apply lane merging logic to the random car
                #random_traffic.mergeLanes()

                #access the nearest lane index of the random car
                #nearest_lane_index = random_traffic.get_nearest_lane()

                #print the nearest lane index
                #print("Nearest Lane Index:", nearest_lane_index)




        speed = car.update(elapsed_time, vec)

        if car.pos.y <= 450 or car_has_hit_550 == True:
            speed = scroll_speed
            car.pos.y = 450
            car_has_hit_550 = True
            car.lockoutW = True
            should_spawn_traffic = True





        #scroll stuff

        scroll_distance = scroll_speed * elapsed_time

        scroll_y += scroll_distance

        if scroll_y >= screen_height:
            scroll_y = 0



        #hitboxes

        line = lineHitbox((0, 0, 0), (0, 465), (Config.WIDTH, 465), 3)
        line_group = pygame.sprite.Group(line)

        for traffic in traffic_group:
            if not traffic.passed:
                if pygame.sprite.spritecollide(traffic, line_group, False):
                    # If there is a collision, the traffic hit the line
                    traffic.passed = True
                    print("Traffic hit the line!")
                    score += 1
                    src.services.musicService.MusicService.getPassedSound()
                    traffic_frequency, scroll_speed = src.components.score.scoreCheck(score, traffic_frequency,
                                                                                      scroll_speed)


        for traffic_car in traffic_group:
            traffic_car.rect.y += scroll_distance

        for traffic_car in traffic_group:
            traffic_car.pos.y += scroll_distance

        if pygame.sprite.groupcollide(car_group, traffic_group, False, True):

           # explosion = Explosion(car.pos.x, car.pos.y)
            #explosion_group.add(explosion)
            car.kill()
            src.services.musicService.MusicService.getCrashSound()
            game_over = True

        if game_over == True:

            explosion = Explosion(car.pos.x, car.pos.y)
            explosion_group.add(explosion)
            gameoverTimer = explosion_group.update()
            pygame.display.update()

            if score > int(src.components.score.readHighScore()):
                src.components.score.setScore(score)

            running = False
            break


        # Update the screen
        screen.fill(white)

        # Draw the background image
        screen.blit(background_image, (0, scroll_y))
        screen.blit(background_image, (0, scroll_y - screen_height))


        # Draw the car
        car_group.draw(screen)
        traffic_group.draw(screen)
        explosion_group.draw(screen)
        #line_group.draw(screen)

        traffic_group.update()
        pygame.display.update()

        if not car.lockoutW:
            font = pygame.font.Font('data/assets/VCR_OSD_MONO_1.001.ttf', 48)
            font2 = pygame.font.Font('data/assets/VCR_OSD_MONO_1.001.ttf', 48)
            text = font.render("Press W", True, white, None)
            textBG = font2.render("Press W", True, black, None)
            textRect = text.get_rect()
            textBGRect = textBG.get_rect()
            textRect.center = (Config.WIDTH / 2, Config.HEIGHT / 2)
            textBGRect.center = ((Config.WIDTH / 2) + 4, (Config.HEIGHT / 2) + 4)
            screen.blit(textBG, textBGRect)
            screen.blit(text, textRect)


        #spawn mile counter
        src.components.score.scoreBoard(screen, score)

    main.main_menu()


#quit
pygame.quit()


