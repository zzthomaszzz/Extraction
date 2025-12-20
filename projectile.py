import math

import pygame

class Projectile:

    def __init__(self, x, y, size, _type):
        self.rect = pygame.rect.Rect(0, 0, size, size)
        self.type = _type
        self.rect.center = (x, y)

class Bullet(Projectile):

    def __init__(self, x, y, destination):
        super().__init__(x, y, 5, "damage")
        self.direction = [0.0,0.0]
        self.speed = 600
        self.damage = 10
        self.set_direction(destination)

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
