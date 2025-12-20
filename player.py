import pygame
import math
import projectile

class Player:

    def __init__(self, _id, location):
        self.rect = pygame.rect.Rect(location[0], location[1], 32, 32)
        self.name = "default"
        self.left, self.right, self.up, self.down = 0, 0, 0, 0
        self.id = _id

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

    def handle_i_frame(self, dt):
        if self.isInvincible:
            self.i_frame_count += dt
            if self.i_frame_count >= self.i_frame_duration:
                self.i_frame_count = 0
                self.isInvincible = False

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

    def alternate_attack(self, point):
        if self.orbit_range == self.default_orbit_range:
            self.orbit_range = self.default_orbit_range * 2
        else:
            self.orbit_range = self.default_orbit_range

    def update(self, dt):
        super().update(dt)

