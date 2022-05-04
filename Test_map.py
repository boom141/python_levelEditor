from flask import Blueprint
import pygame, sys, os
from MapLoader import*
from pygame.locals import*


pygame.init()
Fps = pygame.time.Clock()
Height = 200
Width = 300
Screen = pygame.display.set_mode((1000,500))
Display = pygame.Surface((Width,Height))

decorations = []
backgrounds = []
tiles = []
spawn_point = [700,180]

player_dimension = pygame.Rect(150,100,16,16)

place = False
is_moving = False
left = False
right = False
up = False
jump = False
gravity = True

jump_force = 20
speed = 3
camera_speed = 6
frame_tree = 0

load_map = Load_Map()
entity,generated_map,entity_layer,generated_layer,decoration, decoration_num = load_map.Load_File('MapCoordinate.txt',
        'MapSequence.txt', 'layerCoordinate.txt', 'layerSequence.txt','decoration.txt','decorationNum.txt', 36)

class VFX:
    def __init__(self):
        pass

    def filter(self,entity,loc,deco_id):
        coord = []
        for obj in loc:
            if entity[loc.index(obj)] == deco_id:
                coord.append(obj)
        return coord

def Render_Vfx(camera,frame):
   coord = VFX().filter(decoration_num,decoration,0)
   for obj in coord:
        image = pygame.image.load(os.path.join('vfx', f'tree{int(frame)}.png'))
        image.set_colorkey((0,0,0))
        Display.blit(image, (obj.x - spawn_point[0],obj.y - spawn_point[1]))

def Render_Map(camera,frame):
    if decoration:
        for tile in decoration:
            image = pygame.image.load(os.path.join('set2', f'deco{decoration_num[decoration.index(tile)]}.png'))
            image.set_colorkey((0,0,0))
            tile.x += camera[0]
            tile.y += camera[1]
            decorations.append(Display.blit(image,(tile.x - spawn_point[0],tile.y - spawn_point[1])))
    
    Render_Vfx(camera,frame)

    if entity:
        for tile in entity:
            image = pygame.image.load(os.path.join('set1', f'tile{generated_map[entity.index(tile)]}.png'))
            image = pygame.transform.scale(image, (36,36))
            image.set_colorkey((0,0,0))
            tile.x += camera[0]
            tile.y += camera[1]
            tiles.append(Display.blit(image,(tile.x - spawn_point[0],tile.y - spawn_point[1])))

    if entity_layer:
        for tile in entity_layer:
            image = pygame.image.load(os.path.join('set1', f'tile{generated_layer[entity_layer.index(tile)]}.png'))
            image = pygame.transform.scale(image, (36,36))
            image.set_colorkey((0,0,0))
            tile.x += camera[0]
            tile.y += camera[1]
            backgrounds.append(Display.blit(image,(tile.x - spawn_point[0],tile.y - spawn_point[1])))

def Collision(player_dimension):
    collision = []
    for tile in tiles:
        if player_dimension.colliderect(tile):
            collision.append(tile)
    return collision

def Player_Movements(player_dimension,movement):
    global jump,jump_force
    player_dimension.x += movement[0]
    collision = Collision(player_dimension)
    for tile in collision:
        if movement[0] > 0:
            player_dimension.right = tile.left
        if movement[0] < 0:
            player_dimension.left = tile.right

            
    player_dimension.y += movement[1]
    collision = Collision(player_dimension)
    for tile in collision:
        if movement[1] > 0:
            player_dimension.bottom = tile.top
            jump = False
            jump_force = 20
        if movement[1] < 0:
            player_dimension.top = tile.bottom

    return player_dimension

def Render_Player(player):
    # pygame.draw.rect(Display, 'blue', player)
    pass

while 1:
    Display.fill('black')

    movement = [0,0]
    camera = [0,0]
    if left:
        movement[0] -= speed
        camera[0] += camera_speed
    if right:
        movement[0] += speed
        camera[0] -= camera_speed
    if up:
        camera[1] += camera_speed

    # if jump:
    #     movement[1] -= jump_force
    #     jump_force -= 3
    # if gravity: 
    #     movement[1] += speed
        
    if frame_tree > 8:
        frame_tree = 0
    frame_tree += 0.2
    Render_Map(camera,frame_tree)
    player = Player_Movements(player_dimension,movement)
    Render_Player(player)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit
            sys.exit()


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                up = True
            if event.key == pygame.K_a:
                left = True
            if event.key == pygame.K_d:
                right = True
            if event.key == pygame.K_SPACE:
                jump = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                up = False
            if event.key == pygame.K_a:
                left = False
            if event.key == pygame.K_d:
                right = False

    surf = pygame.transform.scale(Display,(1000,600))
    Screen.blit(surf, (0, 0))
    pygame.display.update()
    Fps.tick(60)
