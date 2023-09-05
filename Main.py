import pygame, sys

pygame.init()
screen = pygame.display.set_mode((400, 500))
clock = pygame.time.Clock()#limits the loop in case that there is powerfull computer(LIMIT FPS)

while True:
    #draw our allements in this loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill((75, 68, 83))
    pygame.display.update()
    clock.tick(120)