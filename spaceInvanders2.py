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

    def getWidth(self):
        return self.shipImg.get_width()

    def getHeight(self):
        return  self.shipImg.get_height()

class Player(Ship):
    def __init__(self, x,y,health = 100):
        super().__init__(x,y,health)
        self.shipImg = YELLOW_SPACE_SHIP
        self.lasserImg = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.shipImg)  #sprawdzanie czy mamy kolizje z statkiem - jego zdjeciem a nie prostokatem wokol niego
        self.maxHealth = health

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

    def move(self, vel):
        self.y +=vel



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

            if keys[pygame.K_s] and player.y < HEIGHT - player.getHeight():   #ruch w dol
                player.y += playerVelocity

            for enemy in enemies[:]:
                enemy.move(enemyVel)
                if(enemy.y + enemy.getHeight()>HEIGHT):
                    enemies.remove(enemy)
                    lives-=1






main()

