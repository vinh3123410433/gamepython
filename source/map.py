from setting import *

class Map:
    def __init__(self):
        self.map = 'monkey lane'
        self.loadmap()

    def loadmap(self):
        self.targets = eval(open('maps/%s/targets.txt' % self.map,'r').read())
        self.waves = eval(open('maps/%s/waves.txt' % self.map,'r').read())

    def getmovelist(self):
        self.pathpoints = []
        for i in range(len(self.targets)-1):
            a,b = self.targets[i:i+2]
            self.pathpoints+=[0]

    def get_background(self):
        background = imgLoad('maps/%s/image.png' % self.map)
        background2 = imgLoad('maps/%s/image2.png' % self.map).convert_alpha()
        background3 = imgLoad('maps/%s/image3.png' % self.map).convert_alpha()
        return background,background2,background3