import pygame

class Player:

    def __init__(self, _id):
        self.rect = pygame.rect.Rect(0, 0, 32, 32)
        self.name = "default player"
        self.speed = 100
        self.left, self.right, self.up, self.down = 0, 0, 0, 0
        self.vision = 100
        self.image_path = "asset/default_player.png"
        self.id = _id

    def update(self, dt):
        self.rect.x += (self.right - self.left) * self.speed * dt
        self.rect.y += (self.down - self.up) * self.speed * dt

    def draw(self):
        pygame.draw.rect(pygame.display.get_surface(), "yellow", self.rect)

class Soldier(Player):

    def __init__(self, _id):
        super().__init__(_id)
        self.name = "soldier"
        self.speed = 250
        self.vision = 300
        self.image_path = "asset/soldier.png"

class Alien(Player):

    def __init__(self, _id):
        super().__init__(_id)
        self.name = "alien"
        self.speed = 300
        self.vision = 250
        self.image_path = "asset/alien.png"
