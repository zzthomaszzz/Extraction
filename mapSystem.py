import pygame
from node import Node
import math

class MapSystem:
    def __init__(self, sizeX, sizeY, obstacles):
        #Grid map is 40 * 25
        self.size = 32
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.nodeX = sizeX / self.size
        self.nodeY = sizeY / self.size

        #Node data
        self.non_traversable_nodes = []
        self.nodes = []
        self.obstacles = obstacles
        self.discovered_nodes = []
        self.initNode()
        self.setObstacles()
        self.previous_player_pos = []
        self.fog_update_distance = 16

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

    def setObstacles(self):
        for item in self.nodes:
            for node in item:
                if node.rect.collidelist(self.obstacles) >= 0:
                    node.traversable = 0
                    self.non_traversable_nodes.append(node)

    def set_player_pos(self, player_pos):
        self.previous_player_pos = player_pos

    def get_adjacent(self, node):
        adj_node = []
        x, y = round(node.grid_id[0]), round(node.grid_id[1])
        #Left
        try:
            adj_node.append(self.nodes[y][x - 1])
        except IndexError:
            pass
        #Top
        try:
            adj_node.append(self.nodes[y - 1][x])
        except IndexError:
            pass
        #Right
        try:
            adj_node.append(self.nodes[y][x + 1])
        except IndexError:
            pass
        #Bottoms
        try:
            adj_node.append(self.nodes[y + 1][x])
        except IndexError:
            pass
        return adj_node

    def handle_fog(self, origin_node, vision, teammate):
        for _node in self.discovered_nodes:
            _node.discovered = 0
        self._handle_fog(origin_node, vision, origin_node)
        for member in teammate:
            self._handle_fog(self.getNodeFromPos(teammate[member][0][0], teammate[member][0][1]), member[1], self.getNodeFromPos(teammate[member][0][0], teammate[member][0][1]))

    def _handle_fog(self, node, vision, originNode):
        dist = math.hypot(node.rect.centerx - originNode.rect.centerx, node.rect.centery - originNode.rect.centery)
        adj = self.get_adjacent(node)
        if not node.discovered:
            if dist <= vision:
                node.discovered = 1
                for _obstacle in self.obstacles:
                    if _obstacle.clipline(node.rect.centerx, node.rect.centery, originNode.rect.centerx, originNode.rect.centery):
                        if node.traversable:
                            node.discovered = 0
                            break
                if node.discovered:
                    self.discovered_nodes.append(node)
                    for _node in adj:
                        if not _node.discovered:
                            self._handle_fog(_node, vision, originNode)


    def getEntityNode(self, _entity):
        x = _entity.rect.x / self.sizeX
        y = _entity.rect.y / self.sizeY
        x *= self.nodeX
        y *= self.nodeY
        return self.nodes[round(y)][round(x)]

    def getNodeFromPos(self, pos_x, pos_y):
        x = pos_x / self.sizeX
        y = pos_y / self.sizeY
        x *= self.nodeX
        y *= self.nodeY
        return self.nodes[round(y)][round(x)]