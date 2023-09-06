import pygame, sys

#######Game Basic Setting#########
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Space Invaders")
background_image = pygame.image.load("assets\\background-black.png")
background_image = pygame.transform.scale(background_image, (600, 600))
clock = pygame.time.Clock()
pygame.init()

#Klasy: Bullet, Laser, Enemy


#########Player - Ship##################
class Player(object):
    image = pygame.image.load("assets\\pixel_ship_yellow.png").convert()

    def __init__(self):
        self.position = 0
        self.image = pygame.transform.scale(self.image, (50, 50))

    def handle_keys(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] or key[pygame.K_a] and self.position>0:
           self.position-=5
        if key[pygame.K_RIGHT] or key[pygame.K_d] and self.position<550:
           self.position+=5

    def draw(self, surface):
       surface.blit(self.image, (self.position, 500))

#########Enemy###########

class Enemy:
    image = pygame.image.load("assets\\pixel_ship_red_small.png").convert()
    speed = 5
    direction = "right"
    def __init__(self, position, points, speed):
        self.position = position
        self.points = points
        self.speed = speed
        self.image = pygame.transform.scale(self.image, (50, 50))

    def change_position(self):
        if Enemy.direction=="left" and self.position>0:
           self.position-=Enemy.speed
        elif Enemy.direction=="right" and self.position<550:
           self.position+=Enemy.speed
        elif Enemy.direction=="right":
           Enemy.direction="left"
        else:
            Enemy.direction="right"

    def draw(self, surface):
       surface.blit(self.image, (self.position, 200))



enemy = Enemy(0, 10, 6)
player = Player()
MOVE_OBJECT_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(MOVE_OBJECT_EVENT, 1000)  # 1000 milliseconds = 1 second

#########Game Loop#############
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOVE_OBJECT_EVENT:
            enemy.change_position()
    
    screen.blit(background_image, (0, 0))
    enemy.draw(screen)
    player.draw(screen)
    player.handle_keys()
    
    pygame.display.update()
    clock.tick(50)