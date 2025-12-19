import math
import pygame
import sys

from client import Client
from mapSystem import MapSystem
from player import *
from projectile import Projectile

host = "127.0.0.1"
port = 5000

try:
    client = Client(host, port)
except ConnectionRefusedError as e:
    print("Server is not running or lobby is full")
    sys.exit()

# pygame setup
pygame.init()
#make sure the screen size is divisible by 32
screen = pygame.display.set_mode((1280, 800))
clock = pygame.time.Clock()
running = True
in_menu = True
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

character_choice = "default_player"
team = 1

obstacles = [
    pygame.rect.Rect(224, 288, 63, 63),
    pygame.rect.Rect(128, 352, 63, 63),
    pygame.rect.Rect(256, 704, 31, 31),
    pygame.rect.Rect(256, 576, 63, 63),
    pygame.rect.Rect(896, 0, 31, 63),
    pygame.rect.Rect(352, 192, 63, 63),
    pygame.rect.Rect(512, 160, 95, 63),
    pygame.rect.Rect(32, 256, 127, 31),
    pygame.rect.Rect(32, 288, 31, 63),
    pygame.rect.Rect(256, 448, 31, 127),
    pygame.rect.Rect(288, 96, 63, 63),
    pygame.rect.Rect(384, 320, 31, 63),
    pygame.rect.Rect(288, 640, 127, 31),
    pygame.rect.Rect(384, 544, 63, 31),
    pygame.rect.Rect(320, 736, 95, 63),
    pygame.rect.Rect(480, 256, 63, 63),
    pygame.rect.Rect(512, 384, 31, 31),
    pygame.rect.Rect(576, 320, 63, 31),
    pygame.rect.Rect(544, 448, 63, 31),
    pygame.rect.Rect(512, 480, 63, 63),
    pygame.rect.Rect(480, 672, 127, 31),
    pygame.rect.Rect(512, 704, 31, 31),
    pygame.rect.Rect(608, 608, 127, 31),
    pygame.rect.Rect(672, 480, 31, 31),
    pygame.rect.Rect(768, 512, 127, 95),
    pygame.rect.Rect(928, 576, 63, 63),
    pygame.rect.Rect(1152, 448, 31, 63),
    pygame.rect.Rect(832, 416, 31, 63),
    pygame.rect.Rect(1024, 416, 63, 31),
    pygame.rect.Rect(896, 320, 95, 63),
    pygame.rect.Rect(1024, 352, 31, 63),
    pygame.rect.Rect(704, 352, 31, 63),
    pygame.rect.Rect(832, 288, 31, 31),
    pygame.rect.Rect(768, 192, 31, 31),
    pygame.rect.Rect(1024, 224, 63, 63),
    pygame.rect.Rect(672, 256, 63, 31),
    pygame.rect.Rect(608, 64, 95, 63),
    pygame.rect.Rect(768, 64, 95, 63),
    pygame.rect.Rect(1024, 96, 63, 63),
]

heal_zone = [
    pygame.rect.Rect(64, 288, 31, 31),
    pygame.rect.Rect(608, 736, 31, 31),
    pygame.rect.Rect(1056, 384, 31, 31),
    pygame.rect.Rect(576, 32, 31, 31),
]

start_zone = [
    [pygame.rect.Rect(0, 0, 96, 96), 1],
    [pygame.rect.Rect(1184, 704, 96, 96), 2],
]

character_zone = [
    [pygame.rect.Rect(544, 384, 32, 32), "soldier"],
    [pygame.rect.Rect(608, 384, 32, 32), "mage"],
    [pygame.rect.Rect(480, 384, 32, 32), "alien"],
]

teammate_data = {}

capture_zone = pygame.rect.Rect(512, 320, 255, 127)

team_progress = {"1": 0, "2": 0}

spawn_zone = [
    pygame.rect.Rect(0, 0, 96, 96),
    pygame.rect.Rect(1184, 704, 96, 96),
]

map_system = MapSystem(1280, 800, obstacles, spawn_zone)


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


while in_menu:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            in_menu = False
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for spawning_zone in start_zone:
                    if spawning_zone[0].collidepoint(pygame.mouse.get_pos()):
                        team = spawning_zone[1]
                for character in character_zone:
                    if character[0].collidepoint(pygame.mouse.get_pos()):
                        character_choice = character[1]
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                in_menu = False

    screen.blit(game_map, (0, 0))

    for spawning_zone in start_zone:
        if spawning_zone[1] == team:
            pygame.draw.rect(screen, "green", spawning_zone[0], 2)
        else:
            pygame.draw.rect(screen, "blue", spawning_zone[0], 2)

    for character in character_zone:
        if character[1] == character_choice:
            pygame.draw.rect(screen, "green", character[0], 2)
        else:
            pygame.draw.rect(screen, "blue", character[0], 2)
        match character[1]:
            case "soldier":
                _image = soldier
            case "mage":
                _image = mage
            case "alien":
                _image = alien
            case _:
                _image = default_player
        screen.blit(_image, (character[0].x, character[0].y))


    pygame.display.flip()

    dt = clock.tick(60) / 1000


client_id = client.send(["initialize", character_choice, team])

if client_id is None:
    print("Failed to receive initial id")
    sys.exit()

player = Player(client_id, [start_zone[team-1][0].x, start_zone[team-1][0].y])

if player is None:
    print("Failed to create player object")
    sys.exit()

map_system.set_player_pos([player.rect.centerx, player.rect.centery])

refresh_rate = 0.25
refresh_counter = 0

point = 0

winner = ""
in_winner_screen = True

dead_timer = 5
dead_counter = 0

spawn = {"1": [0,0], "2": [1247, 767]}

spawn_bar = {"1": [0,0], "2": [1184, 704]}

win_condition = 100

show_grid = False

all_player_character = client.send(["all player character", player.id])

while running:

    if player.isDead:
        player.rect.x, player.rect.y = spawn[str(team)][0], spawn[str(team)][1]
        dead_counter += dt
        if dead_counter > dead_timer:
            player.isDead = False
            player.current_health = player.max_health
            dead_counter = 0
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            in_winner_screen = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and not player.isDead:
                player.basic_attack(pygame.mouse.get_pos())
            if event.button == 3 and not player.isDead:
                player.alternate_attack(pygame.mouse.get_pos())
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_t:
                if show_grid:
                    show_grid = False
                else:
                    show_grid = True
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
                in_winner_screen = False
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

    # This will return {"_id":[[x, y], team], "_id":[[x, y], team]}
    all_player_location = client.send(["all location", [player.rect.x, player.rect.y], team])

    #This will return {"_id": [[projectile.rect, projectile.rect], player.damage]}
    all_player_projectile = client.send(["all player projectile", player.get_projectile_data(), player.damage])

    #This will return {"_id": [current_health, max_health]}
    all_player_health = client.send(["all player health", [player.current_health, player.max_health]])

    #This return team progress for capture the flag
    team_progress = client.send(["team progress", player.id])

    if team_progress == "1" or team_progress == "2" or team_progress == "3" or team_progress == "4":
        winner = team_progress
        break

    #Client update
    player.update(dt)

    handle_player(player)

    player.handle_projectile(obstacles, dt)

    refresh_counter += dt
    if refresh_counter > refresh_rate:
        map_system.handle_fog(map_system.getEntityNode(player), player.vision)
        refresh_counter = 0

    for _node in heal_zone:
        if player.rect.colliderect(_node):
            player.heal(50 * dt)


    if player.rect.colliderect(capture_zone):
        point += dt
    if point > 1:
        client.send_no_recv(["capture", str(team)])
        point = 0

    # fill the screen with a color to wipe away anything from last frame
    screen.blit(game_map, (0, 0))

    #Drawing all players and their health bars
    #Note that the main player character will not be covered by fog
    for entity in all_active_player:
        if entity in all_player_character and entity in all_player_location and entity in all_player_health:
            match all_player_character[entity]:
                case "mage":
                    _image = mage
                case "soldier":
                    _image = soldier
                case "alien":
                    _image = alien
                case _:
                    _image = default_player
            screen.blit(_image, all_player_location[entity][0])

            max_hp_rect = pygame.rect.Rect(all_player_location[entity][0][0], all_player_location[entity][0][1] - 10, 32, 5)
            current_hp_bar = (all_player_health[entity][0] / all_player_health[entity][1]) * 32
            current_hp_rect = pygame.rect.Rect(all_player_location[entity][0][0], all_player_location[entity][0][1] - 10, current_hp_bar, 5)
            pygame.draw.rect(pygame.display.get_surface(), "black", max_hp_rect)
            if all_player_location[entity][1] == team:
                pygame.draw.rect(pygame.display.get_surface(), "green", current_hp_rect)
            else:
                pygame.draw.rect(pygame.display.get_surface(), "red", current_hp_rect)

    #Drawing all projectile
    for entity in all_active_player:
        if entity in all_player_projectile and entity in all_player_location:
            for _proj in all_player_projectile[entity][0]:
                pygame.draw.rect(screen, "red", _proj, 1)

    #Drawing fog of war
    map_system.draw()

    #Drawing progress bar
    for key in team_progress:
        progress_bar = pygame.rect.Rect(spawn_bar[key][0], spawn_bar[key][1], 95, 5)
        current_progress = (team_progress[key] / win_condition) * 95
        current_progress_bar = pygame.rect.Rect(spawn_bar[key][0], spawn_bar[key][1], current_progress, 5)
        pygame.draw.rect(screen, "black", progress_bar)
        pygame.draw.rect(screen, "purple", current_progress_bar)

    #Test Drawing
    if show_grid:
        for i in map_system.nodes:
            for _node in i:
                pygame.draw.rect(screen, "red", _node.rect, 1)
    for _ in obstacles:
        pygame.draw.rect(screen, "black", _, 2)



    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

while in_winner_screen:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            in_winner_screen = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                in_winner_screen = False

    screen.blit(game_map, (0, 0))

    if winner == "1":
        pygame.draw.rect(screen, "green", start_zone[0][0])
    elif winner == "2":
        pygame.draw.rect(screen, "green", start_zone[1][0])

    pygame.display.flip()

pygame.quit()
