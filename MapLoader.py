import pygame

class Load_Map:
    def __init__(self):
        self.temp1 = []
        self.temp2 = []
        self.temp3 = []
        self.temp4 = []
        self.temp5 = [] 
        self.temp6 = []

    def Load_File(self, platform, seq_platform, layer, seq_layer, decoration, decoration_num, size):
        try:
            file1 = open(platform, 'r', encoding='utf-8')
            for str in file1:
                coord = str.split(',')
                self.temp1.append(pygame.Rect(int(coord[0]), int(coord[1]),size,size))
            file2 = open(seq_platform, 'r', encoding='utf-8') 
            for str in file2:
                self.temp2.append(int(str))
            file3 = open(layer, 'r', encoding='utf-8')
            for str in file3:
                coord = str.split(',')
                self.temp3.append(pygame.Rect(int(coord[0]), int(coord[1]),size,size))
            file4 = open(seq_layer, 'r', encoding='utf-8') 
            for str in file4:
                self.temp4.append(int(str))
            file5 = open(decoration, 'r', encoding='utf-8')
            for str in file5:
                coord = str.split(',')
                self.temp5.append(pygame.Rect(int(coord[0]), int(coord[1]),size,size))
            file6 = open(decoration_num, 'r', encoding='utf-8') 
            for str in file6:
                self.temp6.append(int(str))
        finally:
            file1.close()
            file2.close()
            file3.close()
            file4.close()
            file5.close()
            file6.close()

        return self.temp1,self.temp2,self.temp3,self.temp4,self.temp5,self.temp6
