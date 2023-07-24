import pygame


def scoreCheck(score, traffic_frequency, scroll_speed):

        if score < 50:
            traffic_frequency -= 5
            scroll_speed += 5
        elif 50 <= score < 75:
            traffic_frequency -= 2.5
            scroll_speed += 2.5
        elif 75 <= score < 150:
            traffic_frequency -= 1.25
            scroll_speed += 1.25
        elif 150 <= score < 200:
            traffic_frequency -= 0.75
            scroll_speed += 0.75
        elif 200 <= score < 250:
            traffic_frequency -= 0.325
            scroll_speed += 0.325
        else:
            traffic_frequency -= 0.15
            scroll_speed += 0.15

        print("Score:", score)
        print("scroll_speed:", scroll_speed)
        print("traffic_frequency:", traffic_frequency)

        return traffic_frequency, scroll_speed


@staticmethod
def scoreBoard(screen, score):
    score_str = str(score)

    if int(score_str) <= 9:
        score_str = "00" + score_str
    elif int(score_str) >= 10 and int(score_str) <= 99:
        score_str = "0" + score_str

    image_path = "data/assets/mileCounter.png"
    image = pygame.image.load(image_path)
    screen.blit(image, (15, 525))

    font = pygame.font.Font('data/assets/VCR_OSD_MONO_1.001.ttf', 28)
    text = font.render(score_str, True, (178, 180, 126), None)
    textRect = text.get_rect()
    textRect.center = (63, 570)
    screen.blit(text, textRect)

    pygame.display.update()

def readHighScore():
    try:
        with open("data/highScore.txt", "r") as file:
            high_score = int(file.read())
            return str(high_score)
    except FileNotFoundError:
        return 0

def setScore(score):
    with open("data/highScore.txt", "w") as file:
        file.write(str(score))

