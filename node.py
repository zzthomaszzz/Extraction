import pygame

class Node:
    def __init__(self, x, y, size, traversable = 1, spawn = 0):
        self.size = size
        self.rect = pygame.rect.Rect(x, y, self.size, self.size)
        self.traversable = traversable
        self.discovered = 0
        self.isSpawn = spawn
        self.grid_id = [x / self.size, y / self.size]