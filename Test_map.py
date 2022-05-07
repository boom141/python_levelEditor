import pygame, sys, os, time
from MapLoader import*
from Animation import*
from pygame.locals import*


pygame.init()
Fps = pygame.time.Clock()
Height = 200
Width = 300
Screen = pygame.display.set_mode((1000,500))
Display = pygame.Surface((Width,Height))

spawn_point = [700,180]
true_camera = [0,0]

player_dimension = pygame.Rect(150,100, 10,10)

left = False
right = False

velocity = 3
y_momentum = 0
air_timer = 0

last_time = time.time()

load_map = Load_Map()
entity,generated_map,entity_layer,generated_layer,decoration, decoration_num = load_map.Load_File('MapCoordinate.txt',
        'MapSequence.txt', 'layerCoordinate.txt', 'layerSequence.txt','decoration.txt','decorationNum.txt', 36)

vfx = VFX()

def Filter(entity,loc,deco_id):
    attribute = []
    for obj in loc:
        if entity[loc.index(obj)] == deco_id:
            attribute.append(obj)
    return attribute

def Render_Vfx(dt):
    tree_loc = Filter(decoration_num,decoration,0)
    sprites = VFX().Load_Sprite('vfx', 'tree', 9)
    frame = vfx.Animate1(0.2,dt,9)
    for tree in tree_loc:
        image = sprites[int(frame)]
        image.set_colorkey((0,0,0))
        Display.blit(image, (tree.x - spawn_point[0],tree.y - spawn_point[1]))

    bush_loc = Filter(decoration_num,decoration,1)
    sprites = VFX().Load_Sprite('vfx', 'bush', 7)
    frame = vfx.Animate2(0.2,dt,7)
    for bush in bush_loc:
        image = sprites[int(frame)]
        image.set_colorkey((0,0,0))
        Display.blit(image, (bush.x - spawn_point[0],bush.y - spawn_point[1]))

def Render_Map(camera,dt):
    tiles = []
    if decoration:
        for tile in decoration:
            image = pygame.image.load(os.path.join('set2', f'deco{decoration_num[decoration.index(tile)]}.png'))
            image.set_colorkey((0,0,0))
            tile.x -= camera[0]
            tile.y -= camera[1]
            Display.blit(image,(tile.x - spawn_point[0],tile.y - spawn_point[1]))
    
    Render_Vfx(dt)

    if entity:
        for tile in entity:
            image = pygame.image.load(os.path.join('set1', f'tile{generated_map[entity.index(tile)]}.png'))
            image = pygame.transform.scale(image, (36,36))
            image.set_colorkey((0,0,0))
            tile.x -= camera[0]
            tile.y -= camera[1]
            tiles.append(Display.blit(image,(tile.x - spawn_point[0],tile.y - spawn_point[1])))
    
    return tiles

def Collision(player_dimension,tiles):
    collision = []
    for tile in tiles:
        if player_dimension.colliderect(tile):
            collision.append(tile)

    return collision

def Player_Movements(player_dimension,movement,tiles):
    collision_type = {'top':False, 'left':False, 'right':False, 'down':False}
    player_dimension.x += movement[0]
    collision = Collision(player_dimension,tiles)
    for tile in collision:
        if movement[0] > 0:
            player_dimension.right = tile.left
            collision_type['right'] = True
        elif movement[0] < 0:
            player_dimension.left = tile.right
            collision_type['left'] = True

    player_dimension.y += movement[1]
    collision = Collision(player_dimension,tiles)
    for tile in collision:
        if movement[1] > 0:
            player_dimension.bottom = tile.top
            collision_type['down'] = True
        elif movement[1] < 0:
            player_dimension.top = tile.bottom
            collision_type['up'] = True
    
    return player_dimension, collision_type

def Render_Player(player,camera,dt):
    player.x -= camera[0]
    player.y -= camera[1]
    pygame.draw.rect(Display, 'blue', player)

while 1:
    Display.fill('black')
    dt = time.time() - last_time 
    dt *= 60
    last_time = time.time()

    true_camera[0] += (player_dimension.x - true_camera[0] - 152)/2
    true_camera[1] += (player_dimension.y - true_camera[1] - 106)/2
    
    camera = true_camera.copy()
    camera[0] = int(camera[0])
    camera[1] = int(camera[1])

    tiles = Render_Map(camera, dt)  
    movement = [0,0]
    if right:
        movement[0] += velocity
    if left:
        movement[0] -= velocity
    
    movement[1] += y_momentum
    y_momentum += 0.2
    if y_momentum > 3:
       y_momentum = 3
   
    player_dimension, collision_types = Player_Movements(player_dimension,movement,tiles)    

    if collision_types['down'] == True:
       air_timer = 0
       y_momentum = 0
    else:
       air_timer += 1
    
    Render_Player(player_dimension,camera,dt)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                left = True
            if event.key == pygame.K_d:
                right = True
            if event.key == pygame.K_SPACE:
                if air_timer < 6:
                    y_momentum = -5
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                left = False
            if event.key == pygame.K_d:
                right = False

    surf = pygame.transform.scale(Display,(1000,600))
    Screen.blit(surf, (0, 0))
    pygame.display.update()
    Fps.tick(60)
