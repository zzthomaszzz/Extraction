import pygame

class Projectile:

    def __init__(self, x, y, size = 5):
        self.size = size
        self.rect = pygame.rect.Rect(0, 0, self.size, self.size)
        self.rect.center = (x, y)

class Bullet(Projectile):

    def __init__(self, x, y, direction, size=5):
        super().__init__(x, y, size)
        self.speed = 600
        self.direction = direction

    def update(self, dt):
        self.rect.x += self.direction[0] * self.speed * dt
        self.rect.y += self.direction[1] * self.speed * dt

class FireBall(Projectile):

    def __init__(self, x, y, index, size=5):
        super().__init__(x, y, size)
        self.speed = 500
        self.direction = [0, 0]
        self.orbit = True
        self.index = index

    def update(self, dt):
        if not self.orbit:
            self.rect.x += self.direction[0] * self.speed * dt
            self.rect.y += self.direction[1] * self.speed * dt

    def fire(self, direction):
        self.direction = direction
        self.orbit = False


class Claw(Projectile):
    def __init__(self, x, y, size=60):
        super().__init__(x, y, size)
        self.linger_time = 0.2
        self.counter = 0
        self.kill = False

    def update(self, dt):
        if not self.kill:
            self.counter += dt
        if self.counter > self.linger_time:
            self.kill = True