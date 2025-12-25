import math

import pygame

class Projectile:

    def __init__(self, x, y, size, _type):
        self.rect = pygame.rect.Rect(0, 0, size, size)
        self.type = _type
        self.name_id = 1
        self.rect.center = (x, y)
        self.color = (0, 0, 0)

class Bullet(Projectile):

    def __init__(self, x, y, destination):
        super().__init__(x, y, 5, ["damage"])
        self.direction = [0.0,0.0]
        self.speed = 800
        self.damage = 30
        self.set_direction(destination)
        self.name_id = 2

    def set_damage(self, damage):
        self.damage = damage

    def set_direction(self, target_destination):
        x_axis = target_destination[0] - self.rect.centerx
        y_axis = target_destination[1] - self.rect.centery
        angle = math.atan2(y_axis, x_axis)
        direction_y = round(math.sin(angle), 2)
        direction_x = round(math.cos(angle), 2)
        self.direction[0] = direction_x
        self.direction[1] = direction_y

    def update(self, dt):
        self.rect.x += self.direction[0] * self.speed * dt
        self.rect.y += self.direction[1] * self.speed * dt

    def to_string(self):
     return str(self.name_id) + " " + str(self.rect.x) + " " + str(self.rect.y)

class FireZone(Projectile):
    def __init__(self, x, y, destination):
        super().__init__(x, y, 16, ["slow","damage"])
        self.direction = [0.0,0.0]
        self.speed = 100
        self.slow = 0.5
        self.damage = 25
        self.phase = 1
        self.set_direction(destination)
        self.name_id = 3

    def set_damage(self, value):
        self.damage += value

    def set_size(self, value):
        center = self.rect.center
        self.rect.size = (value, value)
        self.rect.center = center

    def set_direction(self, target_destination):
        x_axis = target_destination[0] - self.rect.centerx
        y_axis = target_destination[1] - self.rect.centery
        angle = math.atan2(y_axis, x_axis)
        direction_y = round(math.sin(angle), 2)
        direction_x = round(math.cos(angle), 2)
        self.direction[0] = direction_x
        self.direction[1] = direction_y

    def update(self, dt):
        if self.speed != 0:
            self.rect.x += self.direction[0] * self.speed * dt
            self.rect.y += self.direction[1] * self.speed * dt

    def to_string(self):
     return str(self.name_id) + " " + str(self.rect.x) + " " + str(self.rect.y) + " " + str(self.phase)

class Spike(Projectile):
    def __init__(self, x, y):
        super().__init__(x, y, 64, ["damage"])
        self.name_id = 4
        self.damage = 40

    def set_pos(self, x, y):
        self.rect.center = (x, y)

    def to_string(self):
     return str(self.name_id) + " " + str(self.rect.x) + " " + str(self.rect.y)