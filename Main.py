import pygame
import sys
import random
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
    def __init__(self, position_x, position_y, width, height, vel, laser_vel):
        self.position_x = position_x
        self.position_y = position_y
        self.width = width
        self.height = height
        self.vel = vel
        self.ship_image = None
        self.laser_image = None
        self.laser = None
        self.laser_vel = laser_vel
    
    def draw(self, surface):
        surface.blit(self.ship_image, (self.position_x, self.position_y))
        if self.laser is not None:
            self.laser.draw(surface)
    def shoot(self, spawn):
        if self.laser is None:
            self.laser = Laser(self.position_x, self.position_y + spawn, self.laser_image, self.laser_vel)
    def get_width(self):
        return self.ship_image.get_width()
    
    def get_height(self):
        return self.ship_image.get_height()


class Player(Ship):
    def __init__(self, position_x, position_y, width, height, vel):
        super().__init__(position_x, position_y, width, height, vel, -20)
        self.ship_image = pygame.transform.scale(YELLOW_SHIP, (self.width, self.height))
        self.laser_image = pygame.transform.scale(YELLOW_LASER, (self.width, self.height))
        self.mask = pygame.mask.from_surface(self.ship_image) 
        self.lifes = 3

    def handle_keys(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] or key[pygame.K_a] and self.position_x - self.vel > 0:
           self.position_x-=self.vel
        if key[pygame.K_RIGHT] or key[pygame.K_d] and self.position_x + self.width + self.vel < 600:
           self.position_x+=self.vel
        if key[pygame.K_SPACE]:
           self.shoot(-50)


class Enemy(Ship):
    group_direction = "right"
    group_colors_map = {
                        "red": (RED_SHIP, RED_LASER),
                        "green": (GREEN_SHIP, GREEN_LASER),
                        "blue": (BLUE_SHIP, BLUE_LASER)
    }
    
    def __init__(self, position_x, position_y, width, height, vel, points, color):
        super().__init__(position_x, position_y, width, height, vel, 20)
        self.points = points
        self.ship_image, self.laser_image = self.group_colors_map[color]
        self.ship_image = pygame.transform.scale(self.ship_image, (self.width, self.height))
        Enemy.group_direction = "right"
        # Masks allow us to better check if the objects collide with each other
        self.mask = pygame.mask.from_surface(self.ship_image) 

    def change_position(self):
        if Enemy.group_direction=="left":
            self.position_x -= self.vel
        else:
            self.position_x += self.vel

    def change_level(self):
        if Enemy.group_direction == "left":
            self.position_y += 25
        else:
            self.position_y += 25


class Laser:
    def __init__(self, position_x, position_y, image, vel):
        self.image = pygame.transform.scale(image, (50, 50))
        self.position_x = position_x
        self.position_y = position_y
        self.mask = pygame.mask.from_surface(self.image) 
        self.vel = vel

    def draw(self, surface):
        surface.blit(self.image, (self.position_x, self.position_y))

    def move(self):
        self.position_y += self.vel

    def collision(self, obj):
        return collide(obj, self)

def collide(obj1, obj2):
    offset_x = obj2.position_x - obj1.position_x
    offset_y = obj2.position_y - obj1.position_y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def get_enemy(position_x, position_y, width, height, vel, points, color):
    return Enemy(position_x, position_y, width, height, vel, points, color)

enemy_rows = []
enemy_rows.append([get_enemy(i, 50, 50, 50, 15, 75, "red") for i in range(0, 400, 50)])
enemy_rows.append([get_enemy(i, 100, 50, 50, 15, 50, "green") for i in range(0, 400, 50)])
enemy_rows.append([get_enemy(i, 150, 50, 50, 15, 50, "green") for i in range(0, 400, 50)])
enemy_rows.append([get_enemy(i, 200, 50, 50, 15, 25, "blue") for i in range(0, 400, 50)])
enemy_rows.append([get_enemy(i, 250, 50, 50, 15, 25, "blue") for i in range(0, 400, 50)])

player = Player(300, 500, 50, 50, 5)

MOVE_ENEMY_EVENT = pygame.USEREVENT + 1
MOVE_PLAYER_LASER_EVENT = pygame.USEREVENT + 2
MOVE_ENEMY_LASER_EVENT = pygame.USEREVENT + 3
CREATE_ENEMY_LASER_EVENT = pygame.USEREVENT + 4
pygame.time.set_timer(MOVE_ENEMY_EVENT, 700)
pygame.time.set_timer(MOVE_PLAYER_LASER_EVENT, 60)
pygame.time.set_timer(MOVE_ENEMY_LASER_EVENT, 100)
pygame.time.set_timer(CREATE_ENEMY_LASER_EVENT, 2000)

# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == CREATE_ENEMY_LASER_EVENT:
            random_row = random.choice(enemy_rows)
            enemy = random.choice(random_row)
            enemy.shoot(50)
        elif event.type == MOVE_ENEMY_EVENT:  # Player Event
            # update direction of movement
            # Double list comprehension to see 
            # if any enemy touches the right side of window and 
            # if yes then we change level and directrion of movment
            if any(Enemy.group_direction == "right" and 
                   enemy.position_x + enemy.width + enemy.vel>= 600 
                   for enemies in enemy_rows for enemy in enemies):
                Enemy.group_direction = "left"
                change_enemies_level()
            elif any(Enemy.group_direction == "left" and 
                   enemy.position_x <= 0 
                   for enemies in enemy_rows for enemy in enemies):
               Enemy.group_direction = "right"
               change_enemies_level()
            
            def change_enemies_level():
                for enemies in enemy_rows:
                    for enemy in enemies:
                        enemy.change_level()

            # move all enemies in the same direction
            for enemies in enemy_rows:
                for enemy in enemies:
                    enemy.change_position()
        elif event.type == MOVE_ENEMY_LASER_EVENT:
            for enemies in enemy_rows:
                for enemy in enemies:
                    if enemy.laser is not None: # Does Laser exist
                        if enemy.laser.position_y + enemy.laser.vel <= 600: # If the Laser is out of the Map
                            if enemy.laser.collision(player) == True: # Does the laser collide with any enemy
                                player.lifes-=1
                                print("atak")
                                enemy.laser = None
                            if enemy.laser is not None:
                                enemy.laser.move()
                        else:
                            enemy.laser = None
        elif event.type == MOVE_PLAYER_LASER_EVENT:
                if player.laser is not None: # Does Laser exist
                    if player.laser.position_y + player.laser.vel >= 0: # If the Laser is out of the Map
                        loop_escape = False
                        for enemies in enemy_rows:
                            for enemy in enemies:
                                if player.laser.collision(enemy) == True: # Does the laser collide with any enemy
                                    enemies.pop(enemies.index(enemy))
                                    player.laser = None
                                    loop_escape = True
                                    break
                            if loop_escape:
                                break
                        if player.laser is not None:
                            player.laser.move()
                    else:
                        player.laser = None


    screen.blit(bg_image, (0, 0))
    for enemies in enemy_rows:
        for enemy in enemies:
            enemy.draw(screen)
    player.draw(screen)
    player.handle_keys()
    
    pygame.display.update()
    clock.tick(50)