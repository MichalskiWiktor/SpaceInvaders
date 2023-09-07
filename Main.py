import pygame
import sys

# Game Basic Setting
screen = pygame.display.set_mode((610, 600))
pygame.display.set_caption("Space Invaders")
bg_image = pygame.image.load("assets\\background-black.png")
bg_image = pygame.transform.scale(bg_image, (610, 600))
clock = pygame.time.Clock()
pygame.init()
#Klasy: Bullet, Laser, Enemy, Barier


class Player(object):
    image = pygame.image.load("assets\\pixel_ship_yellow.png").convert_alpha()

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


class Enemy:
    speed = 10
    direction = "right"
    standard_position_y = 0
    
    def __init__(self, position_x, position_y, points, is_alive, image):
        self.position_x = position_x
        self.position_y = position_y
        self.points = points
        self.is_alive = is_alive
        self.image = image
        self.image = pygame.transform.scale(self.image, (50, 50))

    def change_position(self):
        if Enemy.direction=="left" and self.position_x>0:
            self.position_x-=Enemy.speed
        elif Enemy.direction=="right" and self.position_x<560:
            self.position_x+=Enemy.speed
        elif Enemy.direction=="right":
            Enemy.direction="left"
            Enemy.standard_position_y +=25
        else:
            Enemy.direction="right"
            Enemy.standard_position_y +=25

    def draw(self, surface):
       surface.blit(self.image, (self.position_x, (self.position_y + Enemy.standard_position_y)))


imgs = [pygame.image.load("assets\\pixel_ship_red_small.png").convert_alpha(), 
        pygame.image.load("assets\\pixel_ship_green_small.png").convert_alpha(),
        pygame.image.load("assets\\pixel_ship_blue_small.png").convert_alpha(),
        pygame.image.load("assets\\pixel_ship_yellow.png").convert_alpha()]

def get_enemy(position_x, position_y, points, img):
    return Enemy(position_x, position_y, points, True, img)

enemy_rows = []
enemy_rows.append([get_enemy(i, 100, 75, imgs[0]) for i in range(0, 400, 50)])
enemy_rows.append([get_enemy(i, 150, 50, imgs[1]) for i in range(0, 400, 50)])
enemy_rows.append([get_enemy(i, 200, 50, imgs[1]) for i in range(0, 400, 50)])
enemy_rows.append([get_enemy(i, 250, 25, imgs[2]) for i in range(0, 400, 50)])
enemy_rows.append([get_enemy(i, 300, 25, imgs[2]) for i in range(0, 400, 50)])

player = Player()
MOVE_OBJECT_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(MOVE_OBJECT_EVENT, 700)  # 1000 milliseconds = 1 second

# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOVE_OBJECT_EVENT:
            for enemies in enemy_rows:
                if enemies[-1].position_x == 560 and Enemy.direction == "right":
                    enemies[-1].change_position()
                elif enemies[0].position_x == 0 and Enemy.direction == "left":
                    enemies[0].change_position()
                else:    
                    for enemy in enemies:
                        enemy.change_position()
    
    screen.blit(bg_image, (0, 0))
    for enemies in enemy_rows:
        for enemy in enemies:
            enemy.draw(screen)
    player.draw(screen)
    player.handle_keys()
    
    pygame.display.update()
    clock.tick(50)