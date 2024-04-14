#Создай собственный Шутер!

from pygame import *
from random import randint
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
clock = time.Clock()
window = display.set_mode((700, 500))
class GameSprite(sprite.Sprite):
    def __init__(self, image_player, speed, x, y, width, height):
        super().__init__()
        self.image = transform.scale(image.load(image_player), (width, height))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y 

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        elif keys_pressed[K_d] and self.rect.x < 600:
            self.rect.x += self.speed
        elif keys_pressed[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
        elif keys_pressed[K_s] and self.rect.y < 400:
            self.rect.y += self.speed

    def shoot(self):
        bullet = Bullet('bullet.png', speed=6,x=self.rect.centerx, y=self.rect.y, width=15, height=20)
        bullets.add(bullet)


class Enemy(GameSprite):
    
    def update(self):  
        global lost    
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.y = -20
            self.rect.x = randint(0, 600)
            lost += 1

asteroids=sprite.Group()
for i in range(3):
    astr=Enemy(image_player = 'asteroid.png', speed = randint(1, 2), x = randint(0, 600), y = 0, width = 70, height = 50)
    asteroids.add(astr)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
bullets = sprite.Group(  )

 

ufos = sprite.Group()
for i in range(5):
    ufo = Enemy(image_player = 'ufo.png', speed = randint(1, 2), x = randint(0, 600), y = 0, width = 70, height = 50)
    ufos.add(ufo)
galaxy = transform.scale(image.load('galaxy.jpg'),(700, 500))
rocket = Player(image_player = 'rocket.png', speed = 10, x = 200, y = 350, width = 40, height = 110)
font.init()
font2 = font.SysFont('Arial', 36)
score = 0
lost = 0
lives = 3
fps = 60
finish = False
game = True
while game:
    for i in event.get():
        if i.type == QUIT:
            game= False
        if i.type == KEYDOWN:
            if i.key == K_SPACE:
                rocket.shoot()

    if not finish:

        score_text = font2.render('Счёт:)'+ str(score),True, (255, 255, 255))
        miss_text = font2.render('Пропущено:'+ str(lost),True, (255, 255, 255))

        window.blit(galaxy, (0,0))
        window.blit(score_text, (50, 30))
        window.blit(miss_text, (50, 60))
        lives_text = font2.render('Счётчик жизней: '+str(lives),True, (255, 255, 255))
        window.blit(lives_text, (460, 30))

        if sprite.spritecollide(rocket, ufos, True) or sprite.spritecollide(rocket, asteroids, True):
            lives -= 1

        if lives <= 0:   
            finish = True
            
            loos = font2.render('LOSE',True, (255, 255, 255))
            window.blit(loos, (300,250))

        
        if sprite.groupcollide(ufos, bullets, True, True):
            score += 1
            ufo = Enemy(image_player = 'ufo.png', speed = randint(1, 4), x = randint(0, 600), y = 0, width = 70, height = 50)
            ufos.add(ufo)
        if score >= 10:
            finish = True  
            win = font2.render('WIN',True, (255, 255, 255))    
            window.blit(win, (300,250))
        rocket.reset()
        rocket.update()
        ufos.update()
        ufos.draw(window)
        asteroids.update()
        asteroids.draw(window)
        bullets.update()
        bullets.draw(window)
    clock.tick(fps)
    display.update()

