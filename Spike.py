import pygame

pygame.init()


class Spike(pygame.sprite.Sprite):
    def __init__(self, sx, sy, size, spikelist):
        self.x = sx
        self.y = sy
        pygame.sprite.Sprite.__init__(self)
        self.s = pygame.image.load("Assets/Images/spike.png")
        self.image = pygame.transform.scale(self.s, (size, size))
        self.rect = self.image.get_rect(bottomleft=(self.x, self.y))
        self.mask = pygame.mask.from_surface(self.image)
        self.add(spikelist)
