import pygame
import math
from projectile import *

class Player:

    def __init__(self, _id, location, vision = 100, health = 100, speed = 100):
        self.rect = pygame.rect.Rect(location[0], location[1], 32, 32)
        self.name = "default"
        self.left, self.right, self.up, self.down = 0, 0, 0, 0
        self.id = _id
        self.projectile = []

        #I_frame data
        self.isInvincible = False
        self.i_frame_duration = 0.2
        self.i_frame_count = 0

        #Basic Stat Data
        self.default_vision = vision
        self.max_health = health
        self.default_speed = speed

        self.health = 0
        self.vision = 0
        self.speed = 0
        self.init_basic_stats()

        #Status data
        self.isDead = False

    def update(self, dt):
        self.handle_i_frame(dt)
        if self.health < 0:
            self.isDead = True

    def handle_i_frame(self, dt):
        if self.isInvincible:
            self.i_frame_count += dt
            if self.i_frame_count >= self.i_frame_duration:
                self.i_frame_count = 0
                self.isInvincible = False

    def init_basic_stats(self):
        self.health = self.max_health
        self.speed = self.default_speed
        self.vision = self.default_vision

    def take_damage(self, value):
        self.health -= value

    def modify_speed(self, value):
        self.speed = self.default_speed * value

class Soldier(Player):

    def __init__(self, _id, location):
        super().__init__(_id, location, 300, 550, 125)
        self.name = "soldier"

        #Primary stats
        self.attack_on_cooldown = False
        self.default_attack_speed = 0.5
        self.current_attack_speed = 0.5
        self.attack_speed_counter = 0.0

        #Secondary stats
        self.isCooldown = False
        self.health_cost = 0.1
        self.adrenaline_cooldown = 2
        self.adrenaline_cooldown_counter = 0.0
        self.isBoosted = False
        self.adrenaline_duration = 5
        self.adrenaline_counter = 0.0
        self.attack_speed_multiplier = 2
        self.speed_multiplier = 1.5

    def update(self, dt):

        #PRIMARY
        if self.attack_on_cooldown:
            if self.attack_speed_counter > self.current_attack_speed:
                self.attack_on_cooldown = False
                self.attack_speed_counter = 0.0
            else:
                self.attack_speed_counter += dt

        #SECONDARY
        if self.isCooldown:
            if self.adrenaline_cooldown_counter > self.adrenaline_cooldown:
                self.isCooldown = False
                self.adrenaline_cooldown_counter = 0
            else:
                self.adrenaline_cooldown_counter += dt
        else:
            if self.isBoosted:
                if self.adrenaline_counter > self.adrenaline_duration:
                    self.isBoosted = False
                    self.isCooldown = True
                    self.current_attack_speed = self.default_attack_speed
                    self.speed = self.default_speed
                    self.adrenaline_counter = 0
                else:
                    self.adrenaline_counter += dt
                    self.current_attack_speed = self.default_attack_speed / self.attack_speed_multiplier
                    self.speed = self.default_speed * self.speed_multiplier

        super().update(dt)

    def primary(self, location):
        if not self.attack_on_cooldown:
            if self.isBoosted:
                bullet = Bullet(self.rect.centerx, self.rect.centery, location, self.id)
                bullet.set_damage(bullet.type_value * 2)
                self.projectile.append(bullet)
            else:
                self.projectile.append(Bullet(self.rect.centerx, self.rect.centery, location, self.id))
            self.attack_on_cooldown = True

    def secondary(self):
        if not self.isCooldown:
            if not self.isBoosted:
                if self.health > self.max_health * self.health_cost:
                    self.isBoosted = True
                    self.health -= self.max_health * self.health_cost

class Alien(Player):

    def __init__(self, _id, location):
        super().__init__(_id, location)
        self.name = "alien"

        # Basic stats
        self.default_speed = 150
        self.speed = 150
        self.vision = 250
        self.max_health = 800
        self.current_health = 800
        self.vision = 250


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

    def update(self, dt):
        super().update(dt)

