import pygame
import sys
# Lasers
BLUE_LASER = pygame.image.load("assets\\pixel_laser_blue.png")
GREEN_LASER = pygame.image.load("assets\\pixel_laser_green.png")
RED_LASER = pygame.image.load("assets\\pixel_laser_red.png")
YELLOW_LASER = pygame.image.load("assets\\pixel_laser_yellow.png")
# Ships
BLUE_SHIP = pygame.image.load("assets\\pixel_ship_blue_small.png")
GREEN_SHIP = pygame.image.load("assets\\pixel_ship_green_small.png")
RED_SHIP = pygame.image.load("assets\\pixel_ship_red_small.png")
YELLOW_SHIP = pygame.image.load("assets\\pixel_ship_yellow.png")

# Game Basic Setting
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Space Invaders")
bg_image = pygame.image.load("assets\\background-black.png")
bg_image = pygame.transform.scale(bg_image, (600, 600))
clock = pygame.time.Clock()
pygame.init()

class Ship():
    def __init__(self, position_x, position_y, width, height, vel):
        self.position_x = position_x
        self.position_y = position_y
        self.width = width
        self.height = height
        self.vel = vel
        self.ship_image = None
        self.laser_image = None
        self.laser = None
    
    def draw(self, surface):
        surface.blit(self.ship_image, (self.position_x, self.position_y))

    def get_width(self):
        return self.ship_image.get_width()
    
    def get_height(self):
        return self.ship_image.get_height()


class Player(Ship):

    def __init__(self, position_x, position_y, width, height, vel):
        super().__init__(position_x, position_y, width, height, vel)
        self.ship_image = pygame.image.load("assets\\pixel_ship_yellow.png").convert_alpha()
        self.ship_image = pygame.transform.scale(self.ship_image, (self.width, self.height))

    def handle_keys(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] or key[pygame.K_a] and self.position_x - self.vel > 0:
           self.position_x-=self.vel
        if key[pygame.K_RIGHT] or key[pygame.K_d] and self.position_x + self.width + self.vel < 600:
           self.position_x+=self.vel


class Enemy(Ship):
    group_colors_map = {
                        "red": (RED_SHIP, RED_LASER),
                        "green": (GREEN_SHIP, GREEN_LASER),
                        "blue": (BLUE_SHIP, BLUE_LASER)
                        }
    
    def __init__(self, position_x, position_y, width, height, vel, points, color):
        super().__init__(position_x, position_y, width, height, vel)
        self.points = points
        self.ship_image, self.laser_image = self.group_colors_map[color]
        self.ship_image = pygame.transform.scale(self.ship_image, (self.width, self.height))
        self.direction = "right"

    def change_position(self):
        if self.direction=="left":
            self.position_x -= self.vel
        else:
            self.position_x += self.vel

    def change_level(self):
        if self.direction == "left":
            self.position_y += 25
        else:
            self.position_y += 25
    
    def change_direction(self, direction):
        self.direction = direction


def get_enemy(position_x, position_y, width, height, vel, points, color):
    return Enemy(position_x, position_y, width, height, vel, points, color)

enemy_rows = []
enemy_rows.append([get_enemy(i, 50, 50, 50, 15, 75, "red") for i in range(0, 400, 50)])
enemy_rows.append([get_enemy(i, 100, 50, 50, 15, 50, "green") for i in range(0, 400, 50)])
enemy_rows.append([get_enemy(i, 150, 50, 50, 15, 50, "green") for i in range(0, 400, 50)])
enemy_rows.append([get_enemy(i, 200, 50, 50, 15, 25, "blue") for i in range(0, 400, 50)])
enemy_rows.append([get_enemy(i, 250, 50, 50, 15, 25, "blue") for i in range(0, 400, 50)])

player = Player(300, 500, 50, 50, 5)
MOVE_PLAYER_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(MOVE_PLAYER_EVENT, 700)

# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOVE_PLAYER_EVENT:  # Player Event
            # update direction of movement
            for enemies in enemy_rows:
                if enemies[-1].position_x + enemies[-1].width + enemies[-1].vel>= 600 and enemies[-1].direction == "right":
                    for enemy in enemies:
                        enemy.change_direction("left")
                        enemy.change_level()
                elif enemies[0].position_x <= 0 and enemies[0].direction == "left":
                    for enemy in enemies:
                        enemy.change_direction("right")
                        enemy.change_level()

            # move all enemies in the same direction
            for enemies in enemy_rows:
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