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

def main():
        run = True
        FPS = 60   #frame per second to check collision
        clock = pygame.time.Clock()  #set a clock to chceck events per second myst be on the top of main event loop
        level = 1
        lives = 5
        mainFont = pygame.font.SysFont("comicsans",35)

        def redraw_window():
            WIN.blit(BG, (0, 0))
            #pygame.display.update()
            livesLabel = mainFont.render(f"Lives: {lives}",1,(255,255,255))
            levelLabel = mainFont.render(f"Level: {level}",1,(255,255,255))

            WIN.blit(livesLabel,(10,10))
            WIN.blit(levelLabel, (WIDTH- levelLabel.get_width()-10, 10))
            pygame.display.update()

        while run:
            clock.tick(FPS)  #checking how many times per second (int his case 60) we are checking events
            redraw_window()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False




main()

