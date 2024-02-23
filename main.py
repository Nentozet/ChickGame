import pygame
import ctypes
from Dirt import GrassDirt, Dirt
from Ice import Ice
from Spike import Spike
from Chick import Chick
from Wait import wait
from Egg import Egg
from ButtonTypes import Button
import Saving

pygame.init()
pygame.mouse.set_visible(False)

user32 = ctypes.windll.user32
W, H = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

sc = pygame.display.set_mode((W, H), pygame.FULLSCREEN)
pygame.display.set_caption('Chick Game')
pygame.display.set_icon(pygame.image.load('Assets/Images/chickright.png'))
nest = pygame.transform.scale(pygame.image.load('Assets/Images/chicknest.png'), (78, 55))
nest_rect = nest.get_rect()

menuChick = pygame.image.load('Assets/Images/chickright.png').convert_alpha()
menuChick = pygame.transform.scale(menuChick, (menuChick.get_width() * 3, menuChick.get_height() * 3))

titleFont = pygame.font.SysFont('comicsansms', 48)
nameFont = pygame.font.SysFont('comicsansms', 96)

effectsvolume, musicvolume = Saving.volumesettings_load()

skyimg = pygame.image.load('Assets/Images/sky.png').convert_alpha()
skyimg = pygame.transform.scale(skyimg, (W, H))

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (150, 220, 255)
BLACK = (0, 0, 0)
FPS = 60
clock = pygame.time.Clock()

egg_Group = pygame.sprite.Group()
platform_Group = pygame.sprite.Group()
ice_Group = pygame.sprite.Group()
spikes_Group = pygame.sprite.Group()
mainButts_Group = pygame.sprite.Group()
levelButts_Group = pygame.sprite.Group()

play_button = Button(mainButts_Group, 'Играть!', 1)
quit_button = Button(mainButts_Group, 'Выйти', 2)

level1_button = Button(levelButts_Group, '1 уровень', 1)
level2_button = Button(levelButts_Group, '2 уровень', 2)
level3_button = Button(levelButts_Group, '3 уровень', 3)

level = pygame.Surface((W, H))
level.blit(skyimg, (0, 0))

hero = Chick(0, 0)


def load_level(filename):
    filename = "Assets/Level_Maps/" + filename
    with open(filename, 'r') as mapFile:
        lm = [line.strip() for line in mapFile]

    max_width = max(map(len, lm))
    return list(map(lambda xx: xx.ljust(max_width, '_'), lm))


def draw_level(lev_map):
    for i in range(len(lev_map)):
        for j in range(len(lev_map[i])):
            if lev_map[i][j] == '1':
                GrassDirt(j * H // 24, (i + 1) * H // 24, H // 24, platform_Group)
            elif lev_map[i][j] == '2':
                Dirt(j * H // 24, (i + 1) * H // 24, H // 24, platform_Group)
            elif lev_map[i][j] == '3':
                Spike(j * H // 24, (i + 1) * H // 24, H // 24, spikes_Group)
            elif lev_map[i][j] == '4':
                Ice(j * H // 24, (i + 1) * H // 24, H // 24, platform_Group, ice_Group)
            elif lev_map[i][j] == '0':
                Egg(j * H // 24, i * H // 24, egg_Group)
    spikes_Group.draw(level)
    platform_Group.draw(level)
    egg_Group.draw(level)
    hero.x = nest_rect.x + nest_rect.width // 16
    hero.y = nest_rect.y + nest_rect.width // 2


def game_draw(platforms):
    hero.update(platforms, ice_Group)
    sc.blit(level, (0, 0))
    sc.blit(nest, (nest_rect.x, nest_rect.y))
    sc.blit(hero.chickimage, hero.rect)
    pygame.display.update()


def mainmenu_draw():
    mainButts_Group.update(curbutt_num)
    sc.blit(skyimg, (0, 0))
    sc.blit(title, (W - 510, H // 4 - 105))
    pygame.draw.line(sc, BLACK, (W - 510, H // 4 - 25), (W - 175, H // 4 - 25), 5)
    sc.blit(GameName, (50, 20))
    sc.blit(menuChick, (150, H - 250))
    mainButts_Group.draw(sc)
    pygame.display.update()


def select_level_draw():
    levelButts_Group.update(curbutt_num)
    sc.blit(skyimg, (0, 0))
    sc.blit(title, (W - 510, H // 4 - 105))
    pygame.draw.line(sc, BLACK, (W - 510, H // 4 - 25), (W - 175, H // 4 - 25), 5)
    sc.blit(GameName, (50, 20))
    sc.blit(menuChick, (150, H - 250))
    levelButts_Group.draw(sc)
    pygame.display.update()


def play_music(game_mode):
    if game_mode == 'Game':
        pygame.mixer.music.load('Assets/Sounds/Game_Music.mp3')
    elif game_mode == 'Main Menu':
        pygame.mixer.music.load('Assets/Sounds/Main_Menu_Music.mp3')
    pygame.mixer.music.set_volume(musicvolume)
    pygame.mixer.music.play(-1)


def clear_level():
    platform_Group.empty()
    spikes_Group.empty()
    egg_Group.empty()
    level.blit(skyimg, (0, 0))


mode = 'Main Menu'
play_music(mode)
curbutt_num = 1
title = titleFont.render('Главное меню', True, BLACK)
GameName = nameFont.render('Chick Game', True, GREEN)
level_file = ''
while True:
    """Игра"""
    while mode == 'Game':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    curbutt_num = 1
                    title = titleFont.render('Главное меню', True, BLACK)
                    mode = 'Main Menu'
                    hero.x = nest_rect.x + nest_rect.width // 4
                    hero.y = nest_rect.y - nest_rect.height // 2
                    play_music(mode)
                    break

        for spike in spikes_Group:
            if pygame.sprite.collide_mask(spike, hero):
                curbutt_num = 1
                title = titleFont.render('Главное меню', True, BLACK)
                mode = 'Main Menu'
                play_music(mode)
                hero.x = nest_rect.x + nest_rect.width // 4
                hero.y = nest_rect.y - nest_rect.height // 2
                hero.xspeed, hero.yspeed = 0, 0
                break
        for egg in egg_Group:
            if egg.rect.colliderect(hero.rect):
                mode = 'Main Menu'
                play_music(mode)
                hero.x = nest_rect.x + nest_rect.width // 4
                hero.y = nest_rect.y - nest_rect.height // 2
                hero.xspeed, hero.yspeed = 0, 0
                break

        game_draw(platform_Group)
        clock.tick(FPS)

    """Главное меню"""
    while mode == 'Main Menu':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()
                if event.key == pygame.K_s:
                    if curbutt_num == len(mainButts_Group):
                        curbutt_num = 1
                    else:
                        curbutt_num += 1
                if event.key == pygame.K_w:
                    if curbutt_num == 1:
                        curbutt_num = len(mainButts_Group)
                    else:
                        curbutt_num -= 1
                if event.key == pygame.K_SPACE:
                    if play_button.num == curbutt_num:
                        curbutt_num = 1
                        title = titleFont.render('Выбор уровня', True, BLACK)
                        mode = 'Select Level'
                        wait(1)
                        break
                    if quit_button.num == curbutt_num:
                        exit()
        mainmenu_draw()
        clock.tick(FPS)

    """Выбор уровня"""
    while mode == 'Select Level':
        select_level_draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    curbutt_num = 1
                    title = titleFont.render('Главное меню', True, BLACK)
                    mode = 'Main Menu'
                    break
                if event.key == pygame.K_s:
                    if curbutt_num == len(levelButts_Group):
                        curbutt_num = 1
                    else:
                        curbutt_num += 1
                if event.key == pygame.K_w:
                    if curbutt_num == 1:
                        curbutt_num = len(levelButts_Group)
                    else:
                        curbutt_num -= 1
                if event.key == pygame.K_SPACE:
                    if level1_button.num == curbutt_num:
                        level_file = 'level1.txt'
                        nest_rect.x, nest_rect.y = H // 24 * 27, H // 24 * 21.2
                    elif level2_button.num == curbutt_num:
                        level_file = 'level2.txt'
                        nest_rect.x, nest_rect.y = H // 24 * 19.75, H // 24 * 17.2
                    elif level3_button.num == curbutt_num:
                        level_file = 'level3.txt'
                        nest_rect.x, nest_rect.y = H // 24 * 2, H // 24 * 17.2
                    level_map = load_level(level_file)
                    curbutt_num = 1
                    clear_level()
                    draw_level(level_map)
                    mode = 'Game'
                    play_music(mode)
                    wait(1)
                    break
