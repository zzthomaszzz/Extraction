import pygame
import math

from pygame.transform import rotate

import projectile


class Player:
    max_health = 100

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

        #Damage data
        self.isInvincible = False
        self.i_frame_duration = 0.25
        self.i_frame_count = 0

        #Status data
        self.isDead = False

    def update(self, dt):
        if self.isInvincible:
            self.i_frame_count += dt
            if self.i_frame_count >= self.i_frame_duration:
                self.isInvincible = False

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

    def take_damage(self, damage):
        if not self.isInvincible:
            self.current_health -= damage
            self.isInvincible = True

class Soldier(Player):

    def __init__(self, _id):
        super().__init__(_id)
        self.name = "soldier"
        self.speed = 150
        self.vision = 600
        self.max_health = 500
        self.current_health = 500
        self.projectile_speed = 500
        self.image_path = "asset/soldier.png"

class Alien(Player):

    def __init__(self, _id):
        super().__init__(_id)
        self.name = "alien"
        self.speed = 125
        self.max_health = 500
        self.current_health = 500
        self.max_projectile = 4
        self.projectile_speed = 400
        self.vision = 200
        self.image_path = "asset/alien.png"


def rotate_point(point, center_point, angle):

    angle_rad = math.radians(angle % 360)
    # Shift the point so that center_point becomes the origin
    new_point = (point[0] - center_point[0], point[1] - center_point[1])
    new_point = (new_point[0] * math.cos(angle_rad) - new_point[1] * math.sin(angle_rad),
                 new_point[0] * math.sin(angle_rad) + new_point[1] * math.cos(angle_rad))
    # Reverse the shifting we have done
    new_point = (new_point[0] + center_point[0], new_point[1] + center_point[1])
    return new_point


class Mage(Player):
    def __init__(self, _id):
        super().__init__(_id)
        self.name = "mage"
        self.speed = 80
        self.max_health = 300
        self.current_health = 300
        self.max_projectile = 5
        self.projectile_speed = 500
        self.vision = 350
        self.image_path = "asset/mage.png"

        self.cooldown = 1
        self.counter = 0
        self.angle = 0
        self.rotation_speed = 180
        self.orbit_range = 15

    def update(self, dt):
        super().update(dt)
        self.angle += self.rotation_speed * dt
        if self.angle > 360:
            self.angle = 0

        if len(self.projectile) < self.max_projectile:
            self.counter += dt
            if self.counter >= self.cooldown:
                self.counter = 0
                self.projectile.append(projectile.FireBall(self.rect.centerx + self.orbit_range, self.rect.centery + self.orbit_range, len(self.projectile)))

        for _proj in self.projectile:
            if _proj.orbit:
                _proj.rect.center = rotate_point([self.rect.centerx + self.orbit_range, self.rect.centery + self.orbit_range], self.rect.center, self.angle + ((360 / self.max_projectile) * _proj.index))

    def basic_attack(self, point):
        for _proj in self.projectile:
            if _proj.orbit:
                x_axis = point[0] - _proj.rect.centerx
                y_axis = point[1] - _proj.rect.centery
                radian = math.atan2(y_axis, x_axis)
                direction_y = round(math.sin(radian), 2)
                direction_x = round(math.cos(radian), 2)
                direction = [direction_x, direction_y]
                _proj.fire(direction, self.projectile_speed)

