import pygame
import random
pygame.init()


class Grass_Dirt(pygame.sprite.Sprite):
    def __init__(self, x, y, size, dirt_list):
        self.x = x
        self.y = y
        pygame.sprite.Sprite.__init__(self)
        dirt_variant = random.choice(range(0, 5))
        dirt = pygame.image.load(f'Assets/Images/earthblock{dirt_variant}.png').convert_alpha()
        self.image = pygame.transform.scale(dirt, (size, size))
        self.rect = self.image.get_rect(bottomleft=(self.x, self.y))
        self.add(dirt_list)


class Dirt(pygame.sprite.Sprite):
    def __init__(self, x, y, size, dirt_list):
        self.x = x
        pygame.sprite.Sprite.__init__(self)
        dirt_variant = random.choice(range(0, 4))
        dirt = pygame.image.load(f'Assets/Images/earthblockwithoutgrass{dirt_variant}.png').convert_alpha()
        self.image = pygame.transform.scale(dirt, (size, size))
        self.rect = self.image.get_rect(bottomleft=(self.x, self.y))
        self.add(dirt_list)



