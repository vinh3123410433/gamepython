from setting import *

class Map:
    def __init__(self):
        self.map = 'monkey lane'
        self.loadmap()

    def loadmap(self):
        raw_targets = eval(open('maps/%s/targets.txt' % self.map,'r').read())
        sx = screenWidth / 700.0
        sy = screenHeight / 510.0
        self.targets = [(round(x * sx), round(y * sy)) for (x, y) in raw_targets]
        self.waves = eval(open('maps/%s/waves.txt' % self.map,'r').read())

    def getmovelist(self):
        self.pathpoints = []
        for i in range(len(self.targets)-1):
            a,b = self.targets[i:i+2]
            self.pathpoints+=[0]

    def get_background(self):
        background = imgLoad('maps/%s/image.png' % self.map, (screenWidth, screenHeight))
        background2 = imgLoad('maps/%s/image2.png' % self.map, (screenWidth, screenHeight)).convert_alpha()
        background3 = imgLoad('maps/%s/image3.png' % self.map, (screenWidth, screenHeight)).convert_alpha()
        return background,background2,background3