import pygame
import random
import os

#變數存放
WIDTH_W = 900
HIGHT_W = 800
WIDTH = 600
HIGHT = 800
WORD = "Pygame 遊戲製作"
FPS = 60
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

#初始化
pygame.init()
pygame.mixer.init()
running = True
running_sprite = True
show_init = True
score = 20000
rocks_speedmax = 8
check = 0
font_name = os.path.join("font.ttf")
screen = pygame.display.set_mode((WIDTH_W, HIGHT_W))
pygame.display.set_caption(WORD)
clock = pygame.time.Clock()
win = False

#載入外部檔案
background_sound = pygame.mixer.music.load(os.path.join("game_music", "Game_music.mp3"))
pygame.mixer.music.set_volume(0.8)
rock_img = pygame.image.load(os.path.join("img", "rock_img.png"))
player_img = pygame.image.load(os.path.join("img", "player.png"))
pinpon_img = pygame.image.load(os.path.join("img", "pinpon.png"))
rock_up_img = pygame.image.load(os.path.join("img", "rock_up.png"))
rock_right_img = pygame.image.load(os.path.join("img", "rock_right.png"))
win_good = pygame.image.load(os.path.join("img", "win_good.jpg"))

#副程式存放區
class Wall(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, HIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH 
        self.rect.y = 0

class Floor_1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((300, 2))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = 260

class Floor_2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((300, 2))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = 400

class Rocks(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.image = rock_img
        self.image = pygame.transform.scale(rock_img, (85, 85))
        self.image_ori = rock_img
        self.image_ori = pygame.transform.scale(rock_img, (85, 85))
        self.rect = self.image.get_rect()
        self.radius = 30
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(0, WIDTH-30) 
        self.rect.y = -5
        self.speedx = random.randrange(-2, 2)
        self.speedy = random.randrange(4, rocks_speedmax)
        self.rot_degree = 5
        self.total_degree = 0

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if fps_cnt/60 >= 30 and fps_cnt/60 <= 75 and (self.rect.left >= WIDTH or self.rect.right < 0 or self.rect.top > HIGHT):
            self.kill()
        if self.rect.left >= WIDTH or self.rect.right < 0 or self.rect.top > HIGHT:
            self.rect.x = random.randrange(0, WIDTH-30)
            self.rect.y = 0
            self.speedy = random.randrange(4, rocks_speedmax)
        
            
    def rotate(self):
        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree % 360
        self.image = pygame.transform.rotate(self.image_ori, self.total_degree)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center
            
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.radius = 30
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH/2
        self.rect.centery = 560
        self.speed = 6
    
    def update(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_w] or key_pressed[pygame.K_UP]:
            self.rect.y -= self.speed
        if key_pressed[pygame.K_s] or key_pressed[pygame.K_DOWN]:
            self.rect.y += self.speed
        if key_pressed[pygame.K_a] or key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if key_pressed[pygame.K_d] or key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if self.rect.left <= 0:
            self.rect.x = 0
        if self.rect.right >= WIDTH:
            self.rect.x = WIDTH-30
        if self.rect.top <= 0:
            self.rect.y = 0
        if self.rect.bottom >= HIGHT:
            self.rect.y = HIGHT-30

    def attact_up(self):
        big_rocks_up = Big_rocks_up(self.rect.centerx)
        all_sprite.add(big_rocks_up)
        b_r_up.add(big_rocks_up)
        
    def attact_right(self):
        big_rocks_right = Big_rocks_right(self.rect.centery)
        all_sprite.add(big_rocks_right)
        b_r_right.add(big_rocks_right)
        
    def collide(self):
        self.image.fill(GREEN)
        
    def not_collide(self):
        self.image.fill(RED)

class Big_rocks_up(pygame.sprite.Sprite):
    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, WIDTH*9))
        self.image = rock_up_img
        self.image = pygame.transform.scale(rock_up_img, (20, WIDTH*9))
        self.rect = self.image.get_rect()
        self.rect.bottom = 0
        self.rect.centerx = x
        self.speed = 50

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HIGHT:
            self.kill()
            
class Big_rocks_right(pygame.sprite.Sprite):
    def __init__(self, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, WIDTH))
        self.image = rock_right_img
        self.image = pygame.transform.scale(rock_right_img, (HIGHT*2, 20))
        self.rect = self.image.get_rect()
        self.rect.left = WIDTH
        self.rect.centery = y
        self.speed = 20

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()
        
class Pinpon(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((70, 70))
        self.image = pinpon_img
        self.image = pygame.transform.scale(pinpon_img, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.centery = HIGHT/2
        self.rect.centerx = WIDTH/2
        self.speedx = random.randrange(-6, 6)
        self.speedy = random.randrange(-6, 6)
        if self.speedx == 0 or self.speedx == 1 or self.speedx == -1 or self.speedx == -2 or self.speedx == 2:
            self.speedx = 5
        if self.speedy == 0 or self.speedy == 1 or self.speedy == -1 or self.speedy == -2 or self.speedy == 2:
            self.speedx = -5

    def update(self):
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.speedx *= -1.2
        if self.rect.top <= 0 or self.rect.bottom >= HIGHT:
            self.speedy *= -1.2
            
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.speedx >20 or self.speedy >20:
            self.kill()
        
    def attact():
        pin_pon = Pinpon()
        all_sprite.add(pin_pon)
        pinpon.add(pin_pon)
        
class Good(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((300, 2))
        self.image = rock_img
        self.image = pygame.transform.scale(rock_img, (200, 200))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH_W/2
        self.rect.y = HIGHT_W/2

def draw_text_score(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

def draw_init():
    draw_text_score(screen, "第五組_Pygame遊戲製作", 60, WIDTH_W/2, HIGHT_W/4)
    draw_text_score(screen, "按WASD或↑↓←→來控制", 36, WIDTH_W/2, HIGHT_W/2)
    #draw_text_score(screen, "When your score is lower than 0, you lose", 16 ,WIDTH_W/2, HIGHT_W/2+20)
    draw_text_score(screen, "按任何按鍵開始遊戲", 36, WIDTH_W/2, HIGHT_W*3/4)
    draw_text_score(screen, "製作者: 陳上恩、曹詒竣、陳宇懷、林哲安", 36, WIDTH_W/2, HIGHT_W*3/4+52)
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYUP:
                waiting = False

def draw_fine():
    screen.fill(BLACK)
    draw_text_score(screen, "GAME", 64, WIDTH_W/2, 50)
    draw_text_score(screen, "OVER", 64, WIDTH_W/2, 120)
    draw_text_score(screen, "你生存了 ", 30, WIDTH_W/2, HIGHT_W/2)
    if (fps_cnt/60) < 60:
        draw_text_score(screen, str(int(fps_cnt/60)) + "秒", 30, WIDTH_W/2, HIGHT_W/2+30)
    elif (fps_cnt/60) >= 60:
        tem = str(int(fps_cnt/60%60))
        tem_2 = str(int(fps_cnt/60/60))
        draw_text_score(screen, tem_2 + " 分", 30, WIDTH_W/2, HIGHT_W/2+30)
        draw_text_score(screen, tem + " 秒", 30, WIDTH_W/2, HIGHT_W/2+60)
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
            elif event.type == pygame.K_SPACE:
                waiting = False

def draw_rocks_number(check, fps_cnt):
    cnt = 2
    if int(fps_cnt/60) >= 0:
        if int(fps_cnt/60) == 10 and check == 0:
            check += 1
            for i in range(cnt*2):
                r = Rocks()
                rocks.add(r)
                all_sprite.add(r)
        elif int(fps_cnt/60) == 20 and check == 1:
            check += 1
            for i in range(cnt*2):
                r = Rocks()
                rocks.add(r)
                all_sprite.add(r)
        elif int(fps_cnt/60) == 25 and check == 2:
            check += 1
            for i in range(cnt*2):
                r = Rocks()
                rocks.add(r)
                all_sprite.add(r)
        elif int(fps_cnt/60) > 30 and (int(fps_cnt/60))%3 == 0 and int(fps_cnt/60) < 40:
            
            player.attact_up()
            
        elif int(fps_cnt/60) >= 40 and (int(fps_cnt/60))%3 == 0 and check == 3:
            check += 1
            for i in range(cnt*4):
                Pinpon.attact()
                
        elif int(fps_cnt/60) >= 55 and (int(fps_cnt/60))%3 == 0 and int(fps_cnt/60) < 65:
            player.attact_right()
            
        elif int(fps_cnt/60) >= 65 and (int(fps_cnt/60))%3 == 0 and int(fps_cnt/60) < 75:
            player.attact_right()
            player.attact_up()

        elif int(fps_cnt/60) == 75 and check == 4:
            check += 1
            for i in range(cnt*2):
                r = Rocks()
                rocks.add(r)
                all_sprite.add(r)
            
        elif int(fps_cnt/60) >= 85 and (int(fps_cnt/60))%3 == 0 and int(fps_cnt/60) < 95:
            player.attact_up()

        elif int(fps_cnt/60) == 95 and check == 5: 
            check += 1
            for i in range(cnt):
                Pinpon.attact()

        elif int(fps_cnt/60) >= 100 and (int(fps_cnt/60))%3 == 0 and int(fps_cnt/60) < 110:
            player.attact_right()

        elif int(fps_cnt/60) >= 110 and (int(fps_cnt/60))%3 == 0 and int(fps_cnt/60) < 120:
            player.attact_up()

        elif int(fps_cnt/60) == 110 and check == 6: 
            check += 1
            for i in range(cnt+1):
                r = Rocks()
                rocks.add(r)
                all_sprite.add(r)
        
        return check

def draw_health(surf, hp, x, y):
    if hp < 0:
        hp = 0
    BAR_LENGTH = 50
    BAR_HEIGTH = 300
    fill = (hp/20000)*BAR_HEIGTH
    outline_rect = pygame.Rect(x, y, BAR_HEIGTH ,BAR_LENGTH)
    fill_rect = pygame.Rect(x, y, fill, BAR_LENGTH)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def draw_win():
    screen.fill(BLACK)
    draw_text_score(screen, "YOU WIN", 64, WIDTH_W/2, 200)
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
            elif event.type == pygame.K_SPACE:
                waiting = False

all_sprite = pygame.sprite.Group()
player = Player()
wall = Wall()
floor_1 = Floor_1()
floor_2 = Floor_2()
pinpon = Pinpon()
all_sprite.add(player)
all_sprite.add(floor_2)
all_sprite.add(wall)
all_sprite.add(floor_1)
pinpon = pygame.sprite.Group()
b_r_up = pygame.sprite.Group()
b_r_right = pygame.sprite.Group()
rocks = pygame.sprite.Group()
for i in range(10):
    r = Rocks()
    rocks.add(r)
    all_sprite.add(r)

pygame.mixer.music.play(-1)

#Game_Loop
fps_cnt = 0
while running:
    if show_init:
        draw_init()
        show_init = False

    clock.tick(FPS)
    fps_cnt += 1
    time = int(fps_cnt/60)

    #更新畫面
    all_sprite.update()
    check = draw_rocks_number(check, fps_cnt)
    hits = pygame.sprite.spritecollide(player, rocks, False, pygame.sprite.collide_circle)
    hits_up = pygame.sprite.spritecollide(player, b_r_up, False)
    hits_pinpon = pygame.sprite.spritecollide(player, pinpon, False, pygame.sprite.collide_circle)
    hits_right = pygame.sprite.spritecollide(player, b_r_right, False)
    if hits or hits_up or hits_pinpon or hits_right:
        score -= random.randrange(0, 80)
        player.collide()
    else:
        player.not_collide()
    if score <= 0:
        running = False
        win = False
    if fps_cnt/60 >= 120:
        running = False
        win = True

    #畫面顯示
    screen.fill(BLACK)
    #記分板--------------------------------------
    draw_text_score(screen, "TIME", 64, 760, 10)
    draw_text_score(screen, str(time), 64, 760, 100)
    draw_text_score(screen, "SEC", 64, 760, 180)
    draw_text_score(screen, "LIFE", 64, 760, 250)
    draw_text_score(screen, str(score), 64, 760, 320)
    draw_health(screen, score, 601, 400)
    
    if score <= 10000:
        draw_text_score(screen, "你能過關嗎?", 30, 760, 500)
    if fps_cnt/60 >= 100:
        draw_text_score(screen, "快贏了，加油", 30, 760, 600)
        draw_text_score(screen, "(*ﾟ∀ﾟ*)", 30, 760, 650)
    #--------------------------------------------
    all_sprite.draw(screen)
    pygame.display.update()

    #關閉遊戲
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

#離開
if win == False:
    draw_fine()
else:
    draw_win()
pygame.quit()




