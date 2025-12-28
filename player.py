from projectile import *

#BASIC STATS
#DEFAULT PLAYER
default_health = 100
default_speed = 100
default_vision = 100

#####
#SOLDIER
soldier_health = 300
soldier_speed = 90
soldier_vision = 220

#PRIMARY
soldier_attack_speed = 0.5

#SECONDARY
soldier_health_cost = 0.1
soldier_adrenaline_cd = 2
soldier_adrenaline_duration = 3
soldier_attack_speed_multiplier = 2
soldier_speed_multiplier = 1.5
soldier_damage_multiplier = 1.5

#####
#ALIEN
alien_health = 450
alien_speed = 105
alien_vision = 150

#PASSIVE
alien_damage_reduction = 0.9

#PRIMARY
alien_attack_duration = 0.25
alien_attack_cooldown = 0.4

#SECONDARY
alien_rage_duration = 3
alien_rage_cooldown = 10
alien_slow = 0.5

#####
#Mage
mage_health = 280
mage_speed = 80
mage_vision = 250

#PRIMARY
mage_max_distance = 300
mage_damage_interval = 0.25

#SECONDARY
mage_teleport_range = 300
mage_teleport_cooldown = 8

#####
#Medic sniper
medic_health = 250
medic_speed = 90
medic_vision = 150

#PRIMARY
medic_attack_speed = 0.5

#SECONDARY
medic_take_aim_slow = 0.25
medic_take_aim_damage_multiplier = 5
medic_take_aim_bullet_speed_multiplier = 1.5
medic_take_aim_bonus_vision = 500
medic_take_aim_cooldown = 8


class Player:

    def __init__(self, _id, location):
        self.rect = pygame.rect.Rect(location[0], location[1], 32, 32)
        self.name = "default"
        self.left, self.right, self.up, self.down = 0, 0, 0, 0
        self.id = _id
        self.projectile = []

        #Basic Stat Data
        self.state = 1

        self.health = default_health
        self.vision = default_vision
        self.speed = default_speed
        self.max_health = self.health

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
        self.health = default_health
        self.speed = default_speed
        self.vision = default_vision

    def take_damage(self, value):
        self.health -= value

    def heal(self,value):
        self.health += value
        if self.health > self.max_health:
            self.health = self.max_health

    def set_speed(self, value):
        self.speed = value

    def update_projectile(self, dt, obstacles):
        pass

    def get_damage_dealt(self, enemy, position):
        return []

    def get_slow_applied(self, enemy, ally, position):
        return []

    def get_heal_applied(self, ally, position):
        return []

    def get_projectile(self):
        return []

class Soldier(Player):

    def __init__(self, _id, location):
        super().__init__(_id, location)
        self.name = "soldier"

        #Basic stats
        self.health = soldier_health
        self.speed = soldier_speed
        self.vision = soldier_vision
        self.max_health = soldier_health

        #Primary stats
        self.attack_on_cooldown = False
        self.current_attack_speed = soldier_attack_speed
        self.attack_speed_counter = 0.0

        #Secondary stats
        self.isCooldown = False
        self.health_cost = soldier_health_cost
        self.adrenaline_cooldown = soldier_adrenaline_cd
        self.adrenaline_cooldown_counter = 0.0
        self.isBoosted = False
        self.adrenaline_duration = soldier_adrenaline_duration
        self.adrenaline_counter = 0.0
        self.attack_speed_multiplier = soldier_attack_speed_multiplier
        self.speed_multiplier = soldier_speed_multiplier
        self.damage_multiplier = soldier_damage_multiplier

    def death(self):
        super().death()
        self.attack_on_cooldown = False
        self.isCooldown = False
        self.isBoosted = False
        self.adrenaline_cooldown_counter = 0.0
        self.adrenaline_counter = 0.0

    def get_damage_dealt(self, enemy, position):
        damage = []
        for key, value in position.items():
            if key in enemy:
                x = value["x"]
                y = value["y"]
                rect = pygame.rect.Rect(x, y, 32, 32)
                proj_list = self.projectile
                for proj in proj_list:
                    if rect.clipline(proj.get_trace_line()):
                        damage.append([key, proj.damage])
                        self.projectile.remove(proj)
        return damage

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
                    self.state = 1
                    self.isBoosted = False
                    self.isCooldown = True
                    self.current_attack_speed = soldier_attack_speed
                    self.speed = soldier_speed
                    self.adrenaline_counter = 0
                else:
                    self.adrenaline_counter += dt
                    self.current_attack_speed = soldier_attack_speed / self.attack_speed_multiplier
                    self.speed = soldier_speed * self.speed_multiplier

        super().update(dt)

    def primary(self, location):
        if not self.attack_on_cooldown:
            if self.isBoosted:
                bullet = Bullet(self.rect.centerx, self.rect.centery, location)
                bullet.set_damage(bullet.damage * self.damage_multiplier)
                self.projectile.append(bullet)
            else:
                self.projectile.append(Bullet(self.rect.centerx, self.rect.centery, location))
            self.attack_on_cooldown = True

    def secondary(self):
        if not self.isCooldown and not self.isBoosted:
            if self.health > soldier_health * self.health_cost:
                self.state = 2
                self.isBoosted = True
                self.take_damage(soldier_health * self.health_cost)

    def get_projectile(self):
        data = []
        for proj in self.projectile:
            data.append(proj.to_string())
        return data

    def respawn(self):
        self.isDead = False
        self.health = soldier_health
        self.speed = soldier_speed
        self.vision = soldier_vision

class Alien(Player):

    def __init__(self, _id, location):
        super().__init__(_id, location)
        self.name = "alien"
        self.projectile = Spike(self.rect.centerx, self.rect.centery)

        #BASIC
        self.health = alien_health
        self.speed = alien_speed
        self.vision = alien_vision
        self.max_health = alien_health

        #PASSIVE
        self.damage_reduction = alien_damage_reduction

        #PRIMARY
        self.isAttacking = False
        self.isAttackOnCooldown = False
        self.attack_duration = alien_attack_duration
        self.attack_duration_counter = 0.0
        self.attack_cooldown = alien_attack_cooldown
        self.attack_cooldown_counter = 0.0

        #SECONDARY
        self.rage_duration = alien_rage_duration
        self.isRage = False
        self.isRageCooldown = False
        self.rage_cooldown = alien_rage_cooldown
        self.rage_cooldown_counter = 0.0
        self.rage_duration_counter = 0.0
        self.slow = alien_slow

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
            self.state = 2
            self.isRage = True
            self.isRageCooldown = True
            self.speed = alien_speed * self.slow

    def primary(self):
        if not self.isAttacking and not self.isAttackOnCooldown:
            self.isAttacking = True
            self.projectile.set_pos(self.rect.centerx, self.rect.centery)
            self.isAttackOnCooldown = True

    def get_damage_dealt(self, enemy, position):
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
        return damage

    def take_damage(self, value):
        if not self.isRage:
            self.health -= value * self.damage_reduction
        else:
            self.health += value
            if self.health > alien_health:
                self.health = alien_health

    def update(self, dt):
        if self.isAttacking:
            if self.attack_duration_counter > self.attack_duration:
                self.isAttacking = False
                self.attack_duration_counter = 0.0
                if not self.isRage:
                    self.speed = alien_speed
                else:
                    self.speed = alien_speed * self.slow
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
                self.state = 1
                self.isRage = False
                self.speed = alien_speed
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
            return [self.projectile.to_string()]
        return []

    def respawn(self):
        self.isDead = False
        self.health = alien_health
        self.speed = alien_speed
        self.vision = alien_vision

class Mage(Player):
    def __init__(self, _id, location):
        super().__init__(_id, location)
        self.name = "mage"

        #BASIC
        self.health = mage_health
        self.speed = mage_speed
        self.vision = mage_vision
        self.max_health = mage_health

        #PRIMARY
        self.primary_state = 1
        self.max_distance_from_player = mage_max_distance
        self.isFireActive = True
        self.interval = mage_damage_interval
        self.interval_count = 0

        #SECONDARY
        self.max_teleport_distance = mage_teleport_range
        self.isCooldown = False
        self.cooldown = mage_teleport_cooldown
        self.cooldown_counter = 0.0

    def primary(self,location):
        if self.primary_state == 1 and self.projectile == []:
            fire_zone = FireZone(self.rect.centerx, self.rect.centery, location)
            self.projectile.append(fire_zone)
            self.primary_state = 2
        elif self.primary_state == 2:
            fire_zone = self.projectile[0]
            fire_zone.speed = 0
            fire_zone.set_size(128)
            self.primary_state = 3
            self.projectile[0].phase = 2
        elif self.primary_state == 3:
            self.projectile = []
            self.primary_state = 1

    def secondary(self,node):
        if not self.isCooldown:
            if node.traversable == 1:
                dist = math.hypot(node.rect.centerx - self.rect.centerx, node.rect.centery - self.rect.centery)
                if dist <self.max_teleport_distance:
                    self.rect.center = node.rect.center
                    self.isCooldown = True

    def get_damage_dealt(self, enemy, position):
        damage = []
        if self.primary_state == 3:
            for key, value in position.items():
                if key in enemy and self.isFireActive:
                    x = value["x"]
                    y = value["y"]
                    rect = pygame.rect.Rect(x, y, 32, 32)
                    if self.projectile[0].rect.colliderect(rect):
                        damage.append([key, self.projectile[0].damage])
        if damage:
            self.isFireActive = False
        return damage

    def get_slow_applied(self, enemy, ally, position):
        slow = []
        if self.primary_state == 3:
            for key, value in position.items():
                x = value["x"]
                y = value["y"]
                rect = pygame.rect.Rect(x, y, 32, 32)
                if self.projectile[0].rect.colliderect(rect):
                    slow.append([key, self.projectile[0].slow])
        return slow

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

    def update(self, dt):
        if self.isCooldown:
            if self.cooldown_counter > self.cooldown:
                self.isCooldown = False
                self.cooldown_counter = 0.0
            else:
                self.cooldown_counter += dt
        super().update(dt)

    def get_projectile(self):
        data = []
        for proj in self.projectile:
            data.append(proj.to_string())
        return data

    def death(self):
        super().death()
        self.isCooldown = False
        self.cooldown_counter = 0.0
        self.isFireActive = False
        self.interval_count = 0.0
        self.primary_state = 1
        self.projectile = []

    def respawn(self):
        self.isDead = False
        self.health = mage_health
        self.speed = mage_speed
        self.vision = mage_vision

class MedicSniper(Player):

    def __init__(self, _id, location):
        super().__init__(_id, location)
        self.name = "medic sniper"

        #Basic stats
        self.health = medic_health
        self.speed = medic_speed
        self.vision = medic_vision
        self.max_health = medic_health

        #PRIMARY
        self.attack_on_cooldown = False
        self.current_attack_speed = medic_attack_speed
        self.attack_speed_counter = 0.0

        #SECONDARY
        self.isTakeAim = False
        self.isCooldown = False
        self.slow = medic_take_aim_slow
        self.damage_multiplier = medic_take_aim_damage_multiplier
        self.bullet_speed = medic_take_aim_bullet_speed_multiplier
        self.bonus_vision = medic_take_aim_bonus_vision
        self.take_aim_cooldown = medic_take_aim_cooldown
        self.take_aim_cooldown_counter = 0.0

    def death(self):
        super().death()
        self.isTakeAim = False
        self.isCooldown = False
        self.take_aim_cooldown_counter = 0.0
        self.attack_speed_counter = 0.0
        self.attack_on_cooldown = False

    def get_damage_dealt(self, enemy, position):
        damage = []
        for key, value in position.items():
            if key in enemy:
                x = value["x"]
                y = value["y"]
                rect = pygame.rect.Rect(x, y, 32, 32)
                proj_list = self.projectile
                for proj in proj_list:
                    if proj.id == 2:
                        if rect.clipline(proj.get_trace_line()):
                            damage.append([key, proj.damage])
                            self.projectile.remove(proj)
        return damage

    def get_heal_applied(self, ally, position):
        heal = []
        for key, value in position.items():
            if key in ally and key != self.id:
                x = value["x"]
                y = value["y"]
                rect = pygame.rect.Rect(x, y, 32, 32)
                proj_list = self.projectile
                for proj in proj_list:
                    if proj.id == 5 and proj.rect.colliderect(rect):
                        heal.append([key, proj.heal])
                        self.projectile.remove(proj)
        return heal

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
            if self.take_aim_cooldown_counter > self.take_aim_cooldown:
                self.isCooldown = False
                self.take_aim_cooldown_counter = 0.0
            else:
                self.take_aim_cooldown_counter += dt
        super().update(dt)

    def primary(self, location):
        if not self.attack_on_cooldown:
            if self.isTakeAim:
                bullet = Bullet(self.rect.centerx, self.rect.centery, location)
                bullet.set_damage(bullet.damage * self.damage_multiplier)
                bullet.set_speed(bullet.speed * self.bullet_speed)
                self.projectile.append(bullet)
                self.isTakeAim = False
                self.isCooldown = True
                self.speed = medic_speed
                self.vision = medic_vision
                self.state = 1
            else:
                self.projectile.append(MedicBullet(self.rect.centerx, self.rect.centery, location))
            self.attack_on_cooldown = True

    def secondary(self):
        if not self.isTakeAim and not self.isCooldown:
            self.state = 2
            self.isTakeAim = True
            self.vision += self.bonus_vision
            self.speed *= self.slow

    def get_projectile(self):
        data = []
        for proj in self.projectile:
            data.append(proj.to_string())
        return data

    def update_projectile(self, dt, obstacles):
        for bullet in self.projectile:
            update_flag = 1
            if bullet.rect.x < 0 or bullet.rect.x + bullet.rect.width > 1280 or bullet.rect.y < 0 or bullet.rect.y + bullet.rect.height > 800:
                self.projectile.remove(bullet)
                update_flag = 0
            elif bullet.rect.collidelist(obstacles) != -1:
                self.projectile.remove(bullet)
                update_flag = 0
            elif bullet.id == 2:
                for rect in obstacles:
                    if rect.clipline(bullet.get_trace_line()):
                        self.projectile.remove(bullet)
                        update_flag = 0
                        break
            if update_flag:
                bullet.update(dt)

    def respawn(self):
        self.isDead = False
        self.health = medic_health
        self.speed = medic_speed
        self.vision = medic_vision