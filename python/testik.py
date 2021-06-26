# импорт библеотек
import pygame
import random
import sys
import math
from datetime import datetime, date, time
from pygame import key
from pygame import event
from pygame import mouse
from pygame.font import Font
from pygame.surfarray import map_array
from pygame.version import PygameVersion
pygame.init()

# alasaila noldo (Zanrix)#0750
# https://vk.com/anysiebastian
# 

# константы

WIDTH = 1280
HEIGHT = 840
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
BG = pygame.image.load('B:\python\img\i.jpg').convert_alpha()
BG = pygame.transform.scale(BG, (WIDTH, HEIGHT)).convert_alpha()
PAUS_FON = pygame.image.load("B:\python\img/paus_black.png")
FPS = 60
BG_MENU = pygame.image.load('B:\python\img/space_bg.jpg')
BG_MENU = pygame.transform.scale(BG_MENU, (WIDTH, HEIGHT)).convert_alpha()



# переменные
nick = None
clock = pygame.time.Clock()
last_now_text = datetime.now()
font = pygame.font.Font(None, 44)
kill = 0
volume = 0.1
clip = []
bullet_speed = 0.3
spisoK_enemes = []
main = 1
management = 1
paused = False
last_coldown = None
text = font.render(f'Kills: {kill} ', True, [255, 255, 255])
text_coldown = font.render('coldawn...', True, [255, 255, 255])
delay_enemes_spawn = 2300
healt = 4
max_healt = 5
menu = True
spisok_schiff = []
need_input =  False
shiff_img = pygame.image.load("B:\python\img/2.png")
game_over = False
fonts_1 = pygame.font.Font(None, 32)
speed = 1
image_x_input_full = [710, 830, 1030]
gold = 0

# фигнюшки

sound_1 = pygame.mixer.Sound('B:\python\mp3/1.mp3')
sound_1.set_volume(volume)


pygame.mixer.music.load('B:\python\mp3/2.mp3')
pygame.mixer.music.play(-1)

pygame.mixer.music.set_volume(volume)

pygame.display.update()

pygame.time.set_timer(pygame.USEREVENT, delay_enemes_spawn)





# классы функции


def blit_text(font_size, text, color, x, y):
    fonts = pygame.font.Font(None, font_size)
    menu_texts = fonts.render(text, True, color, None)
    WINDOW.blit(menu_texts, (x - menu_texts.get_width()/2, y))

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
                    if len(self.text) <= 12:
                        self.text += event.unicode
                self.render_text()


class bullet(pygame.sprite.Sprite):
    def __init__(self, y, x, speed):
        pygame.sprite.Sprite.__init__(self)

        self.bullet_height = 50
        self.bullet_width = 50

        self.bullet_speed = 0.3 * speed

        self.y = y
        self.x = x
        self.image = pygame.image.load('B:\python\img/3.png').convert_alpha(WINDOW)
        self.image = pygame.transform.scale(
            self.image, (self.bullet_height, self.bullet_width))
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self):
        global saved_time, current_time
        if self.x >= WIDTH:
            self.kill()
            clip.remove(self.rect)
 
        self.x += self.bullet_speed
        self.rect = self.image.get_rect(center=(self.x, self.y))


class enemy(pygame.sprite.Sprite):
    def __init__(self, y, x, speed):
        pygame.sprite.Sprite.__init__(self)
        self.y = y
        self.x = x
        self.speed = 0.2 * speed
        self.enemy_height = 70
        self.enemy_width = 70

        self.image = pygame.image.load('B:\python\img/4.png').convert_alpha(WINDOW)
        self.image = pygame.transform.scale(
            self.image, (self.enemy_height, self.enemy_width))
        self.image = pygame.transform.rotate(self.image, 90)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self):
        global kill, healt, speed
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
                speed += 0.15
                kill += 1
                if healt + 0.25 <= max_healt:
                    healt += 0.25
                break     

class input_schiff_test(pygame.sprite.Sprite):
    def __init__(self, img,x, y, margin):
        pygame.sprite.Sprite.__init__(self)
        self.img = img
        self.active = False
        self.x = x 
        self.y = y
        self.width = 150
        self.height = 150
        self.last_pick = 0
        self.margin = margin
        self.spisok_schiff = spisok_schiff
        self.color = (150, 150, 0)
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x + self.margin, self.y)
    def update(self, event_list):
        global shiff_img
        if self.spisok_schiff[0].active and self.last_pick != 0:
            shiff_img = pygame.image.load("B:\python\img/2.png")
            self.last_pick = 0
            self.spisok_schiff[1].active = False
            self.spisok_schiff[2].active = False
            
        if self.spisok_schiff[1].active and self.last_pick != 1:
            shiff_img = pygame.image.load("B:\python\img/4.png")
            shiff_img = pygame.transform.rotate(shiff_img, -90)
            self.last_pick = 1
            self.spisok_schiff[0].active = False
            spisok_schiff[2].active = False
        if self.spisok_schiff[2].active and self.last_pick != 2:
            shiff_img = pygame.image.load("B:\python\img/5.png")
            shiff_img = pygame.transform.rotate(shiff_img, -90)
            self.last_pick = 2
            self.spisok_schiff[1].active = False
            self.spisok_schiff[0].active = False




        if self.active == True:
            self.color = (255, 255, 0)
        else:
            self.color = (150, 150, 0)
    
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
                self.active = True
        self.image.fill((self.color))
class input_schiff(pygame.sprite.Sprite):
    def __init__(self, width_col, height_col):
        pygame.sprite.Sprite.__init__(self)
        self.width_col = width_col
        self.height_col = height_col
        self.margin = 70
        self.x = 200
        self.y = 400
        self.spisok_schif = pygame.sprite.Group() 

        self.img1 = pygame.image.load("B:\python\img/2.png")
        self.img1 = pygame.transform.scale(self.img1, (140, 140))
        self.img1 = pygame.transform.rotate(self.img1, 90)
        self.img2 = pygame.image.load("B:\python\img/4.png")
        self.img2 = pygame.transform.scale(self.img2, (140, 140))
        self.img3 = pygame.image.load("B:\python\img/5.png")
        self.img3 = pygame.transform.scale(self.img3, (140, 140))
        for i in range(3):
            self.a = input_schiff_test(None, 
            WIDTH/2-250, 350, self.margin)
            self.margin += 10 + self.a.width
            self.spisok_schif.add(self.a)
            spisok_schiff.append(self.a)

    def update(self):


        self.spisok_schif.update(event_list)
        self.spisok_schif.draw(WINDOW)
        WINDOW.blit(self.img1, (390, 280))
        WINDOW.blit(self.img2, (550, 280))
        WINDOW.blit(self.img3, (710, 280))

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, coldawn, img, speed):
        pygame.sprite.Sprite.__init__(self)
        self.time_cooldown = coldawn
        self.last_now = datetime.now()
        self.which_bul = 0

        self.x = x
        self.y = y

        self.player_height = 150
        self.player_width = 150

        self.speed = 0.35 * speed

        self.image = img.convert_alpha()
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
                a = bullet(self.y - 23, self.x + 43, speed)
                clip.append(a)
                bullet_sprites.add(a)
            else:
                a = bullet(self.y + 23, self.x + 43, speed )
                clip.append(a)
                bullet_sprites.add(a)
            self.last_now = datetime.now()
        else:
            last_now_text = datetime.now()
        last_coldown = self.last_now.second - self.time_cooldown 
    
class Button():
    def __init__(self, width, height, inactive_color, active_color):
        self.width = width
        self.height = height
        self.inactive_color = inactive_color
        self.active_color = active_color
    def draw(self, x, y, font_size, text, color_text, action=None):
        self.mouse = pygame.mouse.get_pos()
        self.click = pygame.mouse.get_pressed()

        if x < self.mouse[0] < x + self.width and y < self.mouse[1] < y + self.height:
                pygame.draw.rect(WINDOW, self.active_color, (x, y, self.width, self.height))
                if self.click[0] == 1:
                    if action is not None:
                        action()
        else:
            pygame.draw.rect(WINDOW, self.inactive_color, (x, y, self.width, self.height))
        blit_text(font_size, text, color_text, x + self.width/2, y + self.height/2/2)



















def all_update():
    global game_over
    if healt <= 0:
        game_over = True
    WINDOW.blit(BG, (0, 0))
    text_nick = fonts_1.render(f'Корабль: {nick}', True, (255, 255, 255))
    pygame.draw.rect(WINDOW, (255, 0, 0), (WIDTH - max_healt*50 - 10, 45, max_healt*50, 20))
    pygame.draw.rect(WINDOW, (0, 255, 0), (WIDTH - max_healt*50 - 10, 45, healt*50, 20))

    text = font.render(f'Kills: {kill} ', True, [255, 255, 255])
    if ((datetime.now() - last_now_text).seconds < 1):
        text_coldown = font.render('cooldown...', True, [255, 255, 255])
        WINDOW.blit(text_coldown, (WIDTH/2 - text_coldown.get_width() /
                    2, HEIGHT - 50 - text_coldown.get_height()))
    if healt <= 0:
        paused = True

    bullet_sprites.update()
    bullet_sprites.draw(WINDOW)
    all_sprites.update()
    all_sprites.draw(WINDOW)
    enemes.draw(WINDOW)
    enemes.update()
    WINDOW.blit(text_nick, (WIDTH-260, 15))
    WINDOW.blit(text, (10, 20))




def pause():
    global paused
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            sys.exit()
        elif i.type == pygame.KEYDOWN:
            if i.key == pygame.K_ESCAPE:
                paused = False
    pygame.draw.rect(red_image, (90, 220, 100), red_image.get_rect(), 3)
    WINDOW.blit(red_image, (WIDTH/2-170, 50))



def game_while():
        global delay_enemes_spawn, paused
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                sys.exit()
            elif i.type == pygame.KEYDOWN:
                if i.key == pygame.K_UP:
                    sound_1.play()
                if i.key == pygame.K_DOWN:
                    sound_1.play()
                if i.key == pygame.K_SPACE:
                    player.shot()
                if i.key == pygame.K_ESCAPE:
                    paused = True
            if i.type == pygame.USEREVENT:
                enem = enemy(random.randint(150, HEIGHT-30), WIDTH, speed)
                enemes.add(enem)
                spisoK_enemes.append(enem)
                delay_enemes_spawn -= 200

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and 0 <= player.y - player.player_width // 2:
            player.y -= player.speed
        if keys[pygame.K_DOWN] and HEIGHT >= player.y + player.player_width // 2:
            player.y += player.speed
        all_update() 


text_input_box = TextInputBox(WIDTH/2 - 300/2, 170, 300, font)
group = pygame.sprite.Group(text_input_box)





input_schif = input_schiff(50, 50)



def start_game():
    global menu, player, all_sprites, text_input_box, nick, WINDOW, WIDTH, HEIGHT, BG, speed 
    text = text_input_box.text
    speed = 5 * speed
    if len(text) <= 10 and len(text) > 0:
        menu = False
        nick = text
        player = Player(90, HEIGHT/2, 0.5, shiff_img, speed)
        all_sprites.add(player)

button_play = Button(200, 50, (0,139,255), (0,182,255))
def menu_while():
    global event_list
    WINDOW.blit(BG_MENU, (0, 0))
    blit_text(102, 'Меню', (255, 255, 255), WIDTH/2, 25)
    blit_text(42, 'Введите ник', (255, 255, 25), WIDTH/2, 125)
    blit_text(42, 'Выберите корабль', (255, 255, 25), WIDTH/2, 230)
    event_list = pygame.event.get()
    for i in event_list:
        if i.type == pygame.QUIT:
            sys.exit()
    button_play.draw(WIDTH/2-button_play.width/2, 500, 42, 'Полетели', (34,0,255), action=start_game)
    input_schif.update()
    group.update(event_list)
    group.draw(WINDOW)


# спрайты
all_sprites = pygame.sprite.Group()
enemes = pygame.sprite.Group()
bullet_sprites = pygame.sprite.Group()






# основной цикл
while True:
    if menu:
        menu_while()
    elif not paused:
        if game_over:
            pass
        else:
            game_while()
    elif paused:
        pause()
    pygame.display.update()