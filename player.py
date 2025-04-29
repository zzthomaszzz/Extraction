import pygame

class Player:

    def __init__(self, _id):
        self.rect = pygame.rect.Rect(0, 0, 32, 32)
        self.speed = 100
        self.left, self.right, self.up, self.down = 0, 0, 0, 0
        self.vision = 100
        self.id = _id

    def update(self, dt):
        self.rect.x += (self.right - self.left) * self.speed * dt
        self.rect.y += (self.down - self.up) * self.speed * dt

    def draw(self):
        pygame.draw.rect(pygame.display.get_surface(), "yellow", self.rect)


class Soldier(Player):

    def __init__(self, _id):
        super().__init__(_id)
        self.speed = 250
        self.vision = 300
