import pygame
import random
import sys
import math
from datetime import datetime, date, time
from testik import *

class TextInputBox(pygame.sprite.Sprite):
    def __init__(self, x, y, w, font):
        super().__init__()
        self.color = (255, 255, 255)
        self.backcolor = None
        self.pos = (x, y) 
        self.width = w
        self.font = font
        self.active = False
        self.text = ""
        self.render_text()

    def render_text(self):
        
        t_surf = self.font.render(self.text, True, self.color, self.backcolor)
        self.image = pygame.Surface((max(self.width, t_surf.get_width()+10), t_surf.get_height()+10), pygame.SRCALPHA)
        if self.backcolor:
            self.image.fill(self.backcolor)
        self.image.blit(t_surf, (self.image.get_width()/2 - t_surf.get_width()/2, 5))
        pygame.draw.rect(self.image, self.color, self.image.get_rect().inflate(-2, -2), 2)
        self.rect = self.image.get_rect(topleft = self.pos)



    def update(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and not self.active:
                self.active = self.rect.collidepoint(event.pos)
            if event.type == pygame.KEYDOWN and self.active:
                if event.key == pygame.K_RETURN:
                    self.active = False
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                    print(self.text)
                else:
                    self.text += event.unicode
                self.render_text()



class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, coldawn):
        pygame.sprite.Sprite.__init__(self)

        self.time_cooldown = coldawn
        self.last_now = datetime.now()
        self.which_bul = 0

        self.x = x
        self.y = y

        self.player_height = 150
        self.player_width = 150

        self.speed = 0.25

        self.image = pygame.image.load('img/2.png').convert_alpha(WINDOW)
        self.image = pygame.transform.scale(
            self.image, (self.player_height, self.player_width))
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self):
        self.rect = self.image.get_rect(center=(self.x, self.y))
        pygame.draw.line(WINDOW, (20, 30, 90),
                         (self.x, self.y), (WIDTH, self.y))

    def shot(self):
        global last_now_text, last_coldown
        if ((datetime.now() - self.last_now).seconds > self.time_cooldown):
            self.which_bul += 1
            if self.which_bul % 2 == 0:
                a = bullet(self.y - 23, self.x + 43)
                clip.append(a)
                bullet_sprites.add(a)
            else:
                a = bullet(self.y + 23, self.x + 43)
                clip.append(a)
                bullet_sprites.add(a)
            self.last_now = datetime.now()
        else:
            last_now_text = datetime.now()
        last_coldown = self.last_now.second - self.time_cooldown 

class enemy(pygame.sprite.Sprite):
    def __init__(self, y, x):
        pygame.sprite.Sprite.__init__(self)
        self.y = y
        self.x = x
        self.speed = 0.1
        self.enemy_height = 70
        self.enemy_width = 70

        self.image = pygame.image.load('img/4.png').convert_alpha(WINDOW)
        self.image = pygame.transform.scale(
            self.image, (self.enemy_height, self.enemy_width))
        self.image = pygame.transform.rotate(self.image, 90)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self):
        global kill, healt
        self.x -= self.speed
        self.rect = self.image.get_rect(center=(self.x, self.y))
        if self.rect.colliderect(player.rect):
            healt -= 0.5
            self.kill()
        if self.rect.x <= player.rect.width:
            self.speed += 1
        if self.rect.x <= 0:
            healt -= 1
            self.kill()
        for i in range(len(clip)):
            if self.rect.collidepoint(clip[i].x, clip[i].y):
                self.kill()
                clip[i].kill()
                del clip[i]
                kill += 1
                healt += 0.25
                break         