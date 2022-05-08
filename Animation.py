import pygame,os

class VFX:
    def __init__(self):
      self.Sprites = []
      self.frame1 = 0
      self.frame2 = 0
    
    def Load_Sprite(self, folder_n,file_n,length):
        for i in range(length):
            self.Sprites.append(pygame.image.load(os.path.join(folder_n, f'{file_n}{i}.png')))
        return self.Sprites
    
    def Animate1(self,speed,dt,length):
        self.frame1 += speed
        if self.frame1 >= length:
            self.frame1 = 0
        return self.frame1
    
    def Animate2(self,speed,dt,length):
        self.frame2 += speed
        if self.frame2 >= length:
            self.frame2 = 0
        return self.frame2

class Player_Animation:
    def __init__(self):
        self.Sprites = []
        self.frame = 0
    def Load_Sprites(self,folder_n,file_n,length):
        for i in range(length):
            self.Sprites.append(pygame.image.load(os.path.join(folder_n, f'{file_n}{i}.png')))
        return self.Sprites
    
    def Animate(self, speed, length):
        self.frame += speed
        if self.frame >= length:
            self.frame = 0
        return self.frame