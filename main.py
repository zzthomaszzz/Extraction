import math
import pygame

from client import Client
from mapSystem import MapSystem
from projectile import Projectile

# pygame setup
pygame.init()
#make sure the screen size is divisible by 32
screen = pygame.display.set_mode((1280, 800))
clock = pygame.time.Clock()
running = True
dt = 0

#Global Data
#Where the server data will come through

#list=[_id, _id, _id], We will need this to iterate through dictionaries
all_active_player = []

#dict={"_id": [x, y]}
all_player_location = {}

#dict={"_id": "character_name"}
all_player_character = {}

#dict={"_id":[ Projectile(), Projectile()]}
all_player_projectile = {}

#dict={"_id": int health}
all_player_health = {}

#Older version
projectile_list = []

#client data
game_map = pygame.image.load("asset/map.png")
soldier = pygame.image.load("asset/soldier.png")
alien = pygame.image.load("asset/alien.png")
mage = pygame.image.load("asset/mage.png")
default_player = pygame.image.load("asset/default_player.png")

#INPUTS
host = "127.0.0.1"
port = 5000
character_choice = "soldier"

client = Client(host, port)

obstacles = [
    pygame.rect.Rect(64, 512, 63, 63),
    pygame.rect.Rect(160, 544, 63, 63),
    pygame.rect.Rect(224, 288, 63, 63),
    pygame.rect.Rect(352, 192, 63, 63),
    pygame.rect.Rect(512, 160, 96, 63),
    pygame.rect.Rect(352, 448, 63, 63),
    pygame.rect.Rect(32, 256, 127, 31),
    pygame.rect.Rect(32, 288, 31, 63),
]

map_system = MapSystem(1280, 800, obstacles)

#Server init
player = client.send(["initialize", character_choice])
map_system.set_player_pos([player.rect.centerx, player.rect.centery])


def handle_player(_player):
    _player.rect.x += (_player.right - _player.left) * _player.speed * dt
    if _player.rect.x < 0:
        _player.rect.x = 0
    if _player.rect.x + 32 > 1280:
        _player.rect.x = 1280 - 32
    adjust_horizontal(_player, map_system.obstacles)

    _player.rect.y += (_player.down - _player.up) * _player.speed * dt
    if _player.rect.y < 0:
        _player.rect.y = 0
    if _player.rect.y + 32 > 800:
        _player.rect.y = 800 - 32
    adjust_vertical(_player, map_system.obstacles)


def handle_projectile(_projectiles):
    for _projectile in _projectiles:
        _projectile.update(dt)
        if _projectile.rect.x < 0 or _projectile.rect.x + _projectile.size > 1280 or _projectile.rect.y < 0 or _projectile.rect.y + _projectile.size > 800:
            _projectiles.remove(_projectile)
        elif _projectile.rect.collidelist(obstacles) >= 0:
            _projectiles.remove(_projectile)


def adjust_horizontal(_player, _obstacle_list):
    for rect in _obstacle_list:
        if _player.rect.colliderect(rect):
            if rect.left < _player.rect.right < rect.right:
                _player.rect.right = rect.left
                break
            elif rect.left < _player.rect.left < rect.right:
                _player.rect.left = rect.right
                break


def adjust_vertical(_player, _obstacle_list):
    for rect in _obstacle_list:
        if _player.rect.colliderect(rect):
            if rect.top < _player.rect.top < rect.bottom:
                _player.rect.top = rect.bottom
                break
            elif rect.top < _player.rect.bottom < rect.bottom:
                _player.rect.bottom = rect.top
                break


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                player.basic_attack(pygame.mouse.get_pos())
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

    #Resolving Server Data

    # This will return [_id, _id, _id]
    all_active_player = client.send(["all active player", player.id])

    # This will return {"_id":[x, y], "_id":[x, y]}
    all_player_location = client.send(["all location", [player.rect.x, player.rect.y]])

    # This will return {"_id": "character name"}
    all_player_character = client.send(["all player character", player.id])

    #This will return {"_id": [projectile.rect, projectile.rect]}
    all_player_projectile = client.send(["all player projectile", player.get_projectile_data()])

    #This will return {"_id": [current_health, max_health]}
    all_player_health = client.send(["all player health", [player.current_health, player.max_health]])

    # fill the screen with a color to wipe away anything from last frame
    screen.blit(game_map, (0, 0))

    #return [id, position, name] of other players

    #Drawing all player
    #Note that the main player character will not be covered by fog
    for entity in all_active_player:
        if entity in all_player_character:
            match all_player_character[entity]:
                case "mage":
                    _image = mage
                case "soldier":
                    _image = soldier
                case "alien":
                    _image = alien
                case _:
                    _image = default_player
            if entity in all_player_location:
                screen.blit(_image, all_player_location[entity])

    #Drawing all health bar
    for entity in all_active_player:
        if entity in all_player_location and entity in all_player_health:
            max_hp_rect = pygame.rect.Rect(all_player_location[entity][0], all_player_location[entity][1] - 10, 32, 5)
            current_hp_bar = (all_player_health[entity][0] / all_player_health[entity][1]) * 32
            current_hp_rect = pygame.rect.Rect(all_player_location[entity][0], all_player_location[entity][1] - 10, current_hp_bar, 5)
            pygame.draw.rect(pygame.display.get_surface(), "black", max_hp_rect)
            pygame.draw.rect(pygame.display.get_surface(), "green", current_hp_rect)

    #Drawing all projectile
    for entity in all_active_player:
        if entity in all_player_projectile:
            for _proj in all_player_projectile[entity]:
                if _proj.colliderect(player.rect) and not entity == player.id:
                    player.take_damage(25)
                pygame.draw.rect(screen, "red", _proj, 1)

    #Drawing fog of war
    map_system.draw()

    #Client update
    player.update(dt)

    handle_player(player)

    handle_projectile(player.projectile)

    map_system.handle_fog(map_system.getEntityNode(player), player.vision, [player.rect.centerx, player.rect.centery])


    #Testing Feature

    for _object in obstacles:
        pygame.draw.rect(screen, "blue", _object, 1)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
