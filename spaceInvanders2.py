import pygame
import os
import time
import random


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

BG  = pygame.image.load("assets/background-black.png")

def main():
        run = True
        FPS = 60   #frame per second to check collision
        clock = pygame.time.Clock()  #set a clock to chceck events per second myst be on the top of main event loop

        while run:
            clock.tick(FPS)  #checking how many times per second (int his case 60) we are checking events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False




main()

