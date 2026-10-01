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
        self.sound_enabled = True
        self.music_volume = 0.65
        self.sound_volume = 0.5
        self._sound_cache = {}
        self.load_settings()

    def load_settings(self):
        try:
            with open('settings.json', 'r') as f:
                settings = json.load(f)
                self.music_enabled = settings.get('music_enabled', True)
                self.sound_enabled = settings.get('sound_enabled', True)
                self.music_volume = settings.get('music_volume', 0.65)
                self.sound_volume = settings.get('sound_volume', 0.5)
        except:
            self.save_settings()

    def save_settings(self):
        settings = {
            'music_enabled': self.music_enabled,
            'sound_enabled': self.sound_enabled,
            'music_volume': self.music_volume,
            'sound_volume': self.sound_volume
        }
        with open('settings.json', 'w') as f:
            json.dump(settings, f, indent=4)

    def set_music_volume(self, volume):
        self.music_volume = max(0.0, min(1.0, volume))
        if pygame.mixer.get_init():
            try:
                pygame.mixer.music.set_volume(self.music_volume)
            except Exception:
                pass
        self.save_settings()

    def set_sound_volume(self, volume):
        self.sound_volume = max(0.0, min(1.0, volume))
        for sound in self._sound_cache.values():
            try:
                sound.set_volume(self.sound_volume)
            except Exception:
                pass
        self.save_settings()

    def set_music_enabled(self, enabled):
        self.music_enabled = enabled
        if not self.music_enabled:
            self.stop_music()
        else:
            self.play_music('music/maintheme.mp3')
        self.save_settings()

    def set_sound_enabled(self, enabled):
        self.sound_enabled = enabled
        self.save_settings()

    def toggle_music(self):
        self.set_music_enabled(not self.music_enabled)

    def play_music(self, file, volume=None, loop=-1):
        if not self.music_enabled or not pygame.mixer.get_init():
            return
        try:
            pygame.mixer.music.load(file)
            vol = volume if volume is not None else self.music_volume
            pygame.mixer.music.set_volume(vol)
            pygame.mixer.music.play(loop)
        except Exception as e:
            print(f"Không thể phát nhạc: {e}")

    def play_sound(self, file, volume=None):
        if not self.sound_enabled or not pygame.mixer.get_init():
            return
        try:
            if file not in self._sound_cache:
                self._sound_cache[file] = pygame.mixer.Sound(file)
            sound = self._sound_cache[file]
            vol = volume if volume is not None else self.sound_volume
            sound.set_volume(vol)
            sound.play()
        except Exception as e:
            # Silently handle audio issues without crash
            pass

    def stop_music(self):
        if pygame.mixer.get_init():
            try:
                pygame.mixer.music.stop()
            except Exception:
                pass

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

