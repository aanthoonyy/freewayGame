import random
import pygame
def TrafficFrequency():
    global selector
    selector = random.randint(0, 5)
    if selector == 0:
        return 100
    else:
        return 1000