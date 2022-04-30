import pygame, sys

pygame.init()
Fps = pygame.time.Clock()

Screen = pygame.display.set_mode((600,400))
Display = pygame.Surface((300,200))

camera_coord = [0,-200]

left = False
right = False
down = False
jump = False

speed = 5
jump_force = 15

def Camera(movement):
   camera_coord[0] += movement[0]
   camera_coord[1] += movement[1]
   surf = pygame.transform.scale(Display, (800,600))
   Screen.blit(surf, (camera_coord[0], camera_coord[1]))

while 1:
 Screen.fill('white')
 Display.fill('blue')
 
 movement = [0,0]
  
 if left:
    movement[0] -= speed

 if right:
    movement[0] += speed
    look_right = True
 if jump:
    on_ground = False
    movement[1] -= jump_force
    jump_force -= 1
    if jump_force == -15:
        jump = False
        jump_force = 15 

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
            jump = True

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_a:
            left = False       
        if event.key == pygame.K_d:
            right = False

 Camera(movement)
 pygame.display.update()
 Fps.tick(60)