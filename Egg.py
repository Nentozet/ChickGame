import pygame
pygame.init()

class Egg(pygame.sprite.Sprite):
    def __init__(self, x, y, egg_list):
        self.x = x
        self.y = y
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(f'Assets/Images/egg.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.add(egg_list)
