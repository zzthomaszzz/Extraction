import math

import pygame
import sys

from client import Client
from mapSystem import MapSystem
from player import *
from projectile import *

host = "127.0.0.1"
port = 5000

try:
    client = Client(host, port)
except ConnectionRefusedError as e:
    print("Server is not in_game or in_lobby is full")
    sys.exit()

def isEnemy(_id):
    if team_choice == 1:
        if _id in team_2:
            return True
    if team_choice == 2:
        if _id in team_1:
            return True
    return False

def getEnemyTeam():
    if team_choice == 1:
        return team_2
    elif team_choice == 2:
        return team_1

def getAllyTeam():
    if team_choice == 1:
        return team_1
    elif team_choice == 2:
        return team_2

def get_projectiles(_packet):
    data = []
    for key, value in _packet.items():
        if key != "team 1" and key != "team 2":
            for _proj in value["proj"]:
                data.append(_proj)
    return data

def get_hp_percent():
    return player.health / player.max_health

def get_character_image(name):
    match name:
        case "mage":
            data = mage
        case "soldier":
            data = soldier
        case "alien":
            data = alien
        case _:
            data = default_player
    return data

def to_color(number):
    match number:
        case 1:
            _color = (255, 0, 0)
        case 2:
            _color = (0, 255, 0)
        case 3:
            _color = (0, 0, 255)
        case 4:
            _color = (255, 255, 255)
        case 5:
            _color = (0, 255, 255)
        case 6:
            _color = (255, 255, 0)
        case _:
            _color = (0, 0, 0)
    return _color

def use_primary():
    match character_choice:
        case "soldier":
            player.primary(pygame.mouse.get_pos())
        case _:
            pass

def use_secondary():
    match character_choice:
        case "soldier":
            player.secondary()
        case _:
            pass

#-----------------------------------------------------------------------------------------------------------------------
#PRE-LOBBY
pygame.init()
#make sure the screen size is divisible by 32

#ASSETS
game_map = pygame.image.load("asset/map.png")
lobby = pygame.image.load("asset/lobby.png")
soldier = pygame.image.load("asset/soldier.png")
alien = pygame.image.load("asset/alien.png")
mage = pygame.image.load("asset/mage.png")
default_player = pygame.image.load("asset/default_player.png")
bullet = pygame.image.load("asset/bullet.png")
slow_phase_1 = pygame.image.load("asset/slow_1.png")
slow_phase_2 = pygame.image.load("asset/slow_2.png")

character_choice = None
team_choice = None

team_holder = [
    [pygame.rect.Rect(160, 608, 192, 64), 1],
    [pygame.rect.Rect(928, 608, 192, 64), 2],
]

character_holder = [
    [pygame.rect.Rect(608, 480, 64, 64), "soldier"],
    [pygame.rect.Rect(736, 480, 64, 64), "mage"],
    [pygame.rect.Rect(480, 480, 64, 64), "alien"],
]

ready_holder = pygame.rect.Rect(480, 672, 320, 64)
color_holder = pygame.rect.Rect(576, 384, 128, 8)

###
team_1_holder = [
    pygame.rect.Rect(64, 64, 64, 64),
    pygame.rect.Rect(64, 192, 64, 64),
    pygame.rect.Rect(64, 320, 64, 64)
]

team_1_ready_holder = [
    pygame.rect.Rect(160, 96, 32, 32),
    pygame.rect.Rect(160, 224, 32, 32),
    pygame.rect.Rect(160, 352, 32, 32)
]

###
team_2_holder = [
    pygame.rect.Rect(1152, 64, 64, 64),
    pygame.rect.Rect(1152, 192, 64, 64),
    pygame.rect.Rect(1152, 320, 64, 64)
]

team_2_ready_holder = [
    pygame.rect.Rect(1088, 96, 32, 32),
    pygame.rect.Rect(1088, 224, 32, 32),
    pygame.rect.Rect(1088, 352, 32, 32)
]

client_id = client.get(["initialize"])

if client_id is None:
    print("Failed to receive initial id")
    sys.exit()

client_color = to_color(client_id)

screen = pygame.display.set_mode((1280, 800))
clock = pygame.time.Clock()
in_lobby = True

#-----------------------------------------------------------------------------------------------------------------------
# LOBBY
while in_lobby:

    team_1 = client.get(["team 1"])
    team_2 = client.get(["team 2"])

    characters = client.get(["all player character"])

    ready = client.get(["ready status"])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if client_id in ready:
                    if not ready[client_id]:
                        for spawning_zone in team_holder:
                            if spawning_zone[0].collidepoint(pygame.mouse.get_pos()):
                                team_choice = spawning_zone[1]
                                client.send(["team choice", team_choice])
                        for character in character_holder:
                            if character[0].collidepoint(pygame.mouse.get_pos()):
                                character_choice = character[1]
                                client.send(["character choice", character_choice])
                        if ready_holder.collidepoint(pygame.mouse.get_pos()):
                            if character_choice is not None and team_choice is not None:
                                client.send(["ready"])

    start = client.get(["game start"])
    if start:
        in_lobby = False
    clock.tick(30)

    screen.blit(lobby, (0, 0))

    if character_choice is not None:
        image = get_character_image(character_choice)
        new_width = image.get_width() * 4
        new_height = image.get_height() * 4
        new_size = (new_width, new_height)
        scaled_image = pygame.transform.scale(image, new_size)
        screen.blit(scaled_image, (color_holder.x, color_holder.y - 128))

    pygame.draw.rect(screen, client_color, color_holder)

    count = 0
    for player in team_1:
        color = to_color(player)
        pygame.draw.rect(screen, color, team_1_holder[count], 5)

        if player in characters:
            character = characters[player]
            image = get_character_image(character)
            new_width = image.get_width() * 2
            new_height = image.get_height() * 2
            new_size = (new_width, new_height)
            scaled_image = pygame.transform.scale(image, new_size)
            screen.blit(scaled_image, (team_1_holder[count].x, team_1_holder[count].y))

        if player in ready:
            if ready[player]:
                pygame.draw.rect(screen, "green", team_1_ready_holder[count])
        count += 1

    count = 0
    for player in team_2:
        color = to_color(player)
        pygame.draw.rect(screen, color, team_2_holder[count], 5)

        if player in characters:
            character = characters[player]
            image = get_character_image(character)
            new_width = image.get_width() * 2
            new_height = image.get_height() * 2
            new_size = (new_width, new_height)
            scaled_image = pygame.transform.scale(image, new_size)
            screen.blit(scaled_image, (team_2_holder[count].x, team_2_holder[count].y))

        if player in ready:
            if ready[player]:
                pygame.draw.rect(screen, "green", team_2_ready_holder[count])
        count += 1

    for holder in team_holder:
        if holder[1] == team_choice:
            pygame.draw.rect(screen, "green", holder[0], 2)
        else:
            pygame.draw.rect(screen, "blue", holder[0], 2)

    for holder in character_holder:
        if holder[1] == character_choice:
            pygame.draw.rect(screen, "green", holder[0], 2)
        else:
            pygame.draw.rect(screen, "blue", holder[0], 2)
        image = get_character_image(holder[1])
        new_width = image.get_width() * 2
        new_height = image.get_height() * 2
        new_size = (new_width, new_height)
        scaled_image = pygame.transform.scale(image, new_size)
        screen.blit(scaled_image, (holder[0].x, holder[0].y))

    pygame.display.flip()

#-----------------------------------------------------------------------------------------------------------------------
#PRE-GAME
del ready_holder
del color_holder
del team_1_holder
del team_1_ready_holder
del team_2_holder
del team_2_ready_holder

capture_zone = pygame.rect.Rect(512, 320, 255, 127)

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

spawn_zone = [
    pygame.rect.Rect(0, 0, 96, 96),
    pygame.rect.Rect(1184, 704, 96, 96),
]

if team_choice is None or character_choice is None:
    print("Couldn't create player object")
    pygame.quit()
    sys.exit()

match character_choice:
    case "mage":
        player_image = mage
        player = Mage(client_id, [spawn_zone[team_choice - 1].centerx, spawn_zone[team_choice - 1].centery])
    case "soldier":
        player_image = soldier
        player = Soldier(client_id, [spawn_zone[team_choice - 1].centerx, spawn_zone[team_choice - 1].centery])
    case "alien":
        player_image = alien
        player = Alien(client_id, [spawn_zone[team_choice - 1].centerx, spawn_zone[team_choice - 1].centery])
    case _:
        player_image = default_player
        player = Player(client_id, [spawn_zone[team_choice - 1].centerx, spawn_zone[team_choice - 1].centery])

team_1 = client.get(["team 1"])
team_2 = client.get(["team 2"])

primary = Bullet
secondary = SlowZone
damage_dealt = []
slow_applied = []


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
#Global Data
#Where the server data will come through

current_players = client.get(["all active player", player.id])
print(current_players)

player_characters = client.get(["all player character", player.id])
print(player_characters)

point = 0

winner = ""
in_winner_screen = True

dead_timer = 5
dead_counter = 0

win_condition = 100

show_grid = False

in_game = True
dt = 0

#-----------------------------------------------------------------------------------------------------------------------
#GAME

def get_damage_received(_packet):
    total_damage = 0
    for key, value in _packet.items():
        if key != "team 1" and key != "team 2":
            damage_received = value["dmg"]
            for instance in damage_received:
                if instance[0] == client_id:
                    total_damage += instance[1]
    return total_damage

def get_slow_received(_packet):
    total_slow = 1
    for key, value in _packet.items():
        if key != "team 1" and key != "team 2":
            slow_received = value["slow"]
            for instance in slow_received:
                if instance[0] == client_id:
                    total_slow *= instance[1]
    return total_slow



while in_game:

    packet = {
        "x": player.rect.x,
        "y": player.rect.y,
        "hp": get_hp_percent(),
        "proj": player.projectile,
        "dmg": damage_dealt,
        "slow": slow_applied
    }

    server_packet = client.get(["packet", packet])
    server_projectile = get_projectiles(server_packet)

    damage_dealt = []
    slow_applied = []

    speed_mod = get_slow_received(server_packet)
    dmg_received = get_damage_received(server_packet)

    player.take_damage(dmg_received)
    player.modify_speed(speed_mod)

    for proj in player.projectile:
        enemyTeam = getEnemyTeam()
        allyTeam = getAllyTeam()
        for enemy in enemyTeam:
            x = server_packet[enemy]["x"]
            y = server_packet[enemy]["y"]
            if proj.rect.collidepoint(x, y):
                if proj.type == "damage":
                    data = [enemy, proj.type_value]
                    damage_dealt.append(data)
                    player.projectile.remove(proj)
                elif proj.type == "slow":
                    data = [enemy, proj.type_value]
                    slow_applied.append(data)
        for ally in allyTeam:
            x = server_packet[ally]["x"]
            y = server_packet[ally]["y"]
            if proj.rect.collidepoint(x, y):
                if proj.type == "slow":
                    data = [ally, proj.type_value]
                    slow_applied.append(data)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            in_game = False
            in_winner_screen = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                use_primary()
            if event.button == 3:
                use_secondary()
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
                pygame.quit()
                sys.exit()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                player.left = 0
            if event.key == pygame.K_d:
                player.right = 0
            if event.key == pygame.K_s:
                player.down = 0
            if event.key == pygame.K_w:
                player.up = 0

    player.update(dt)

    handle_player(player)

    for proj in player.projectile:
        proj.update(dt)
        if proj.rect.collidelist(obstacles) != -1:
            if proj.type == "damage":
                player.projectile.remove(proj)
            if proj.type == "slow":
                if proj.speed != 0:
                    proj.speed = 0
                    proj.sizeUp()
                else:
                    if proj.kill:
                        player.projectile.remove(proj)
        elif proj.rect.x < 0 or proj.rect.x + proj.rect.width > 1280 or proj.rect.y < 0 or proj.rect.y + proj.rect.height > 800:
            player.projectile.remove(proj)

    map_system.handle_fog(map_system.getEntityNode(player), player.vision)
    # fill the screen with a color to wipe away anything from last frame
    screen.blit(game_map, (0, 0))

    #Drawing all players and their health bars
    #Note that the main player character will not be covered by fog

    for entity in current_players:
        if entity is not client_id:
            if entity in server_packet:
                for proj in server_packet[entity]["proj"]:
                    if proj.name_id == 2:
                        proj.draw_image(bullet)
                    elif proj.name_id == 3:
                        if proj.phase == 1:
                            proj.draw_image(slow_phase_1)
                        elif proj.phase == 2:
                            proj.draw_image(slow_phase_2)
                            proj.draw()
                    else:
                        if isEnemy(entity):
                            proj.set_color(True)
                        proj.draw()


    for proj in player.projectile:
        if proj.name_id == 2:
            proj.draw_image(bullet)
        elif proj.name_id == 3:
            if proj.phase == 1:
                proj.draw_image(slow_phase_1)
            elif proj.phase == 2:
                proj.draw_image(slow_phase_2)
                proj.draw()
        else:
            proj.draw()


    for entity in current_players:
        if entity is not client_id:
            if entity in player_characters and entity in server_packet:
                image = get_character_image(player_characters[entity])
                x = server_packet[entity]["x"]
                y = server_packet[entity]["y"]
                screen.blit(image, (x,y))
                border = pygame.rect.Rect(server_packet[entity]["x"], server_packet[entity]["y"] - 11, 34, 7)
                current_hp = server_packet[entity]["hp"] * 32
                current_hp_rect = pygame.rect.Rect(server_packet[entity]["x"], server_packet[entity]["y"] - 10, current_hp, 5)
                pygame.draw.rect(screen, to_color(entity), current_hp_rect)
                if isEnemy(entity):
                    pygame.draw.rect(screen, "red", current_hp_rect)
                else:
                    pygame.draw.rect(screen, "green", current_hp_rect)

    screen.blit(player_image, (player.rect.x, player.rect.y))
    border = pygame.rect.Rect(player.rect.x, player.rect.y - 11, 34, 7)
    current_hp = get_hp_percent() * 32
    current_hp_rect = pygame.rect.Rect(player.rect.x, player.rect.y - 10, current_hp, 5)
    pygame.draw.rect(screen, to_color(client_color), current_hp_rect)
    pygame.draw.rect(screen, "green", current_hp_rect)
    #Drawing fog of war
    map_system.draw()

    #Test Drawing
    if show_grid:
        for i in map_system.nodes:
            for _node in i:
                pygame.draw.rect(screen, "red", _node.rect, 1)
    for _ in obstacles:
        pygame.draw.rect(screen, "black", _, 2)



    # flip() the display to put your work on screen
    pygame.display.flip()

    dt = clock.tick(30) / 1000

while in_winner_screen:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            in_winner_screen = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                in_winner_screen = False

    screen.blit(game_map, (0, 0))
    pygame.display.flip()

pygame.quit()
