import pygame
from node import Node

class FogOfWar:
    def __init__(self, sizeX, sizeY):
        self.size = 32
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.nodeX = sizeX / self.size
        self.nodeY = sizeY / self.size
        self.nodes = []
        self.initNode()

    def initNode(self):
        y = 0
        while y < self.nodeY:
            self.nodes.append([])
            x = 0
            while x < self.nodeX:
                self.nodes[y].append(Node(x * self.size, y * self.size, self.size))
                x += 1
            y += 1

    def draw(self):
        for i in self.nodes:
            for node in i:
                if not node.discovered:
                    pygame.draw.rect(pygame.display.get_surface(), "black", node.rect)

    def setObstacles(self, obstacle_list):
        for obstacle in obstacle_list:
            for item in self.nodes:
                for node in item:
                    if obstacle.colliderect(node.rect):
                        node.traversable = 0

    def getBlockedNode(self):
        blocked_nodes = []
        for i in self.nodes:
            for node in i:
                if not node.traversable:
                    blocked_nodes.append(node.rect)
        return blocked_nodes

    def getEntityNode(self, _entity):
        x = _entity.rect.x / self.sizeX
        y = _entity.rect.y / self.sizeY
        x *= self.nodeX
        y *= self.nodeY
        return self.nodes[round(y)][round(x)]