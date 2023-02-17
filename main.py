import os
import sys
import random

import pygame
from pygame import *

pygame.init()
SIZE = W, H = 1500, 900
screen = display.set_mode(SIZE)
all_sprites = sprite.Group()
player_sprite = sprite.Group()
clock = time.Clock()
FPS = 10

def terminate():
    pygame.quit()
    sys.exit()

def load_image(name, colorkey=None):
    filename = os.path.join('data', name)
    if not os.path.isfile(filename):
        print(f'Файл {filename} не найден')
        sys.exit()
    image = pygame.image.load(filename)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image

class Player(sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites, player_sprite)
        self.frames = []
        self.cur_frame = 0
        self.image = None
        self.change_animation('idle', x, y)
        self.speed = 5

    def change_animation(self, anim, x, y):
        if anim == 'idle':
            self.frames = []
            self.cut_sheet(load_image('animation/Idle.png'), 4, 1, x, y)
            self.cur_frame = 0
            self.image = self.frames[self.cur_frame]
        if anim == 'walk':
            self.frames = []
            self.cut_sheet(load_image('animation/Walk.png'), 8, 1, x, y)
            self.cur_frame = 0
            self.image = self.frames[self.cur_frame]

    def cut_sheet(self, sheet, cols, rows, x, y):
        self.rect = Rect(x, y, sheet.get_width() // cols,
                         sheet.get_height() // rows)
        for j in range(rows):
            for i in range(cols):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(Rect(
                    frame_location, self.rect.size
                )))

    def walk(self):
        self.change_animation('walk', self.rect.x, self.rect.y)
        self.rect.x += self.speed

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


player = Player(750, 700)
while True:
    for e in event.get():
        if e.type == pygame.QUIT:
            terminate()
        if e.type == KEYDOWN and e.key == K_RIGHT:
            player.walk()
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    all_sprites.update()
    display.flip()
    clock.tick(FPS)
