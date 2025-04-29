import pygame

class Player:

    def __init__(self, name):
        self.rect = pygame.rect.Rect(0, 0, 32, 32)
        self.speed = 150
        self.left, self.right, self.up, self.down = 0, 0, 0, 0
        self.vision = 200
        self.name = name

    def update(self, dt):
        self.rect.x += (self.right - self.left) * self.speed * dt
        self.rect.y += (self.down - self.up) * self.speed * dt

    def draw(self):
        pygame.draw.rect(pygame.display.get_surface(), "yellow", self.rect)