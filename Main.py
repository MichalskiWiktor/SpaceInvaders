import pygame
import sys

# Game Basic Setting
screen = pygame.display.set_mode((610, 600))
pygame.display.set_caption("Space Invaders")
bg_image = pygame.image.load("assets\\background-black.png")
bg_image = pygame.transform.scale(bg_image, (610, 600))
clock = pygame.time.Clock()
pygame.init()
#Klasy: Barier


class Player(object):
    image = pygame.image.load("assets\\pixel_ship_yellow.png").convert_alpha()
    size = 50
    laser = None

    def __init__(self):
        self.position = 0
        self.image = pygame.transform.scale(self.image, (Player.size, Player.size))

    def handle_keys(self, surface):
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] or key[pygame.K_a] and self.position>0:
           self.position-=5
        if key[pygame.K_RIGHT] or key[pygame.K_d] and self.position<550:
           self.position+=5
        if key[pygame.K_SPACE]:
            Player.laser = Laser(self.position, 450)

    def draw(self, surface):
       surface.blit(self.image, (self.position, 500))


class Enemy:
    speed = 10
    size = 50
    direction = "right"
    standard_position_y = 0
    
    def __init__(self, position_x, position_y, points, is_alive, image):
        self.position_x = position_x
        self.position_y = position_y
        self.points = points
        self.is_alive = is_alive
        self.image = image
        self.image = pygame.transform.scale(self.image, (Enemy.size, Enemy.size))

    def change_position(self):
        if Enemy.direction=="left":
            self.position_x-=Enemy.speed
        else:
            self.position_x+=Enemy.speed
    
    @classmethod
    def change_level(cls, side):
        if side == "left":
            Enemy.direction="right" 
            Enemy.standard_position_y += 25
        else:
            Enemy.direction="left"
            Enemy.standard_position_y += 25

    def draw(self, surface):
       surface.blit(self.image, (self.position_x, (self.position_y + Enemy.standard_position_y)))


class Laser:
    
    def __init__(self, position_x, position_y):
        self.is_alive = True
        self.image = pygame.image.load("assets\\pixel_laser_yellow.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.position_x = position_x
        self.position_y = position_y
    
    def change_position(self):
        self.position_y -= 20
    
    def draw(self, surface):
       surface.blit(self.image, (self.position_x, self.position_y))

# Enemy Creation Section
imgs = [pygame.image.load("assets\\pixel_ship_red_small.png").convert_alpha(), 
        pygame.image.load("assets\\pixel_ship_green_small.png").convert_alpha(),
        pygame.image.load("assets\\pixel_ship_blue_small.png").convert_alpha(),
        pygame.image.load("assets\\pixel_ship_yellow.png").convert_alpha()]

def get_enemy(position_x, position_y, points, img):
    return Enemy(position_x, position_y, points, True, img)

enemy_rows = []
enemy_rows.append([get_enemy(i, 50, 75, imgs[0]) for i in range(0, 400, 50)])
enemy_rows.append([get_enemy(i, 100, 50, imgs[1]) for i in range(0, 400, 50)])
enemy_rows.append([get_enemy(i, 150, 50, imgs[1]) for i in range(0, 400, 50)])
enemy_rows.append([get_enemy(i, 200, 25, imgs[2]) for i in range(0, 400, 50)])
enemy_rows.append([get_enemy(i, 250, 25, imgs[2]) for i in range(0, 400, 50)])

player = Player()
MOVE_PLAYER_EVENT = pygame.USEREVENT + 1
MOVE_PLAYER_LASER_EVENT = pygame.USEREVENT + 2
pygame.time.set_timer(MOVE_PLAYER_EVENT, 700)
pygame.time.set_timer(MOVE_PLAYER_LASER_EVENT, 100)

# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOVE_PLAYER_EVENT:  # Player Event
            # update direction of movement
            for enemies in enemy_rows:
                if enemies[-1].position_x >= 560 and Enemy.direction == "right":
                    Enemy.change_level("right")
                elif enemies[0].position_x <= 0 and Enemy.direction == "left":
                    Enemy.change_level("left")

            # move all enemies in the same direction
            for enemies in enemy_rows:
                for enemy in enemies:
                    enemy.change_position()
        # move player laser
        elif event.type == MOVE_PLAYER_LASER_EVENT:
            if Player.laser is not None:
                Player.laser.change_position()

    screen.blit(bg_image, (0, 0))
    for enemies in enemy_rows:
        for enemy in enemies:
            enemy.draw(screen)
    player.draw(screen)
    if Player.laser is not None:
        Player.laser.draw(screen)
    player.handle_keys(screen)
    
    pygame.display.update()
    clock.tick(50)