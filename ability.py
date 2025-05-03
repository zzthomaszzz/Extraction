import pygame

class Ability:

    def __init__(self, x, y, size):
        self.size = size
        self.rect = pygame.rect.Rect(0, 0, self.size, self.size)
        self.rect.center = (x, y)