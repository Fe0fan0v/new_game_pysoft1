import os
import sys
import random

import pygame
from pygame import *

pygame.init()
SIZE = W, H = 1000, 900
screen = display.set_mode(SIZE)
all_sprites = sprite.Group()
player_sprite = sprite.Group()
level_sprites = sprite.Group()
clock = time.Clock()
FPS = 15
GRAVITY = 5


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


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - W // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - H // 2)


class Player(sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites, player_sprite)
        self.frames = []
        self.cur_frame = 0
        self.image = None
        self.change_animation('idle', x, y)
        self.direction = 'R'
        self.status = 'stay'
        self.speed = 10
        self.jump_power = 20
        self.vx = 0
        self.vy = 0

    def change_animation(self, anim, x, y):
        if anim == 'idle':
            self.frames = []
            self.cut_sheet(load_image('animation/Idle.png'), 4, 1, x, y)
            self.cur_frame = 0
            self.image = self.frames[self.cur_frame].convert_alpha()
        elif anim == 'walk':
            self.frames = []
            self.cut_sheet(load_image('animation/Walk.png'), 8, 1, x, y)
            self.cur_frame = 0
            self.image = self.frames[self.cur_frame].convert_alpha()
        elif anim == 'jump':
            self.frames = []
            self.cut_sheet(load_image('animation/Jump.png'), 6, 1, x, y)
            self.cur_frame = 0
            self.image = self.frames[self.cur_frame].convert_alpha()

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
        player.status = 'walk'
        self.vx = self.speed
        self.change_animation('walk', self.rect.x, self.rect.y)

    def stay(self):
        player.status = 'stay'
        self.vx = 0
        self.change_animation('idle', self.rect.x, self.rect.y)

    def jump(self):
        player.status = 'jump'
        self.vy = self.jump_power
        self.change_animation('jump', self.rect.x, self.rect.y)

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        if self.direction == 'R':
            self.image = self.frames[self.cur_frame]
        elif self.direction == 'L':
            self.image = transform.flip(self.frames[self.cur_frame], True, False)
        if self.status == 'walk' and self.direction == 'R':
            self.rect.x += self.vx
        elif self.status == 'walk' and self.direction == 'L':
            self.rect.x -= self.vx
        elif self.status == 'jump':
            self.rect.y -= self.vy
        if not pygame.sprite.spritecollideany(self, level_sprites):
            self.rect.y += GRAVITY


class Ground(sprite.Sprite):
    def __init__(self):
        super().__init__(level_sprites, all_sprites)
        self.image = load_image('grass.png')
        self.rect = self.image.get_rect()
        self.rect.bottom = H


ground = Ground()
player = Player(ground.rect.top, 700)
camera = Camera()

while True:
    keys = key.get_pressed()
    for e in event.get():
        if e.type == pygame.QUIT:
            terminate()
        if e.type == KEYDOWN:
            if e.key == K_RIGHT:
                player.direction = 'R'
                player.walk()
            elif e.key == K_LEFT:
                player.direction = 'L'
                player.walk()
            if e.key == K_SPACE:
                player.jump()
        if e.type == KEYUP:
            player.stay()
    camera.update(player)
    for sprite in all_sprites:
        camera.apply(sprite)
    screen.fill((0, 0, 0))
    all_sprites.update()
    all_sprites.draw(screen)
    display.flip()
    clock.tick(FPS)
