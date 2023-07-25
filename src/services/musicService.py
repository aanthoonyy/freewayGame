import pygame
from pygame import mixer
class MusicService:

    def getCrashSound():
        mixer.music.load('data/audio/Tok2.ogg')
        mixer.music.set_volume(1)
        mixer.music.play(0)


    def getMenuClickSound():
        mixer.music.load('data/audio/Tok5.ogg')
        mixer.music.set_volume(.2)
        mixer.music.play(0)


    def getPassedSound():
        mixer.music.load('data/audio/Tok9.ogg')
        mixer.music.set_volume(.2)
        mixer.music.play(0)

