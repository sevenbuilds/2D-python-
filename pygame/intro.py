import pygame
from sys import exit

W, H = 800, 400

pygame.init() #initalizes subsystems like audio, display, fonts

screen = pygame.display.set_mode((W,H)) #creates the window
title = pygame.display.set_caption("Runner")
clock = pygame.time.Clock()  #clock object

sky_surface = pygame.image.load(r"pygame\images\Sky.png")
ground_surface = pygame.image.load(r"pygame\images\ground.png")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(sky_surface,(0,0)) # Second argument is pos downward is +y right is +x
    screen.blit(ground_surface,(0,300))

    #draws all our elements
    #updates everything
    pygame.display.update()
    clock.tick(60)