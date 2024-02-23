import pygame

pygame.init()


def volumesettings_load():
    saves = open("Assets/Saves.txt", "r")
    volumesetts = saves.readline()
    effects, music = volumesetts.split(',')
    effects, music = int(effects), int(music)
    effects, music = effects / 100, music / 100
    saves.close()
    return effects, music
