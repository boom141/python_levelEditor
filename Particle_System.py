import pygame, sys, random

pygame.init()

Window = pygame.display.set_mode((400,300))
Fps = pygame.time.Clock()

class Particle_system:
    def __init__(self):
        pass
    def Disperse(self):
        return [[200, 150], [random.randrange(-3,3),random.randrange(-10,10)], random.randint(4, 6)]

particles = []
while 1:
    Window.fill('black')
   
    for particle in particles:
        particle[0][0] += particle[1][0]
        particle[0][1] += particle[1][1]
        particle[2] -= 0.1
        particle[1][1] += 0.1
        pygame.draw.circle(Window, (255, 255, 255), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
        if particle[2] <= 0:
            particles.remove(particle)
  

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_t:
                for i in range(20):
                    particles.append(Particle_system().Disperse())
                    

    pygame.display.update()
    Fps.tick(60)
