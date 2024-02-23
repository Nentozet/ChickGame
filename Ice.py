import pygame

pygame.init()


class Ice(pygame.sprite.Sprite):
    def __init__(self, x, y, size, platform_list, ice_list):
        self.x = x
        self.y = y
        pygame.sprite.Sprite.__init__(self)
        ice = pygame.image.load(f'Assets/Images/iceblock.png').convert_alpha()
        self.image = pygame.transform.scale(ice, (size, size))
        self.rect = self.image.get_rect(bottomleft=(self.x, self.y))
        self.add(platform_list)
        self.add(ice_list)
