import pygame
import math
import projectile

class Player:

    def __init__(self, _id):
        self.rect = pygame.rect.Rect(0, 0, 32, 32)
        self.name = "default"
        self.speed = 100
        self.left, self.right, self.up, self.down = 0, 0, 0, 0
        self.vision = 100
        self.max_health = 100
        self.current_health = 100
        self.image_path = "asset/default_player.png"
        self.id = _id

        #Projectile data
        self.projectile = []
        self.max_projectile = 10
        self.projectile_size = 5
        self.projectile_speed = 300

        #Status data
        self.isDead = False

    def update(self, dt):
        self.rect.x += (self.right - self.left) * self.speed * dt
        self.rect.y += (self.down - self.up) * self.speed * dt

    def basic_attack(self, point):
        x_axis = point[0] - self.rect.centerx
        y_axis = point[1] - self.rect.centery
        angle = math.atan2(y_axis, x_axis)
        direction_y = round(math.sin(angle), 2)
        direction_x = round(math.cos(angle), 2)

        if len(self.projectile) < self.max_projectile:
            self.projectile.append(projectile.Bullet(self.rect.centerx, self.rect.centery, [direction_x, direction_y], self.projectile_speed))

    def draw_health_bar(self):
        max_hp_rect = pygame.rect.Rect(self.rect.x, self.rect.y - 10, 32, 5)
        current_hp_bar = (self.current_health / self.max_health) * 32
        current_hp_rect = pygame.rect.Rect(self.rect.x, self.rect.y - 10, current_hp_bar, 5)
        pygame.draw.rect(pygame.display.get_surface(), "black", max_hp_rect)
        pygame.draw.rect(pygame.display.get_surface(), "green", current_hp_rect)

    def get_projectile_data(self):
        data = []
        for _projectile in self.projectile:
            data.append(_projectile.rect)
        return data

class Soldier(Player):

    def __init__(self, _id):
        super().__init__(_id)
        self.name = "soldier"
        self.speed = 400
        self.vision = 400
        self.max_health = 500
        self.current_health = 500
        self.projectile_speed = 500
        self.image_path = "asset/soldier.png"

class Alien(Player):

    def __init__(self, _id):
        super().__init__(_id)
        self.name = "alien"
        self.speed = 300
        self.max_health = 800
        self.current_health = 800
        self.max_projectile = 4
        self.projectile_speed = 400
        self.vision = 200
        self.image_path = "asset/alien.png"
