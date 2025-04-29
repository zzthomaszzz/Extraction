import pygame

class Node:
    def __init__(self, x, y, size, traversable = 1):
        self.x = x
        self.y = y
        self.size = size
        self.rect = pygame.rect.Rect(self.x, self.y, self.size, self.size)
        self.traversable = traversable
        self.discovered = 0