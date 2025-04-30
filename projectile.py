import pygame

class Projectile:

    def __init__(self, x, y,_id, velocity, speed):
        self.id = _id
        self.x = x
        self.y = y
        self.size = 10
        self.speed = speed
        self.rect = pygame.rect.Rect(0, 0, self.size, self.size)
        self.rect.center = (self.x, self.y)
        self.velocity = velocity
        #Bullet doing double damage
        self.damage = 25

    def update(self, dt):
        self.rect.x += self.velocity[0] * self.speed * dt
        self.rect.y += self.velocity[1] * self.speed * dt

