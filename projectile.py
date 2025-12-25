import math
import pygame

#PROJECTILE STATS
#####
#Bullet
bullet_damage = 30
bullet_speed = 800

#####
#Fire zone
fire_zone_damage = 40
fire_zone_speed = 150
fire_zone_slow = 0.75

#####
#Spike
spike_damage = 30

#####
#Medic bullet
med_heal = 20
med_speed = 600

class Projectile:

    def __init__(self, x, y, size):
        self.rect = pygame.rect.Rect(0, 0, size, size)
        self.id = 1
        self.rect.center = (x, y)
        self.color = (0, 0, 0)

class Bullet(Projectile):

    def __init__(self, x, y, destination):
        super().__init__(x, y, 5)
        self.direction = [0.0,0.0]
        self.speed = bullet_speed
        self.damage = bullet_damage
        self.set_direction(destination)
        self.trace_line = ((0, 0), (0, 0))
        self.id = 2

    def set_damage(self, value):
        self.damage = value

    def set_speed(self, value):
        self.speed = value
    def set_direction(self, target_destination):
        x_axis = target_destination[0] - self.rect.centerx
        y_axis = target_destination[1] - self.rect.centery
        angle = math.atan2(y_axis, x_axis)
        direction_y = round(math.sin(angle), 2)
        direction_x = round(math.cos(angle), 2)
        self.direction[0] = direction_x
        self.direction[1] = direction_y

    def update(self, dt):
        old_pos = self.rect.center
        self.rect.x += self.direction[0] * self.speed * dt
        self.rect.y += self.direction[1] * self.speed * dt
        new_pos = self.rect.center
        self.trace_line = (old_pos, new_pos)

    def get_trace_line(self):
        return self.trace_line

    def to_string(self):
     return str(self.id) + " " + str(self.rect.x) + " " + str(self.rect.y)

class FireZone(Projectile):
    def __init__(self, x, y, destination):
        super().__init__(x, y, 16)
        self.direction = [0.0,0.0]
        self.speed = fire_zone_speed
        self.slow = fire_zone_slow
        self.damage = fire_zone_damage
        self.phase = 1
        self.set_direction(destination)
        self.id = 3

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
     return str(self.id) + " " + str(self.rect.x) + " " + str(self.rect.y) + " " + str(self.phase)

class Spike(Projectile):
    def __init__(self, x, y):
        super().__init__(x, y, 64)
        self.id = 4
        self.damage = spike_damage

    def set_pos(self, x, y):
        self.rect.center = (x, y)

    def to_string(self):
     return str(self.id) + " " + str(self.rect.x) + " " + str(self.rect.y)

class MedicBullet(Projectile):
    def __init__(self, x, y, destination):
        super().__init__(x, y, 5)
        self.direction = [0.0,0.0]
        self.speed = med_speed
        self.heal = med_heal
        self.set_direction(destination)
        self.id = 5

    def set_heal(self, value):
        self.heal = value

    def set_speed(self, value):
        self.speed = value

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
     return str(self.id) + " " + str(self.rect.x) + " " + str(self.rect.y)