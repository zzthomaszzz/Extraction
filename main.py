import math
import pygame
from player import Player
from fogOfWar import FogOfWar

# pygame setup
pygame.init()
#make sure the screen size is divisible by 32
screen = pygame.display.set_mode((1280, 800))
clock = pygame.time.Clock()
running = True
dt = 0

obstacle = [
    pygame.rect.Rect(200, 50, 50, 50),
    pygame.rect.Rect(1000, 500, 50, 50),
    pygame.rect.Rect(200, 600, 50, 50),
    pygame.rect.Rect(500, 230, 32, 50),
    pygame.rect.Rect(250, 50, 50, 50),
    pygame.rect.Rect(250, 100, 50, 50)
]

fogGrid = FogOfWar(1280, 800)

fogGrid.setObstacles(obstacle)

player = Player()

def handleMovement(_player):
    _player.rect.x += (_player.right - _player.left) * _player.speed * dt
    checkForCollisionHorizontal(_player, fogGrid.getBlockedNode())

    player.rect.y += (player.down - player.up) * player.speed * dt
    checkForCollisionVertical(_player, fogGrid.getBlockedNode()
                              )

def checkForCollisionHorizontal(_player, obstacle_list):
    for rect in obstacle_list:
        if _player.rect.colliderect(rect):
            if rect.left < _player.rect.right < rect.right:
                _player.rect.right = rect.left
            elif rect.left < _player.rect.left < rect.right:
                _player.rect.left = rect.right

def checkForCollisionVertical(_player, obstacle_list):
    for rect in obstacle_list:
        if _player.rect.colliderect(rect):
            if rect.top < _player.rect.top < rect.bottom:
                _player.rect.top = rect.bottom
            elif rect.top < _player.rect.bottom < rect.bottom:
                _player.rect.bottom = rect.top

def checkVision(_player, nodes):
    for item in nodes:
        for node in item:
            if not node.discovered:
                dist = math.hypot(_player.rect.centerx - node.rect.centerx, _player.rect.centery - node.rect.centery)
                if dist <= _player.vision:
                    node.discovered = 1
            #To remove vision
            else:
                dist = math.hypot(_player.rect.centerx - node.rect.centerx, _player.rect.centery - node.rect.centery)
                if dist > _player.vision:
                    node.discovered = 0


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                player.left = 1
            if event.key == pygame.K_d:
                player.right = 1
            if event.key == pygame.K_s:
                player.down = 1
            if event.key == pygame.K_w:
                player.up = 1
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                player.left = 0
            if event.key == pygame.K_d:
                player.right = 0
            if event.key == pygame.K_s:
                player.down = 0
            if event.key == pygame.K_w:
                player.up = 0

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    pygame.draw.rect(screen, "white", fogGrid.getPlayerNode(player))
    fogGrid.draw()
    for i in obstacle:
        pygame.draw.rect(screen, "blue", i)



    handleMovement(player)
    checkVision(player, fogGrid.nodes)

    pygame.draw.rect(screen, "yellow", player.rect)


    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()