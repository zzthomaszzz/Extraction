import pygame

class Projectile:

    def __init__(self, x, y, size = 5):
        self.size = size
        self.rect = pygame.rect.Rect(0, 0, self.size, self.size)
        self.rect.center = (x, y)

class Bullet(Projectile):

    def __init__(self, x, y, direction, speed, size=5):
        super().__init__(x, y, size)
        self.speed = speed
        self.direction = direction

    def update(self, dt):
        self.rect.x += self.direction[0] * self.speed * dt
        self.rect.y += self.direction[1] * self.speed * dt

class FireBall(Projectile):

    def __init__(self, x, y, index, size=5):
        super().__init__(x, y, size)
        self.speed = 0
        self.direction = [0, 0]
        self.orbit = True
        self.index = index

    def update(self, dt):
        if not self.orbit:
            self.rect.x += self.direction[0] * self.speed * dt
            self.rect.y += self.direction[1] * self.speed * dt

    def fire(self, direction, speed):
        self.direction = direction
        self.speed = speed
        self.orbit = False