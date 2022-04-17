from pygame import*
from random import randint
from time import time as timer
font.init()
window = display.set_mode((700, 500))
display.set_caption('лабиринт')
background = transform.scale(image.load("galaxy.jpg"), (700, 500))
lost = 0
score = 0
heart = 0
score2 = 100
timer1 = timer()
bullets2 = sprite.Group()
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.y>5:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.y<450:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)



class Monster(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed, health):
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)
        self.health = health
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1
    def moster2(self):
        direction = "left"
        if self.rect.x <=1:
            self.direction ="right"
        if self.rect.x >=515:
            self.direction = "left"
        if self.direction == "right":
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed
    def fireboss(self):
        bullet2 = Bullets2("bullet.png", self.rect.centerx, self.rect.top, 50, 80, 15)
        bullets2.add(bullet2)

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y <0:
            self.kill()
class Bullets2(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.kill()
win_width = 700
win_height = 500
clock = time.Clock()
FPS = 60
b = Player("rocket.png", 250, 400,80, 100, 5)
v = Player("heart.png", 500, 450,80, 40, 5)
z = Player("heart.png", 560, 450,80, 40, 5)
n = Player("heart.png", 620, 450,80, 40, 5)
boss = Monster('boss.png', 0, -40, 150, 150, 10, 100)
f1 = font.Font(None, 36)
font2 = font.Font(None, 36)

f2 = font.SysFont(None, 36)
f3 = font.SysFont(None, 50)
f4 = font.SysFont(None, 36)
f5 = font.SysFont(None, 50)

osteroids = sprite.Group()
monsters = sprite.Group()
bullets = sprite.Group()
for i in range(1, 3):
    osteroid = Monster('ball.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 2), 3)
    osteroids.add(osteroid)    
for i in range(1, 6):
    monster = Monster('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 2), 1)
    monsters.add(monster)
finish = False
game = True
heart = sprite.Group()
heart.add(z)
heart.add(v)
heart.add(n)
num_fire = 0
num_fire_boss = 0
a = 0
rel_time = False
game2 = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire <30 and rel_time == False:
                    num_fire +=1
                    b.fire()
                if num_fire >=30 and rel_time == False:
                    rel_time = True
                    last_time = timer()

       
    if not finish:
        window.blit(background, (0, 0))
        text1 = f1.render('Счет: '+ str(score), True,(255, 255, 255))
        text2 = f2.render("Пропущено: "+ str(lost), False,(255, 255, 255))
        text4 = f4.render("Жизней у босса:"+str(score2), False,(255, 0, 0))
        timer2 = timer()
        window.blit(text1, (10, 30))
        window.blit(text2, (10, 60))
        if score >= 10:
            for i in monsters:
                i.kill()
            for i in osteroids:
                i.kill()
            boss.moster2()
            boss.draw()
            text4 = f4.render("Жизней у босса:"+str(score2), False,(255, 0, 0))
            window.blit(text4, (10, 90))
            if round(timer2 - timer1, 2)%2 == 0:
                print(round(timer2 - timer1, 1))
                boss.fireboss()
        if lost >= 1:
            heart.remove(v)
        if lost >= 2:
            heart.remove(z)
        if lost >= 3:
            heart.remove(n)
            finish = True
            text3 = f3.render("Проигрыш):", False,(255, 0, 0))
            window.blit(text3, (250, 200))

        b.draw()
        b.update()
        heart.draw(window)
        bullets.update()
        bullets2.update() 
        monsters.update()
        monsters.draw(window)
        bullets.draw(window)
        bullets2.draw(window)
        if rel_time == True:
            now_time = timer()
            if now_time - last_time <1:
                reload2 = font2.render('Перезарядка!', 1,(150, 0, 0))
                window.blit(reload2, (200, 460))
            else:
                num_fire = 0
                rel_time = False 
        osteroids.update()
        osteroids.draw(window)
        sprites_list = sprite.groupcollide(bullets, monsters, True, True)
        sprite_list = sprite.spritecollide(b, monsters, False)
        sprites_list2 = sprite.groupcollide(osteroids, bullets, False, True)
        sprite_list3 = sprite.spritecollide(b, bullets2, True)
        #sprites_list3 = sprite.spritecollide(boss, bullets, False)
        for i in sprite_list3:
            lost += 1       
        for i in sprites_list2:
            i.health -= 1
            if i.health == 0:
                i.kill()
                osteroid = Monster('ball.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 2), 3)
                osteroids.add(osteroid)
        for i in sprite_list:
            text3 = f3.render("Проигрыш):", False,(255, 0, 0))
            window.blit(text3, (250, 200))
            finish = True    
        for i in sprites_list:
            score += 1
            monster = Monster('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 2), 1)
            monsters.add(monster)
        if sprite.spritecollide(boss, bullets, False):
            boss.health -= 1
            score2 -= 1
            if boss.health <= 0:
                boss.kill()
                text5 = f5.render("ПОБЕДА!", False,(0, 255, 0))
                window.blit(text5, (250, 200))
                finish = True

        display.update()
            
    clock.tick(FPS)