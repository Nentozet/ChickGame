import pygame
import ctypes

user32 = ctypes.windll.user32
W, H = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
pygame.init()

class Chick(pygame.sprite.Sprite):

    def __init__(self, x, y):
        self.chickleft = self.scale(pygame.image.load('Assets/Images/chickleft.png').convert_alpha())
        self.chickright = self.scale(pygame.image.load('Assets/Images/chickright.png').convert_alpha())
        self.chickjumpright = self.scale(pygame.image.load('Assets/Images/chickjumpright.png').convert_alpha())
        self.chickjumpleft = self.scale(pygame.image.load('Assets/Images/chickjumpleft.png').convert_alpha())
        self.chickrunleft1 = self.scale(pygame.image.load('Assets/Images/chickrunleft1.png').convert_alpha())
        self.chickrunleft2 = self.scale(pygame.image.load('Assets/Images/chickrunleft2.png').convert_alpha())
        self.chickrunright1 = self.scale(pygame.image.load('Assets/Images/chickrunright1.png').convert_alpha())
        self.chickrunright2 = self.scale(pygame.image.load('Assets/Images/chickrunright2.png').convert_alpha())
        self.flyleft1 = self.scale(pygame.image.load('Assets/Images/chickflyleftst1.png').convert_alpha())
        self.flyleft2 = self.scale(pygame.image.load('Assets/Images/chickflyleftst2.png').convert_alpha())
        self.flyleft3 = self.scale(pygame.image.load('Assets/Images/chickflyleftst3.png').convert_alpha())
        self.flyright1 = self.scale(pygame.image.load('Assets/Images/chickflyrightst1.png').convert_alpha())
        self.flyright2 = self.scale(pygame.image.load('Assets/Images/chickflyrightst2.png').convert_alpha())
        self.flyright3 = self.scale(pygame.image.load('Assets/Images/chickflyrightst3.png').convert_alpha())
        self.deadchick = self.scale(pygame.image.load('Assets/Images/Chickdeatheffect.png').convert_alpha())
        self.chicksound = pygame.mixer.Sound('Assets/Sounds/Papapapapapa.mp3')

        self.chickimage = self.chickright
        self.on_ice = 0
        self.xspeed = 0
        self.runspeed = 5
        self.yspeed = 0
        self.gravity = 0.7
        self.jumpspeed = 15
        self.acceleration = 0.5
        self.ground = H
        self.chickturnr = 0
        self.runanim = 1
        self.flyanim = 1
        self.x = x
        self.y = y
        self.on_ground = False


        pygame.sprite.Sprite.__init__(self)
        self.image = self.chickimage
        self.rect = self.image.get_rect(bottomleft=(self.x, 0))

        self.mask = pygame.mask.from_surface(self.chickimage)

    def scale(self, img):
        return pygame.transform.scale(img, (60, 65))

    def collide_horizontal(self, platforms):
        k = 0
        for p in platforms:
            if self.xspeed > 0:
                k = 1
            elif self.xspeed < 0:
                k = -1
            if p.rect.colliderect(self.rect.x + self.xspeed + k, self.rect.y, self.rect.width, self.rect.height):
                if not abs(self.y - p.rect.top) <= 12:
                    if self.xspeed > 0:  # если движется вправо
                        self.xspeed = 0
                    if self.xspeed < 0:  # если движется влево
                        self.xspeed = 0

    def collide_vertical(self, platforms, ice_list):
        ice_collide_count = 0
        k = -20
        if self.yspeed < 0:
            k = 2
        self.on_ground = False
        for p in platforms:
            if p.rect.colliderect(self.rect.x, self.rect.y + self.yspeed + k, self.rect.width, self.rect.height):

                if self.yspeed > 0:
                    self.yspeed = 0

                if self.yspeed < 0 and abs(self.y - p.rect.top) <= 12:
                    self.ground = p.rect.top
                    self.y = self.ground
                    if p in ice_list:
                        self.on_ice = True
                    self.on_ground = True
                    self.yspeed = 0
                    self.ground = self.y
                    for ice in ice_list:
                        if ice in platforms:
                            ice_collide_count += 1
                    if ice_collide_count == 0:
                        self.on_ice = False
        if not self.on_ground:
            self.ground = H

    def update(self, platforms, ice_list):
        keys = pygame.key.get_pressed()

        self.rect = self.image.get_rect(bottomleft=(self.x, self.y))

        "Движение по X "
        # ОБЕ НАЖАТЫ (Остановка)
        if keys[pygame.K_a] and keys[pygame.K_d]:
            if self.xspeed > 0:
                if self.xspeed - self.acceleration <= 0:
                    self.xspeed = 0
                else:
                    if self.rect.bottom == self.ground:
                        if self.on_ice:
                            self.xspeed -= self.acceleration / 3
                        else:
                            self.xspeed -= self.acceleration
                    elif keys[pygame.K_SPACE]:
                        self.xspeed -= self.acceleration / 1.5
                    else:
                        self.xspeed -= self.acceleration / 1.25
            else:
                if self.xspeed + self.acceleration >= 0:
                    self.xspeed = 0
                else:
                    if self.rect.bottom == self.ground:
                        if self.on_ice:
                            self.xspeed += self.acceleration / 3
                        else:
                            self.xspeed += self.acceleration
                    elif keys[pygame.K_SPACE]:
                        self.xspeed += self.acceleration / 3
                    else:
                        self.xspeed += self.acceleration / 2
        # НАЛЕВО
        elif keys[pygame.K_a] and self.xspeed <= 0:
            if self.rect.bottom == self.ground:
                if self.on_ice:
                    if self.xspeed > -self.runspeed * 1.5:
                        self.xspeed -= self.acceleration / 3
                else:
                    if self.xspeed > -self.runspeed:
                        self.xspeed -= self.acceleration
            elif keys[pygame.K_SPACE]:
                if self.xspeed > -self.runspeed / 1.5:
                    self.xspeed -= self.acceleration / 3
            else:
                if self.xspeed > -self.runspeed / 1.25:
                    self.xspeed -= self.acceleration / 2
            self.chickturnr = False
        # НАПРАВО
        elif keys[pygame.K_d] and self.xspeed >= 0:
            if self.rect.bottom == self.ground:
                if self.on_ice:
                    if self.xspeed < self.runspeed * 1.5:
                        self.xspeed += self.acceleration / 3
                else:
                    if self.xspeed < self.runspeed:
                        self.xspeed += self.acceleration
            elif keys[pygame.K_SPACE]:
                if self.xspeed < self.runspeed / 1.5:
                    self.xspeed += self.acceleration / 3
            else:
                if self.xspeed < self.runspeed / 1.25:
                    self.xspeed += self.acceleration / 2
            self.chickturnr = True
            # НЕ НАЖАТЫ (Остановка)
        else:
            if self.xspeed > 0:
                if self.xspeed - self.acceleration <= 0:
                    self.xspeed = 0
                else:
                    if self.rect.bottom == self.ground:
                        if self.on_ice:
                            self.xspeed -= self.acceleration / 3
                        else:
                            self.xspeed -= self.acceleration
                    elif keys[pygame.K_SPACE]:
                        self.xspeed -= self.acceleration / 3
                    else:
                        self.xspeed -= self.acceleration / 2
            else:
                if self.xspeed + self.acceleration >= 0:
                    self.xspeed = 0
                else:
                    if self.rect.bottom == self.ground:
                        if self.on_ice:
                            self.xspeed += self.acceleration / 3
                        else:
                            self.xspeed += self.acceleration
                    elif keys[pygame.K_SPACE]:
                        self.xspeed += self.acceleration / 3
                    else:
                        self.xspeed += self.acceleration / 2

        self.collide_horizontal(platforms)
        self.x += self.xspeed


        if self.rect.bottom != self.ground:
            self.on_ground = False
            self.on_ice = False
        "Обрабатываем прыжок"
        if keys[pygame.K_SPACE] and self.on_ground:
            self.yspeed = self.jumpspeed

        "Поднимаем по Y"
        if self.yspeed > 0:
            self.collide_vertical(platforms, ice_list)
            self.y -= self.yspeed
            self.yspeed -= self.gravity

        "Падение и полёт"
        if self.yspeed <= 0:
            if keys[pygame.K_SPACE]:
                if self.yspeed > -2:
                    self.yspeed -= self.gravity / 2
                else:
                    self.yspeed = -2
            else:
                if self.yspeed > -6:
                    self.yspeed -= self.gravity
                else:
                    self.yspeed = -6

            self.collide_vertical(platforms, ice_list)
            self.y -= self.yspeed

        "Анимация"
        # При беге
        if self.rect.bottom == self.ground and not keys[pygame.K_SPACE]:
            if self.xspeed:
                if self.runanim <= 5:
                    if self.chickturnr:
                        self.chickimage = self.chickrunright1
                    else:
                        self.chickimage = self.chickrunleft1
                    self.runanim += 1
                elif self.runanim <= 10:
                    if self.chickturnr:
                        self.chickimage = self.chickrunright2
                    else:
                        self.chickimage = self.chickrunleft2
                    self.runanim += 1
                elif self.runanim > 10:
                    self.runanim = 1
            else:
                if self.chickturnr:
                    self.chickimage = self.chickright
                else:
                    self.chickimage = self.chickleft
        # При полёте
        if not self.rect.bottom == self.ground:
            if self.yspeed >= 0:
                if self.chickturnr:
                    self.chickimage = self.chickjumpright
                else:
                    self.chickimage = self.chickjumpleft
            elif keys[pygame.K_SPACE]:
                if self.chickturnr:
                    if self.flyanim <= 10:
                        self.chickimage = self.flyright1
                        self.flyanim += 1
                    elif 10 < self.flyanim <= 20:
                        self.chickimage = self.flyright2
                        self.flyanim += 1
                    elif 20 < self.flyanim <= 30:
                        self.chickimage = self.flyright3
                        self.flyanim += 1
                    elif 30 < self.flyanim < 35:
                        self.chickimage = self.flyright2
                        self.flyanim += 1
                    elif self.flyanim == 35:
                        self.flyanim = 1
                else:
                    if self.flyanim <= 10:
                        self.chickimage = self.flyleft1
                        self.flyanim += 1
                    elif 10 < self.flyanim <= 20:
                        self.chickimage = self.flyleft2
                        self.flyanim += 1
                    elif 20 < self.flyanim <= 30:
                        self.chickimage = self.flyleft3
                        self.flyanim += 1
                    elif 30 < self.flyanim < 35:
                        self.chickimage = self.flyleft2
                        self.flyanim += 1
                    elif self.flyanim == 35:
                        self.flyanim = 1
            else:
                if self.chickturnr:
                    self.chickimage = self.chickjumpright
                else:
                    self.chickimage = self.chickjumpleft

        self.mask = pygame.mask.from_surface(self.chickimage)


