import pygame

pos=[]

# Width screen. Pixels
screenWidth = 800
# Height screen
screenHeight = 600
#
squareSize = 50
# Original upscaled (Frames per second)
fps = 30

enemyList = []
bulletList = []
iconList = []
senderList = []
startList= []
hailList = []
explosionList = []
EnemyImageArray = dict()

colors = { # R,G,B
    'yellow':   (255,255,0),
    'lime':     (0,255,0),
    'darkblue': (0,0,255),
    'aqua':     (0,255,255),
    'magenta':  (255,0,255),
    'purple':   (128,0,128),
    'green':    (97,144,0),
    'purple':   (197,125,190),
    'brown':    (110,73,32),}

# Optional music
def play_music(file, volume=0.65, loop=-1):
    pygame.mixer.music.load(file)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(loop)

def play_sound(file, volume=0.5):
    sound = pygame.mixer.Sound(file)
    sound.set_volume(volume)
    sound.play()

def stop_music(): pygame.mixer.music.stop()

def imgLoad(file,size=None):
    image = pygame.image.load(file).convert_alpha()
    return pygame.transform.scale(image,size) if size else image


def loadImages():
    bloon = imgLoad('enemies/bloonImg.png')
    EnemyImageArray['red'] = bloon
    width,height = bloon.get_size()
    for name in colors:
        image = bloon.copy()
        for x in range(width): 
            for y in range(height):
                p = image.get_at((x,y))[:-1]
                if p not in ((0,0,0),(255,255,255)):
                    c = colors[name]
                    r,g,b = p[0]*c[0]/255, p[0]*c[1]/255, p[0]*c[2]/255
                    image.set_at((x,y),(min(int(r),255),min(int(g),255),min(int(b),255)))
        EnemyImageArray[name] = image

