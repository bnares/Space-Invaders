import pygame
import os
import time
import random

pygame.font.init()


WIDTH,HEIGHT = 750,650

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SPACE SHOOTER")

#load images
RED_SPACE_SHIP = pygame.image.load("assets/pixel_ship_red_small.png")
GREEN_SPACE_SHIP = pygame.image.load("assets/pixel_ship_green_small.png")
BLUE_SPACE_SHIP = pygame.image.load("assets/pixel_ship_blue_small.png")

#player images
YELLOW_SPACE_SHIP = pygame.image.load("assets/pixel_ship_yellow.png")

#lasers

RED_LASER = pygame.image.load("assets/pixel_laser_red.png")
GREEN_LASER = pygame.image.load("assets/pixel_laser_green.png")
BLUE_LASER = pygame.image.load("assets/pixel_laser_blue.png")
YELLOW_LASER = pygame.image.load("assets/pixel_laser_yellow.png")

#background

BG  = pygame.transform.scale(pygame.image.load("assets/background-black.png"), (WIDTH, HEIGHT))  #skalowanie bg to rozmiaru width i height bo ioryginslny bg jest za maly


#define abstract sship class

class Ship():
    COOLDOWN = 30
    def __init__(self, x,y,health =100):
        self.x = x
        self.y = y
        self.health = health
        self.shipImg = None
        self.lasserImg = None
        self.lassers = []
        self.coolDownCounter = 0

    def draw(self, window):
        #pygame.draw.rect(window, (255,0,0),(self.x, self.y, 50,50))
        window.blit(self.shipImg, (self.x, self.y))
        for laser in self.lassers:
            laser.draw(WIN)

    def moveLassers(self, vel, obj):
        self.cooldown()
        for lasser in self.lassers:
            lasser.move(vel)
            if lasser.off_screen(HEIGHT):
                self.lassers.remove(lasser)
            elif lasser.collison(obj):
                obj.health -=10
                self.lassers.remove(lasser)

    def getWidth(self):
        return self.shipImg.get_width()

    def getHeight(self):
        return  self.shipImg.get_height()

    def cooldown(self):
        if(self.coolDownCounter >= self.COOLDOWN):
            self.coolDownCounter =0
        elif self.coolDownCounter>0:
            self.coolDownCounter+=1

    def shoot(self):
        if self.coolDownCounter ==0:
            laser = Laser(self.x, self.y, self.lasserImg)
            self.lassers.append(laser)

class Player(Ship):
    def __init__(self, x,y,health = 100):
        super().__init__(x,y,health)
        self.shipImg = YELLOW_SPACE_SHIP
        self.lasserImg = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.shipImg)  #sprawdzanie czy mamy kolizje z statkiem - jego zdjeciem a nie prostokatem wokol niego
        self.maxHealth = health

    def moveLassers(self, vel, objs):
        self.cooldown()
        for lasser in self.lassers:
            lasser.move(vel)
            if lasser.off_screen(HEIGHT):
                self.lassers.remove(lasser)
            else:
                for obj in objs:
                    if lasser.collison(obj):
                        self.lassers.remove(lasser)
                        objs.remove(obj)


    def healthBar(self, window):
        rectFull = pygame.Rect(self.x, self.y+self.shipImg.get_height()+10, self.shipImg.get_width(), 10)
        pygame.draw.rect(window, (255,0,0), rectFull)

        #pygame.draw.rect(window, (255,0,0),self.x, self.y+self.getHeight()+10, self.shipImg.get_width(),10)
        rectAdjustabile = pygame.Rect(self.x, self.y+self.shipImg.get_height()+10, self.shipImg.get_width()*(self.health/self.maxHealth),10)
        pygame.draw.rect(window, (0,255,0), rectAdjustabile)
        #pygame.draw.rect(window, (0,255,0),self.x, self.y+self.shipImg.get_height()+10, self.shipImg.get_width(),10)


    def draw(self, window):
        #pygame.draw.rect(window, (255,0,0),(self.x, self.y, 50,50))
        window.blit(self.shipImg, (self.x, self.y))
        self.healthBar(WIN)
        for laser in self.lassers:
            laser.draw(WIN)


class Enemy(Ship):

    COLOR_MAP = {
                 "red": (RED_SPACE_SHIP, RED_LASER),
                 "blue": (BLUE_SPACE_SHIP, BLUE_LASER),
                 "green": (GREEN_SPACE_SHIP, GREEN_LASER)
                 }



    def __init__(self,x,y, color, health):
        super().__init__(x,y,health)


        self.shipImg = self.COLOR_MAP[color][0]
        self.lasserImg = self.COLOR_MAP[color][1]
        self.mask = pygame.mask.from_surface(self.shipImg)

    def move(self, vel):
        self.y +=vel


class Laser:
    def __init__(self, x,y,img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not self.y <= height and self.y >=0

    def collison(self, obj):
        return  collide(obj, self)

def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y))




def main():
        run = True
        FPS = 60   #frame per second to check collision
        clock = pygame.time.Clock()  #set a clock to chceck events per second myst be on the top of main event loop
        level = 0
        lives = 5
        mainFont = pygame.font.SysFont("comicsans",35)
        lostFont = pygame.font.SysFont("comicsans", 45)
        playerVelocity =5
        player = Player(300, 550)
        enemies = []
        wavelength = 5
        enemyVel = 1
        lost = False
        lostCountdown = 0;
        lesserVel =5


        def redraw_window():
            WIN.blit(BG, (0, 0))
            #pygame.display.update()
            livesLabel = mainFont.render(f"Lives: {lives}",1,(255,255,255))
            levelLabel = mainFont.render(f"Level: {level}",1,(255,255,255))

            WIN.blit(livesLabel,(10,10))
            WIN.blit(levelLabel, (WIDTH- levelLabel.get_width()-10, 10))


            if lost:
                lostLabel = lostFont.render("You Lost!!",1,(255,255,255))
                WIN.blit(lostLabel, (WIDTH/2- lostLabel.get_width()/2, HEIGHT/2 - lostLabel.get_height()))



            player.draw(WIN)

            for enemy in enemies:
                enemy.draw(WIN)

            pygame.display.update()

        while run:
            clock.tick(FPS)  #checking how many times per second (int his case 60) we are checking events

            redraw_window()

            if lives <=0 or player.health<=0:
                lost = True
                lostCountdown+=1

            if lost:
                if(lostCountdown >= FPS*3):
                    run = False

                else:
                    continue

            if len(enemies) ==0:
                level+=1
                wavelength +=5
                for i in range(wavelength):
                    enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["green", "blue", "red"]), 100)
                    enemies.append(enemy)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False


            keys = pygame.key.get_pressed()  #slownik ktory okresla ktore przycicki zostaly wcisniete
            if keys[pygame.K_a] and player.x > 0:   #a - ruch w lewo
                player.x -= playerVelocity

            if keys[pygame.K_d] and player.x <WIDTH-player.getWidth():     #ruch w prawo
                player.x +=playerVelocity

            if keys[pygame.K_w] and player.y >0 :   #ruch do gory
                player.y -= playerVelocity

            if keys[pygame.K_s] and player.y < HEIGHT - player.getHeight()-30:   #ruch w dol
                player.y += playerVelocity

            if keys[pygame.K_SPACE]:
                player.shoot()

            for enemy in enemies[:]:
                enemy.move(enemyVel)
                enemy.moveLassers(lesserVel, player)
                if random.randrange(0,4*60)==1:
                    enemy.shoot()
                if(enemy.y + enemy.getHeight()>HEIGHT):
                    enemies.remove(enemy)
                    lives-=1
                if collide(player, enemy):
                    player.health-=10
                    enemies.remove(enemy)

            player.moveLassers(-lesserVel, enemies)




main()

