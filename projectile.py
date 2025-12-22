import math

import pygame

class Projectile:

    def __init__(self, x, y, size, _type, owner):
        self.rect = pygame.rect.Rect(0, 0, size, size)
        self.type = _type
        self.name_id = 1
        self.rect.center = (x, y)
        self.color = (0, 0, 0)
        self.id = owner

    def set_color(self, enemy = False):
        if not enemy:
            self.color = "green"
        else:
            self.color = "red"

    def draw_image(self, image):
        pygame.display.get_surface().blit(image, self.rect)

class Bullet(Projectile):

    def __init__(self, x, y, destination, owner):
        super().__init__(x, y, 5, ["damage"], owner)
        self.direction = [0.0,0.0]
        self.speed = 800
        self.damage = 25
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

    def draw(self):
        pygame.draw.rect(pygame.display.get_surface(), self.color, self.rect, 1)

class FireZone(Projectile):
    def __init__(self, x, y, destination, owner):
        super().__init__(x, y, 16, ["slow","damage"], owner)
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
        self.rect.size = (value, value)
        self.rect.center = (self.rect.x, self.rect.y)

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

    def draw(self):
        pygame.draw.rect(pygame.display.get_surface(), "orange", self.rect, 1)