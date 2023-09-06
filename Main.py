import pygame, sys

#######Game Basic Setting#########
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Space Invaders")
background_image = pygame.image.load("assets\\background-black.png")
background_image = pygame.transform.scale(background_image, (600, 600))
clock = pygame.time.Clock()

#Klasy: Bullet, Laser, Enemy


#########Player - Ship##################
class Player(object):
    image = pygame.image.load("assets\\pixel_ship_yellow.png").convert()
    position = 0
    def __init__(self):
        self.rect = pygame.rect.Rect((64, 54, 16, 16))
        self.image = pygame.transform.scale(self.image, (50, 50))

    def handle_keys(self):
        key = pygame.key.get_pressed()
        dist = 1
        if key[pygame.K_LEFT] or key[pygame.K_a] and self.position>100:
           self.position-=1
        if key[pygame.K_RIGHT] or key[pygame.K_d] and self.position<550:
           self.position+=1

    def draw(self, surface):
       surface.blit(self.image, (self.position, 500))

pygame.init()
player = Player()
clock = pygame.time.Clock()#Limit FPS

#########Game Loop#############
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((0, 0, 0))
    screen.blit(background_image, (0, 0))
    player.draw(screen)
    player.handle_keys()
    pygame.display.update()

    clock.tick(120)