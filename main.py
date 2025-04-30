import pygame
from fogOfWar import FogOfWar
from client import Client
import math
from projectile import Projectile

# pygame setup
pygame.init()
#make sure the screen size is divisible by 32
screen = pygame.display.set_mode((1280, 800))
clock = pygame.time.Clock()
running = True
dt = 0


#Global Data
#Where the server sending back to this machine (client)
player_list = []
projectile_list = []

#client data
game_map = pygame.image.load("asset/map.png")
soldier = pygame.image.load("asset/soldier.png")
alien = pygame.image.load("asset/alien.png")
default_player = pygame.image.load("asset/default_player.png")


#INPUTS
host = input("Enter Host Address: ")
port = int(input("Enter Port: "))
choice = input("Choose between [soldier] - [alien]: ")

client = Client(host, port)

fogGrid = FogOfWar(1280, 800)
obstacle = [
    pygame.rect.Rect(288, 64, 95, 95),
    pygame.rect.Rect(384, 96, 31, 31),
    pygame.rect.Rect(384, 320, 31, 63),
    pygame.rect.Rect(416, 320, 31, 31),
    pygame.rect.Rect(64, 512, 95, 127),
    pygame.rect.Rect(160, 544, 127, 159),
    pygame.rect.Rect(352, 448, 31, 63),
    pygame.rect.Rect(384, 480, 31, 31),
    pygame.rect.Rect(512, 448, 95, 31),
    pygame.rect.Rect(576, 416, 31, 31),
    pygame.rect.Rect(576, 320, 63, 31),
    pygame.rect.Rect(544, 544, 31, 95),
    pygame.rect.Rect(576, 576, 95, 95),
    pygame.rect.Rect(672, 576, 95, 31),
    pygame.rect.Rect(768, 512, 127, 95),
    pygame.rect.Rect(896, 576, 95, 63),
    pygame.rect.Rect(832, 256, 159, 63),
    pygame.rect.Rect(960, 224, 31, 31),
    pygame.rect.Rect(864, 320, 127, 31),
    pygame.rect.Rect(896, 352, 95, 31),
    pygame.rect.Rect(1024, 128, 159, 191),
    pygame.rect.Rect(1088, 96, 95, 31),
]

fogGrid.setObstacles(obstacle)
obstacle_list = fogGrid.getBlockedNode()


#Server init
player = client.send(["init", choice])


def handleMovement(_player):
    _player.rect.x += (_player.right - _player.left) * _player.speed * dt
    if _player.rect.x < 0:
        _player.rect.x = 0
    if _player.rect.x + 32 > 1280:
        _player.rect.x = 1280-32
    checkForCollisionHorizontal(_player, fogGrid.getBlockedNode())

    player.rect.y += (player.down - player.up) * player.speed * dt
    if _player.rect.y < 0:
        _player.rect.y = 0
    if _player.rect.y + 32 > 800:
        _player.rect.y = 800-32
    checkForCollisionVertical(_player, fogGrid.getBlockedNode())

def checkForCollisionHorizontal(_player, _obstacle_list):
    for rect in _obstacle_list:
        if _player.rect.colliderect(rect):
            if rect.left < _player.rect.right < rect.right:
                _player.rect.right = rect.left
            elif rect.left < _player.rect.left < rect.right:
                _player.rect.left = rect.right

def checkForCollisionVertical(_player, _obstacle_list):
    for rect in _obstacle_list:
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
                    for obs in obstacle:
                        if obs.clipline(_player.rect.centerx, _player.rect.centery, node.rect.centerx, node.rect.centery):
                            if node.traversable:
                                node.discovered = 0
                                break

            #To remove vision
            else:
                dist = math.hypot(_player.rect.centerx - node.rect.centerx, _player.rect.centery - node.rect.centery)
                if dist > _player.vision:
                    node.discovered = 0
                for obs in obstacle:
                    if obs.clipline(_player.rect.centerx, _player.rect.centery, node.rect.centerx, node.rect.centery):
                        if node.traversable:
                            node.discovered = 0
                            break


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                deltaX = pygame.mouse.get_pos()[0] - player.rect.centerx
                deltaY = pygame.mouse.get_pos()[1] - player.rect.centery
                angle = math.atan2(deltaY, deltaX)
                velY = round(math.sin(angle), 2)
                velX = round(math.cos(angle), 2)
                player.projectile.append(Projectile(player.rect.centerx, player.rect.centery, player.id, pygame.Vector2(velX, velY)))
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
    screen.blit(game_map, (0, 0))

    #return [id, position, name] of other players
    player_list = client.send(["position", player])
    projectile_list = client.send(["projectile", player.id, player.projectile])

    for entity in player_list:
        if entity.id != player.id:
            if entity.name == "soldier":
                screen.blit(soldier, (entity.rect.x, entity.rect.y))
            if entity.name == "alien":
                screen.blit(alien, (entity.rect.x, entity.rect.y))
            if entity.name == "default player":
                screen.blit(default_player, (entity.rect.x, entity.rect.y))

    for proj in projectile_list:
        if proj[0] != player.id:
            proj_list = proj[1]
            for entry in proj_list:
                pygame.draw.rect(screen, "cyan", entry.rect)

    fogGrid.draw()

    handleMovement(player)
    checkVision(player, fogGrid.nodes)

    if player.name == "soldier":
        screen.blit(soldier, (player.rect.x, player.rect.y))
    elif player.name == "alien":
        screen.blit(alien, (player.rect.x, player.rect.y))
    elif player.name == "default player":
        screen.blit(default_player, (player.rect.x, player.rect.y))

    pygame.draw.line(screen, "white", player.rect.center, pygame.mouse.get_pos())

    for proj in player.projectile:
        proj.update(dt)
        if proj.rect.x < 0 or proj.rect.x + proj.size > 1270 or proj.rect.y < 0 or proj.rect.y + proj.size > 790:
            player.projectile.remove(proj)
        elif not fogGrid.getEntityNode(proj).traversable:
            player.projectile.remove(proj)
        pygame.draw.rect(screen, "green", proj.rect)
    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()