import math
from math import hypot

from projectile import *

class Player:

    def __init__(self, _id, location, vision = 100, health = 100, speed = 100):
        self.rect = pygame.rect.Rect(location[0], location[1], 32, 32)
        self.name = "default"
        self.left, self.right, self.up, self.down = 0, 0, 0, 0
        self.id = _id
        self.projectile = []

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
        if self.health < 0:
            self.death()

    def death(self):
        self.isDead = True
        self.health = 0
        self.vision = 0
        self.speed = 0

    def respawn(self):
        self.isDead = False
        self.health = self.max_health
        self.speed = self.default_speed
        self.vision = self.default_vision

    def init_basic_stats(self):
        self.health = self.max_health
        self.speed = self.default_speed
        self.vision = self.default_vision

    def take_damage(self, value):
        self.health -= value

    def modify_speed(self, value):
        self.speed = self.default_speed * value

    def update_projectile(self, dt, obstacles):
        pass

    def process_projectiles(self, enemy, ally, position):
        return [], []

    def get_projectile(self):
        return []

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

    def death(self):
        super().death()
        self.attack_on_cooldown = False
        self.isCooldown = False
        self.isBoosted = False
        self.adrenaline_cooldown_counter = 0.0
        self.adrenaline_counter = 0.0

    def process_projectiles(self, enemy, ally, position):
        damage = []
        for key, value in position.items():
            if key in enemy:
                x = value["x"]
                y = value["y"]
                rect = pygame.rect.Rect(x, y, 32, 32)
                proj_list = self.projectile
                for proj in proj_list:
                    if proj.rect.colliderect(rect):
                        damage.append([key, proj.damage])
                        self.projectile.remove(proj)
        return [], damage

    def update_projectile(self, dt, obstacles):
        for bullet in self.projectile:
            bullet.update(dt)
            if bullet.rect.x < 0 or bullet.rect.x + bullet.rect.width > 1280 or bullet.rect.y < 0 or bullet.rect.y + bullet.rect.height > 800:
                self.projectile.remove(bullet)
            elif bullet.rect.collidelist(obstacles) != -1:
                self.projectile.remove(bullet)

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
                bullet.set_damage(bullet.damage * 2)
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

    def get_projectile(self):
        return self.projectile

class Alien(Player):

    def __init__(self, _id, location):
        super().__init__(_id, location, 250, 800, 150)
        self.name = "alien"
        self.projectile = Spike(self.rect.centerx, self.rect.centery, _id)

        #PASSIVE
        self.damage_reduction = 0.8

        #PRIMARY
        self.isAttacking = False
        self.isAttackOnCooldown = False
        self.attack_duration = 0.25
        self.attack_duration_counter = 0.0
        self.attack_cooldown = 0.25
        self.attack_cooldown_counter = 0.0

        #SECONDARY
        self.rage_duration = 3
        self.isRage = False
        self.isRageCooldown = False
        self.rage_cooldown = 10
        self.rage_cooldown_counter = 0.0
        self.rage_duration_counter = 0.0
        self.slow = 0.5

    def death(self):
        super().death()
        self.isAttacking = False
        self.isAttackOnCooldown = False
        self.isRage = False
        self.isRageCooldown = False
        self.rage_duration_counter = 0.0
        self.rage_duration_counter = 0.0

    def secondary(self):
        if not self.isRage and not self.isRageCooldown:
            self.isRage = True
            self.isRageCooldown = True
            self.speed = self.default_speed * self.slow

    def primary(self):
        if not self.isAttacking and not self.isAttackOnCooldown:
            self.isAttacking = True
            self.projectile.set_pos(self.rect.centerx, self.rect.centery)
            self.isAttackOnCooldown = True

    def process_projectiles(self, enemy, ally, position):
        damage = []
        for key, value in position.items():
            if key in enemy:
                x = value["x"]
                y = value["y"]
                rect = pygame.rect.Rect(x, y, 32, 32)
                if self.projectile.rect.colliderect(rect) and self.isAttacking:
                    damage.append([key, self.projectile.damage])
        if damage:
            self.isAttacking = False
        return [], damage

    def take_damage(self, value):
        if not self.isRage:
            self.health -= value * self.damage_reduction
        else:
            self.health += value
            if self.health > self.max_health:
                self.health = self.max_health

    def update(self, dt):
        if self.isAttacking:
            if self.attack_duration_counter > self.attack_duration:
                self.isAttacking = False
                self.attack_duration_counter = 0.0
                if not self.isRage:
                    self.speed = self.default_speed
                else:
                    self.speed = self.default_speed * self.slow
            else:
                self.attack_duration_counter += dt
                self.speed = 0
        elif not self.isAttacking and self.isAttackOnCooldown:
            if self.attack_cooldown_counter > self.attack_cooldown:
                self.isAttackOnCooldown = False
                self.attack_cooldown_counter = 0.0
            else:
                self.attack_cooldown_counter += dt

        if self.isRage:
            if self.rage_duration_counter > self.rage_duration:
                self.isRage = False
                self.speed = self.default_speed
                self.rage_duration_counter = 0.0
            else:
                self.rage_duration_counter += dt
        elif not self.isRage and self.isRageCooldown:
            if self.rage_cooldown_counter > self.rage_cooldown:
                self.isRageCooldown = False
                self.rage_cooldown_counter = 0.0
            else:
                self.rage_cooldown_counter += dt
        super().update(dt)

    def get_projectile(self):
        if self.isAttacking:
            return [self.projectile]
        return []

class Mage(Player):
    def __init__(self, _id, location):
        super().__init__(_id, location, 350, 500, 130)
        self.name = "mage"

        #PRIMARY
        self.primary_state = 1
        self.max_distance_from_player = 300
        self.isFireActive = True
        self.interval = 0.25
        self.interval_count = 0

        #SECONDARY
        self.max_teleport_distance = 350
        self.isCooldown = False
        self.cooldown = 5
        self.cooldown_counter = 0.0

    def death(self):
        self.isCooldown = False
        self.cooldown_counter = 0.0
        self.isFireActive = False
        self.interval_count = 0.0
        self.primary_state = 1
        self.projectile = []

    def primary(self,location):
        if self.primary_state == 1 and self.projectile == []:
            print("Phase 2")
            fire_zone = FireZone(self.rect.centerx, self.rect.centery, location, self.id)
            self.projectile.append(fire_zone)
            self.primary_state = 2
        elif self.primary_state == 2:
            print("Phase 3")
            fire_zone = self.projectile[0]
            fire_zone.speed = 0
            fire_zone.set_size(128)
            self.primary_state = 3
            self.projectile[0].phase = 2
        elif self.primary_state == 3:
            print("Phase 1")
            self.projectile = []
            self.primary_state = 1

    def secondary(self,node):
        if not self.isCooldown:
            if node.traversable == 1:
                dist = math.hypot(node.rect.centerx - self.rect.centerx, node.rect.centery - self.rect.centery)
                if dist <self.max_teleport_distance:
                    self.rect.center = node.rect.center
                    self.isCooldown = True


    def update_projectile(self, dt, obstacles):
        if self.primary_state == 2:
            self.projectile[0].update(dt)
            if self.projectile[0].rect.collidelist(obstacles) != -1:
                self.projectile[0].speed = 0
                self.projectile[0].set_size(128)
                self.projectile[0].phase = 2
                self.primary_state = 3
        elif self.primary_state == 3:
            if not self.isFireActive:
                if self.interval_count > self.interval:
                    self.interval_count = 0
                    self.isFireActive = True
                else:
                    self.interval_count += dt
            distance = math.hypot(self.projectile[0].rect.centerx - self.rect.centerx, self.projectile[0].rect.centery - self.rect.centery)
            if distance > self.max_distance_from_player:
                self.projectile = []
                self.primary_state = 1

    def process_projectiles(self, enemy, ally, position):
        slow = []
        damage = []
        if self.primary_state == 3:
            for key, value in position.items():
                x = value["x"]
                y = value["y"]
                rect = pygame.rect.Rect(x, y, 32, 32)
                if self.projectile[0].rect.colliderect(rect):
                    slow.append([key, self.projectile[0].slow])
                    if key in enemy and self.isFireActive:
                        damage.append([key, self.projectile[0].damage])
        if damage:
            self.isFireActive = False
        return slow, damage

    def update(self, dt):
        if self.isCooldown:
            if self.cooldown_counter > self.cooldown:
                self.isCooldown = False
                self.cooldown_counter = 0.0
            else:
                self.cooldown_counter += dt
        super().update(dt)

    def get_projectile(self):
        return self.projectile

