import pygame, sys, os
from MapLoader import*
from pygame.locals import*


pygame.init()
Fps = pygame.time.Clock()
Height = 500
Width = 1000
Screen = pygame.display.set_mode((Width,Height))
Display = pygame.Surface((Width,Height))

render_tile_x = []
render_tile_y = []

place = False
is_moving = False
paint = True
layer = False
erase = False
decor = False
select = False

current_seq = -1
set_number = 'set1'
file_name = 'tile'
current_tool = 'PAINT'

class Import_Sprite:
    def __init__(self):
        self.set_img = []

    def Initialize_platform(self, count, size):
        for x in range(0, count, size):
             x *= 2
             self.set_img.append(pygame.Rect(x + 10, 450,32,32))
        
        return self.set_img

def Render_TileSet(set_number, file_name, tile_Set, size):
    arr= []
    index = -1
    for tile in tile_Set:
        index += 1 
        set_img = pygame.image.load(os.path.join(f'{set_number}', f'{file_name}{index}.png'))
        set_img.set_colorkey((0, 0, 0))
        pygame.draw.rect(Display, 'black', (tile.x,tile.y,32,32))
        arr.append(Display.blit(pygame.transform.scale(set_img,(size,size)),(tile.x,tile.y)))
    if current_seq != -1:
        pygame.draw.rect(Display, 'green', tile_Set[current_seq], 1)
    return arr

def Render_Sprites():
        if decoration:
            for tile in decoration:
                image = pygame.image.load(os.path.join('set2', f'deco{decoration_num[decoration.index(tile)]}.png'))
                image.set_colorkey((0,0,0))
                Display.blit(image,(tile.x,tile.y))
        
        if entity:
            for tile in entity:
                image = pygame.image.load(os.path.join('set1', f'tile{generated_map[entity.index(tile)]}.png'))
                image = pygame.transform.scale(image, (36,36))
                image.set_colorkey((0,0,0))
                Display.blit(image,(tile.x,tile.y))

        if entity_layer:
            for tile in entity_layer:
                image = pygame.image.load(os.path.join('set1', f'tile{generated_layer[entity_layer.index(tile)]}.png'))
                image = pygame.transform.scale(image, (36,36))
                image.set_colorkey((0,0,0))
                Display.blit(image,(tile.x,tile.y))

def Check_Duplicate_Paint(object):
    if object in entity:
        return True
    else:
        return False
def Check_Duplicate_Layer(object):
    if object in entity_layer:
        return True
    else:
        return False
def Check_Duplicate_Decoration(object):
    if object in decoration:
        return True
    else:
        return False

def Generate_Coordinate(mouse_inputs,is_moving,grid_list,x,y,set_number):
    if (mouse_inputs[0] and is_moving):
            for grid in grid_list:
                if grid.collidepoint(pygame.mouse.get_pos()):
                    if current_seq != -1:     
                        if (paint and erase == False):
                            verify = Check_Duplicate_Paint(grid)
                            if verify == False:
                                entity.append(grid)
                                generated_map.append(current_seq)
                        if (layer and erase == False):
                            verify = Check_Duplicate_Layer(grid)
                            if verify == False:    
                                entity_layer.append(grid)
                                generated_layer.append(current_seq)
    if (decor and erase == False and set_number == 'set2'):
        if mouse_inputs[0]:
            for grid in grid_list:
                if grid.collidepoint(pygame.mouse.get_pos()):
                    image = pygame.image.load(os.path.join('set2', f'deco{current_seq}.png'))
                    rect = pygame.Rect(x - int(image.get_width()/2),y-int(image.get_height()/2), 0,0)
                    verify = Check_Duplicate_Decoration(rect)
                    if verify == False:
                        decoration.append(rect)
                        decoration_num.append(current_seq)

def Erase(mouse_inputs,is_moving):
    if erase:
        if (mouse_inputs[0] and is_moving):
            if paint:
                for obj in entity:
                    if obj.collidepoint(pygame.mouse.get_pos()):
                        generated_map.remove(generated_map[entity.index(obj)])
                        entity.remove(obj)  
            if layer:                                   
                for obj in entity_layer:
                    if obj.collidepoint(pygame.mouse.get_pos()):
                        generated_layer.remove(generated_layer[entity_layer.index(obj)])
                        entity_layer.remove(obj) 
            if decor:
                for obj in decoration:
                    if obj.collidepoint(pygame.mouse.get_pos()):
                        print('hovering')
                        decoration_num.remove(decoration_num[decoration.index(obj)])
                        decoration.remove(obj)

def Save_Map():
    try:
        map_coord = open('MapCoordinate.txt', 'w', encoding='utf-8')
        for obj in entity:
            map_coord.write(f'{obj.x}, {obj.y}\n')
        map_seq = open('MapSequence.txt', 'w', encoding='utf-8')
        for seq in generated_map:
            map_seq.write(f'{seq}\n')
        layer_coord = open('layerCoordinate.txt', 'w', encoding='utf-8')
        for obj in entity_layer:
            layer_coord.write(f'{obj.x}, {obj.y}\n')
        layer_seq = open('layerSequence.txt', 'w', encoding='utf-8')
        for seq in generated_layer:
            layer_seq.write(f'{seq}\n')
        decor_coord = open('decoration.txt', 'w', encoding='utf-8')
        for obj in decoration:
            decor_coord.write(f'{obj.x}, {obj.y}\n')
        decor_seq = open('decorationNum.txt', 'w', encoding='utf-8')
        for seq in decoration_num:
            decor_seq.write(f'{seq}\n')
    finally:
        map_coord.close()
        map_seq.close()
        layer_coord.close()
        layer_seq.close()
        decor_coord.close()
        decor_seq.close()

def Display_Tool(current_tool,Display):
    Font = pygame.font.Font(os.path.join('font', 'ChalkFont.ttf'),30)
    Text = Font.render(current_tool,False,'white')
    pygame.draw.rect(Display, 'black', (800,450,150,30))
    Display.blit(Text,(800, 450))

def Hover(x,y,grid,set_number):
    if set_number == 'set2' and erase == False:
        for grd in grid:
            if grd.collidepoint(pygame.mouse.get_pos()) and current_seq != -1:
                image = pygame.image.load(os.path.join('set2', f'deco{current_seq}.png'))
                image.set_colorkey((0,0,0))
                Display.blit(image,(x - int(image.get_width()/2),y-int(image.get_height()/2)))

def Grid(Display, grid_size):
    grid_list = []
    for x in range(0,Width,grid_size):
        for y in range(0,400,grid_size):
            rect = pygame.Rect(x, y, grid_size, grid_size)
            grid_list.append(pygame.draw.rect(Display, (0,0,0), rect, 1))
    pygame.draw.line(Display, (255,255,255), (0,420), (Width,420), width=1)
    return grid_list

grid = Grid(Display,32)
sprite = Import_Sprite()
load_map = Load_Map()

entity,generated_map,entity_layer,generated_layer,decoration, decoration_num = load_map.Load_File('MapCoordinate.txt',
        'MapSequence.txt', 'layerCoordinate.txt', 'layerSequence.txt','decoration.txt','decorationNum.txt', 36)

tile_set = sprite.Initialize_platform(280,32)

while 1:
    Display.fill('black')
    x,y = pygame.mouse.get_pos()
    mouse_inputs = pygame.mouse.get_pressed()

    sprite_selection = Render_TileSet(set_number,file_name,tile_set,32)
    Generate_Coordinate(mouse_inputs,is_moving,grid,x,y,set_number)    
    Erase(mouse_inputs,is_moving)
    Render_Sprites()
    Hover(x,y,grid,set_number)
    Display_Tool(current_tool,Display)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            is_moving = True
        else:
            is_moving = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            loop = 1
            for sprite in sprite_selection:
                if sprite.collidepoint(pygame.mouse.get_pos()):
                    current_seq = sprite_selection.index(sprite)
    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                    current_tool = 'PAINT'
                    paint = True
                    layer = False
                    erase = False
                    decor = False
            if event.key == pygame.K_l:
                    current_tool = 'LAYER'
                    layer = True
                    paint = False
                    erase = False
                    decor = False
            if event.key == pygame.K_d:
                    current_tool = 'DECOR'
                    decor = True
                    layer = False
                    paint = False
                    erase = False
            if event.key == pygame.K_e:
                    current_tool = 'ERASE'
                    erase = True
            if event.key == pygame.K_s:
                    Save_Map()
            if event.key == pygame.K_1:
                set_number = 'set1'
                file_name = 'tile'
            if event.key == pygame.K_2:
                set_number = 'set2'
                file_name = 'deco'

    Screen.blit(Display,(0, 0))
    pygame.display.update()
    Fps.tick(60)