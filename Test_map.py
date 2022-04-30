import pygame, sys, os
from MapLoader import*
from pygame.locals import*


pygame.init()
Fps = pygame.time.Clock()
Height = 200
Width = 300
Screen = pygame.display.set_mode((1000,500))
Display = pygame.Surface((Width,Height))
image = pygame.image.load(os.path.join('set1', 'tile1.png'))
image = pygame.transform.scale(image, (36,36))

render_tile_x = []
render_tile_y = []
tiles = []

canvas_coord = [0,0]

place = False
is_moving = False
left = False
right = False
up = False
down = False 

offset = 0
speed = 5

load_map = Load_Map()
entity,generated_map,entity_layer,generated_layer,decoration, decoration_num = load_map.Load_File('MapCoordinate.txt',
        'MapSequence.txt', 'layerCoordinate.txt', 'layerSequence.txt','decoration.txt','decorationNum.txt', 36)

def Render_Map(movement):
        if decoration:
            for tile in decoration:
                image = pygame.image.load(os.path.join('set2', f'deco{decoration_num[decoration.index(tile)]}.png'))
                image.set_colorkey((0,0,0))
                tile.x += movement[0]
                tile.y += movement[1]
                Display.blit(image,(tile.x,tile.y))
        
        if entity:
            for tile in entity:
                image = pygame.image.load(os.path.join('set1', f'tile{generated_map[entity.index(tile)]}.png'))
                image = pygame.transform.scale(image, (36,36))
                image.set_colorkey((0,0,0))
                tile.x += movement[0]
                tile.y += movement[1]
                Display.blit(image,(tile.x,tile.y))

        if entity_layer:
            for tile in entity_layer:
                image = pygame.image.load(os.path.join('set1', f'tile{generated_layer[entity_layer.index(tile)]}.png'))
                image = pygame.transform.scale(image, (36,36))
                image.set_colorkey((0,0,0))
                tile.x += movement[0]
                tile.y += movement[1]
                Display.blit(image,(tile.x,tile.y))
while 1:
    Screen.fill('grey')
    Display.fill('black')
    x,y = pygame.mouse.get_pos()
    mouse_inputs = pygame.mouse.get_pressed()

    movement = [0,0]
    if left:
        movement[0] -= speed
    if right:
        movement[0] += speed
    if up:
        movement[1] -= speed
    if down: 
        movement[1] += speed

    Render_Map(movement)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            is_moving = True
        else:
            is_moving = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                left = True
            if event.key == pygame.K_RIGHT:
                right = True
            if event.key == pygame.K_UP:
                up = True
            if event.key == pygame.K_DOWN:
                down = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                left = False
            if event.key == pygame.K_RIGHT:
                right = False
            if event.key == pygame.K_UP:
                up = False
            if event.key == pygame.K_DOWN:
                down = False

    surf = pygame.transform.scale(Display,(1000,600))
    Screen.blit(surf, (canvas_coord[0], canvas_coord[1]))
    pygame.display.update()
    Fps.tick(60)