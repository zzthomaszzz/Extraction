import pygame

class Player:

    def __init__(self, _id):
        self.rect = pygame.rect.Rect(0, 0, 32, 32)
        self.name = "default player_data"
        self.speed = 100
        self.left, self.right, self.up, self.down = 0, 0, 0, 0
        self.vision = 100
        self.max_health = 100
        self.current_health = 100
        self.image_path = "asset/default_player.png"
        self.id = _id
        self.projectile = []
        self.max_projectile = 3
        self.isDead = False

    def update(self, dt):
        self.rect.x += (self.right - self.left) * self.speed * dt
        self.rect.y += (self.down - self.up) * self.speed * dt

    def draw_health_bar(self):
        holder_rect = pygame.rect.Rect(self.rect.x, self.rect.y - 10, 32, 5)
        calculation = (self.current_health / self.max_health) * 32
        real_heath_rect = pygame.rect.Rect(self.rect.x, self.rect.y - 10, calculation, 5)
        pygame.draw.rect(pygame.display.get_surface(), "black", holder_rect)
        pygame.draw.rect(pygame.display.get_surface(), "green", real_heath_rect)

class Soldier(Player):

    def __init__(self, _id):
        super().__init__(_id)
        self.name = "soldier"
        self.speed = 200
        self.vision = 500
        self.max_health = 500
        self.current_health = 500
        self.image_path = "asset/soldier.png"

class Alien(Player):

    def __init__(self, _id):
        super().__init__(_id)
        self.name = "alien"
        self.speed = 300
        self.max_health = 800
        self.current_health = 800
        self.vision = 200
        self.image_path = "asset/alien.png"
