import pygame

class Player:

    def __init__(self):
        self.rect = pygame.rect.Rect(0, 0, 32, 32)
        self.speed = 250
        self.left, self.right, self.up, self.down = 0, 0, 0, 0
        self.vision = 400

    def update(self, dt):
        self.rect.x += (self.right - self.left) * self.speed * dt
        self.rect.y += (self.down - self.up) * self.speed * dt

    def draw(self):
        pygame.draw.rect(pygame.display.get_surface(), "yellow", self.rect)