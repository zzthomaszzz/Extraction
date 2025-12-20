import pygame
import math
import projectile

def rotate_point(point, center_point, angle):

    angle_rad = math.radians(angle % 360)
    # Shift the point so that center_point becomes the origin
    new_point = (point[0] - center_point[0], point[1] - center_point[1])
    new_point = (new_point[0] * math.cos(angle_rad) - new_point[1] * math.sin(angle_rad),
                 new_point[0] * math.sin(angle_rad) + new_point[1] * math.cos(angle_rad))
    # Reverse the shifting we have done
    new_point = (new_point[0] + center_point[0], new_point[1] + center_point[1])
    return new_point

class Player:

    def __init__(self, _id, location):
        self.rect = pygame.rect.Rect(location[0], location[1], 32, 32)
        self.name = "default"
        self.left, self.right, self.up, self.down = 0, 0, 0, 0
        self.id = _id

        #Projectile data
        self.projectile = []
        self.max_projectile = 3
        self.projectile_size = 5

        #I_frame data
        self.isInvincible = False
        self.i_frame_duration = 0.2
        self.i_frame_count = 0

        #Basic Stat Data
        self.vision = 100
        self.max_health = 100
        self.current_health = 100
        self.speed = 100
        self.damage = 10

        #Status data
        self.isDead = False

    def update(self, dt):
        self.handle_i_frame(dt)
        if self.current_health < 0:
            self.isDead = True

    def handle_projectile(self, obstacles, dt):
        for _projectile in self.projectile:
            _projectile.update(dt)
            if _projectile.rect.x < 0 or _projectile.rect.x + _projectile.size > 1280 or _projectile.rect.y < 0 or _projectile.rect.y + _projectile.size > 800:
                self.projectile.remove(_projectile)
            elif _projectile.rect.collidelist(obstacles) >= 0:
                self.projectile.remove(_projectile)

    def handle_i_frame(self, dt):
        if self.isInvincible:
            self.i_frame_count += dt
            if self.i_frame_count >= self.i_frame_duration:
                self.i_frame_count = 0
                self.isInvincible = False

    def basic_attack(self, point):
        x_axis = point[0] - self.rect.centerx
        y_axis = point[1] - self.rect.centery
        angle = math.atan2(y_axis, x_axis)
        direction_y = round(math.sin(angle), 2)
        direction_x = round(math.cos(angle), 2)

        if len(self.projectile) < self.max_projectile:
            self.projectile.append(projectile.Bullet(self.rect.centerx, self.rect.centery, [direction_x, direction_y]))

    def alternate_attack(self, point):
        pass

    def get_projectile_data(self):
        data = []
        for _projectile in self.projectile:
            data.append(_projectile.rect)
        return data

    def take_damage(self, damage):
        if damage > 0:
            if not self.isInvincible:
                self.current_health -= damage
                self.isInvincible = True

    def heal(self, amount):
        if self.current_health < self.max_health:
            self.current_health += amount
            if self.current_health > self.max_health:
                self.current_health = self.max_health

class Soldier(Player):

    def __init__(self, _id, location):
        super().__init__(_id, location)
        self.name = "soldier"
        self.image_path = "asset/soldier.png"

        #Basic stats
        self.speed = 125
        self.vision = 300
        self.max_health = 550
        self.current_health = 550
        self.damage = 50

class Alien(Player):

    def __init__(self, _id, location):
        super().__init__(_id, location)
        self.name = "alien"
        self.image_path = "asset/alien.png"

        # Basic stats
        self.default_speed = 150
        self.speed = 150
        self.vision = 250
        self.max_health = 800
        self.current_health = 800
        self.max_projectile = 1
        self.vision = 250
        self.damage = 35


    #Passive data
        self.regen = 5
        self.counter = 0


    def basic_attack(self, point = (0,0)):
        if len(self.projectile) < self.max_projectile:
            self.projectile.append(projectile.Claw(self.rect.centerx, self.rect.centery))

    def update(self, dt):
        super().update(dt)
        if not self.isDead:
            self.set_regeneration_rate()
            self.regenerate(dt)

    def set_regeneration_rate(self):
        if self.current_health < 150:
            self.regen = 15
            self.speed = self.default_speed / 3
        elif self.current_health < 400:
            self.regen = 10
            self.speed = self.default_speed / 2
        else:
            self.regen = 5
            self.speed = self.default_speed

    def regenerate(self, dt):
        if self.current_health < self.max_health:
            self.counter += dt
            if self.counter >= 1:
                self.counter = 0
                self.current_health += self.regen
                if self.current_health > self.max_health:
                    self.current_health = self.max_health

    def handle_projectile(self, obstacles, dt):
        for _projectile in self.projectile:
            _projectile.update(dt)
            if _projectile.kill:
                self.projectile.remove(_projectile)

class Mage(Player):
    def __init__(self, _id, location):
        super().__init__(_id, location)
        self.name = "mage"
        self.image_path = "asset/mage.png"

        # Basic stats
        self.speed = 130
        self.vision = 350
        self.max_health = 500
        self.current_health = 500
        self.max_projectile = 5
        self.damage = 40

        #Passive data
        #For orbiting circle
        self.cooldown = 0.5
        self.counter = 0
        self.angle = 0
        self.rotation_speed = 180
        self.default_orbit_range = 25
        self.orbit_range = 25

    def handle_projectile(self, obstacles, dt):
        for _projectile in self.projectile:
            _projectile.update(dt)
            if not _projectile.orbit:
                if _projectile.rect.x < 0 or _projectile.rect.x + _projectile.size > 1280 or _projectile.rect.y < 0 or _projectile.rect.y + _projectile.size > 800:
                    self.projectile.remove(_projectile)
                elif _projectile.rect.collidelist(obstacles) >= 0:
                    self.projectile.remove(_projectile)

    def alternate_attack(self, point):
        if self.orbit_range == self.default_orbit_range:
            self.orbit_range = self.default_orbit_range * 2
        else:
            self.orbit_range = self.default_orbit_range

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
                _proj.fire(direction)

