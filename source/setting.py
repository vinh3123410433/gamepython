import pygame
import json
import os

pos=[]

# Width screen. Pixels
screenWidth = 800
# Height screen
screenHeight = 600
#
squareSize = 50
# Original upscaled (Frames per second)
fps = 30

class SoundManager:
    def __init__(self):
        self.music_enabled = True
        self.music_volume = 0.65
        self.sound_volume = 0.5
        self.load_settings()

    def load_settings(self):
        try:
            with open('settings.json', 'r') as f:
                settings = json.load(f)
                self.music_enabled = settings.get('music_enabled', True)
                self.music_volume = settings.get('music_volume', 0.65)
                self.sound_volume = settings.get('sound_volume', 0.5)
        except:
            self.save_settings()

    def save_settings(self):
        settings = {
            'music_enabled': self.music_enabled,
            'music_volume': self.music_volume,
            'sound_volume': self.sound_volume
        }
        with open('settings.json', 'w') as f:
            json.dump(settings, f)

    def toggle_music(self):
        self.music_enabled = not self.music_enabled
        if self.music_enabled:
            self.play_music('music/maintheme.mp3')
        else:
            self.stop_music()
        self.save_settings()

    def play_music(self, file, volume=None, loop=-1):
        if not self.music_enabled:
            return
        pygame.mixer.music.load(file)
        pygame.mixer.music.set_volume(volume if volume is not None else self.music_volume)
        pygame.mixer.music.play(loop)

    def play_sound(self, file, volume=None):
        if not self.music_enabled:
            return
        sound = pygame.mixer.Sound(file)
        sound.set_volume(volume if volume is not None else self.sound_volume)
        sound.play()

    def stop_music(self):
        pygame.mixer.music.stop()

# Tạo instance của SoundManager
sound_manager = SoundManager()

# Các hàm wrapper để tương thích với code cũ
def play_music(file, volume=None, loop=-1):
    sound_manager.play_music(file, volume, loop)

def play_sound(file, volume=None):
    sound_manager.play_sound(file, volume)

def stop_music():
    sound_manager.stop_music()

def toggle_music():
    sound_manager.toggle_music()

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

