#Создай собственный Шутер!
from pygame import *
from random import randint
from time import time as timer 




fps = 60
clock = time.Clock()

window = display.set_mode((700, 500))
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'),(700, 500))
window.blit(background,(0, 0))


num_fire = 0

rel_time = False


mixer.init()

shot = mixer.Sound('fire.ogg')


mixer.music.load('space.ogg')
mixer.music.play()

miss = 0
kills = 0



class Gamesprite(sprite.Sprite):
    def __init__(self, jimage, speed, x, y,sx=80,sy=100):
        super().__init__()
        self.image = transform.scale(image.load(jimage), (sx, sy))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))



class Bullet(Gamesprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < -5:
            self.kill()

        


class Enemy(Gamesprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.x = randint(80, 700 - 80)
            self.rect.y = 0
            global miss
            miss = miss + 1


class Player(Gamesprite): 
    def update(self): 
        keys = key.get_pressed()
        if keys[K_LEFT] : 
            self.rect.x -= self.speed
        if keys[K_RIGHT] : 
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', 20, self.rect.centerx, self.rect.top, 15, 20)
        bullets.add(bullet)
        shot.play()


st_time = 0


font.init()
font1 = font.Font(None, 36)


asteroids = sprite.Group()
for i in range(2):
    asteroids.add(Enemy('asteroid.png', randint(1,2), randint(0, 700), -10))

bullets = sprite.Group()


hero77 = Player('rocket.png', 8, 310, 400)


monsters = sprite.Group()
for i in range(3):
    monsters.add(Enemy('ufo.png', randint(1,2), randint(0, 700), -10))


finish = False
gamenotover = True 

while gamenotover:
    for e in event.get():
        if e.type == QUIT:
            gamenotover = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 10 and rel_time == False:
                    num_fire += 1
                    hero77.fire()
                elif num_fire >= 10 and rel_time == False:
                    rel_time = True
                    st_time = timer()






    if not finish: 
        window.blit(background,(0,0))
        if kills > 19:
            finish = True
            text_win= font1.render('Победа!', True, (0,255,0))
            window.blit(text_win, (300,250))
        if miss > 9:
            finish = True
            text_defeat= font1.render('Поражение!', True, (255,0,0))
            window.blit(text_defeat, (300,250))

        if rel_time == True:
            h_time = timer()
            if h_time - st_time > 3:
                num_fire = 0
                rel_time = False
            else:
                text_reload= font1.render('Перезарядка!', True, (255,0,0))
                window.blit(text_reload, (300,200))


        if sprite.spritecollide(hero77, asteroids, True):
            finish = True
            text_asteroid= font1.render('В тебя влетел астероид', True, (255,0,0))
            window.blit(text_asteroid, (300,200))

        sprites_list = sprite.groupcollide(monsters, bullets, True, True)
        monsters.draw(window)
        monsters.update()

        asteroids.draw(window)
        asteroids.update()



        bullets.update()
        bullets.draw(window)

        for bulet in sprites_list:
            kills += 1
            monsters.add(Enemy('ufo.png', randint(1,2), randint(0, 700), -10))


        text_lose= font1.render('Пропущено: ' + str(miss), 1, (255, 255, 255))
        window.blit(text_lose, (10,50))

        text_kills= font1.render('Убито: ' + str(kills), 1, (255, 255, 255))
        window.blit(text_kills, (10,10))


        hero77.reset()
        hero77.update()

        clock.tick(fps)
        display.update()
    else:
        kills=0
        miss=0
        finish = False
        time.delay(5000)