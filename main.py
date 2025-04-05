#!/usr/bin/env python3
import pygame, sys, os, time, math, random, cv2, numpy

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

def stop_music(): pygame.mixer.music.stop()

def imgLoad(file,size=None):
    image = pygame.image.load(file).convert_alpha()
    return pygame.transform.scale(image,size) if size else image

class Player:

    def __init__(self):
        self.health = 1
        self.money = 30000000
        self.score = 0
        self.level = 1
        self.exp = 0
        self.exp_to_next_level = 1000

    def add_exp(self, amount):
        self.exp += amount
        if self.exp >= self.exp_to_next_level:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.exp -= self.exp_to_next_level
        self.exp_to_next_level = int(self.exp_to_next_level * 1.5)
        self.health += 1
        self.money += 1000
        print(f"Level Up! Bạn đã đạt level {self.level}!")

player = Player()

# store images using a dictionary 
EnemyImageArray = dict()

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

class Map:
    def __init__(self):
        self.map = 'monkey lane'
        self.loadmap()
        print(self.targets)

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

mapvar = Map()

class Enemy:
    layers = [ # Name Health Speed CashReward ExpReward
        ('red',      1, 5.0, 0, 10),
        ('darkblue', 1, 5.0, 0, 15),
        ('green',    1, 5.2, 0, 20),
        ('yellow',   1, 6.0, 0, 25),
        ('purple',   2, 5.5, 0, 30),
        ('brown',    2, 5.8, 0, 35),
        ('magenta',  3, 5.3, 0, 40),
        ('aqua',     3, 5.6, 0, 45),]

    def __init__(self,layer):
        self.layer = layer
        self.setLayer()
        self.targets = mapvar.targets
        self.pos = list(self.targets[0])
        self.target = 0
        self.next_target()
        self.rect = self.image.get_rect(center=self.pos)
        self.distance = 0
        self.shape_type = random.randint(0, 4)
        self.shape_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.event = random.randint(0, 10)
        self.start = 0
        enemyList.append(self)

    def setLayer(self): 
        self.name,self.health,self.speed,self.cashprize,self.exp_reward = self.layers[self.layer]
        self.image = EnemyImageArray[self.name]

    def nextLayer(self): 
        old = self.shape_type
        valid_numbers = [n for n in range(0, 3) if n !=old]
        new = random.choice(valid_numbers)
        self.shape_type= new
        self.event= random.randint(0, 5)
        self.layer-=1; 
        if self.layer== -1: 
            self.kill()
        else :
            self.setLayer()
            player.add_exp(self.exp_reward)

    def next_target(self):
        if self.target<len(self.targets)-1:
            self.target+=1
            t=self.targets[self.target]
            self.angle = -((math.atan2(t[1]-self.pos[1],t[0]-self.pos[0]))/(math.pi/180))
            self.vx,self.vy = math.cos(math.radians(self.angle)),-math.sin(math.radians(self.angle))
        else:
            damage = self.layer + 1
            player.health -= damage
            player.score = max(0, player.score - 50)
            font = pygame.font.Font(None, 36)
            msg = font.render(f"-{damage}", True, (255, 0, 0))
            msg_rect = msg.get_rect(center=(self.pos[0], self.pos[1] - 20))
            screen = pygame.display.get_surface()
            screen.blit(msg, msg_rect)
            pygame.display.update(msg_rect)
            try:
                play_sound('sounds/life_lost.mp3', 0.3)
            except:
                print("Sound file not found")
            flash = pygame.Surface((screenWidth, screenHeight))
            flash.fill((255, 0, 0))
            for alpha in range(0, 255, 51):
                flash.set_alpha(255 - alpha)
                screen.blit(flash, (0,0))
                pygame.display.flip()
                pygame.time.delay(5)
            self.kill()

    def speedup(self):
        self.speed += 1

    def hit(self,damage):
        player.money+=1
        self.health -= damage
        if self.health<=0:
            player.money+=self.cashprize
            self.nextLayer() if self.layer>0 else self.kill()

    def kill(self):
        if self in enemyList:
            enemyList.remove(self)
        print(f"Enemy {self.name} popped!")
        player.score += 100
        player.add_exp(self.exp_reward)
        try:
            play_sound('sounds/pop3.mp3', 0.3)
        except:
            print("Không tìm thấy file âm thanh")

    def move(self,frametime):
        speed = frametime*fps*self.speed
        a,b = self.pos,self.targets[self.target]
        c= a.copy()
        a[0] += self.vx*speed
        a[1] += self.vy*speed
        if (a[0]-c[0])**2 + (a[1]-c[1])**2 >(b[0]-c[0])**2 + (b[1]-c[1])**2: self.next_target()
        self.rect.center = self.pos
        self.distance+=speed

    def draw_health_bar(self, screen):
        bar_width = self.rect.width
        bar_height = 5
        current_health_ratio = self.health / self.layers[self.layer][1]
        pygame.draw.rect(screen, (255, 0, 0), (self.rect.left, self.rect.top - bar_height, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (self.rect.left, self.rect.top - bar_height, bar_width * current_health_ratio, bar_height))
        line_length = 16
        line_y = self.rect.top - bar_height - 10
        
        if self.shape_type == 0:
            pygame.draw.line(screen, (0, 0, 0), 
                           (self.rect.centerx - line_length//2, line_y),
                           (self.rect.centerx + line_length//2, line_y), 5)
            pygame.draw.line(screen, self.shape_color, 
                           (self.rect.centerx - line_length//2, line_y),
                           (self.rect.centerx + line_length//2, line_y), 3)
        elif self.shape_type == 1:
            pygame.draw.line(screen, (0, 0, 0),
                           (self.rect.centerx, line_y - line_length//2),
                           (self.rect.centerx, line_y + line_length//2), 4)
            pygame.draw.line(screen, self.shape_color,
                           (self.rect.centerx, line_y - line_length//2),
                           (self.rect.centerx, line_y + line_length//2), 2)
        elif self.shape_type == 2:
            pygame.draw.line(screen, (0, 0, 0),
                           (self.rect.centerx - line_length//2, line_y - line_length//2),
                           (self.rect.centerx + line_length//2, line_y + line_length//2), 5)
            pygame.draw.line(screen, self.shape_color,
                           (self.rect.centerx - line_length//2, line_y - line_length//2),
                           (self.rect.centerx + line_length//2, line_y + line_length//2), 3)
        elif self.shape_type == 3:
            pygame.draw.line(screen, (0, 0, 0),
                           (self.rect.centerx - line_length//2, line_y - line_length//2),
                           (self.rect.centerx, line_y + line_length//2), 5)
            pygame.draw.line(screen, (0, 0, 0),
                           (self.rect.centerx + line_length//2, line_y - line_length//2),
                           (self.rect.centerx, line_y + line_length//2), 5)
            pygame.draw.line(screen, self.shape_color,
                           (self.rect.centerx - line_length//2, line_y - line_length//2),
                           (self.rect.centerx, line_y + line_length//2), 3)
            pygame.draw.line(screen, self.shape_color,
                           (self.rect.centerx + line_length//2, line_y - line_length//2),
                           (self.rect.centerx, line_y + line_length//2), 3)
        elif self.shape_type == 4:
            pygame.draw.circle(screen, (0, 0, 0),
                             (self.rect.centerx, line_y), line_length//1.5, 5)
            pygame.draw.circle(screen, self.shape_color,
                             (self.rect.centerx, line_y), line_length//1.5, 3)

def dispText(screen,wavenum):
    font = pygame.font.SysFont('arial', 18)
    h = font.get_height()+2
    strings = [
        ('Round: %d/%d' % (wavenum,len(mapvar.waves)),(200,20)),
        (str(player.money),(730,15)),
        (str(max(player.health,0)),(730,45)),
        ('Score: %d' % player.score,(200,45)),
        ('Level: %d' % player.level,(200,70)),
        ('EXP: %d/%d' % (player.exp, player.exp_to_next_level),(200,95))
    ]
    for string,pos in strings:
        text = font.render(string,2,(0,0,0))
        screen.blit(text,text.get_rect(midleft=pos))

def workEvents(selected, wave, speed, pos, drawing, spawn):
    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit(); sys.exit()
        if event.type == pygame.MOUSEBUTTONUP and event.button == 3: selected = None
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            drawing = True
            pos= [pygame.mouse.get_pos()]
        if event.type == pygame.MOUSEMOTION and drawing == True:
            mpos = pygame.mouse.get_pos()
            if len(pos) > 0:
                last_pos = pos[-1]
                dx = mpos[0] - last_pos[0]
                dy = mpos[1] - last_pos[1]
                dist = max(abs(dx), abs(dy))
                for i in range(dist):
                    x = last_pos[0] + dx * i / dist
                    y = last_pos[1] + dy * i / dist
                    pos.append((int(x), int(y)))
            pos.append(mpos)
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            drawing = False
            pos=[]
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not enemyList:
                if wave<=len(mapvar.waves): Sender(wave)
                else: print('Congratulations!! You survived the swarm')
            if event.key == pygame.K_w and speed<10: speed+=1
            if event.key == pygame.K_s and speed>1: speed-=1
        if event.type == SPAWN_HAIL:
            spawn_hail()

    return selected,wave,speed, pos, drawing

def spawn_hail():
        pos = pygame.mouse.get_pos()
        hail = Hail(pos[0], pos[1])
        hailList.append(hail)

SPAWN_HAIL= pygame.USEREVENT + 1

def detect(surface_temp):
    img = pygame.surfarray.array3d(surface_temp)
    img = numpy.transpose(img, (1, 0, 2))
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)
    
    kernel = numpy.ones((5,5), numpy.uint8)
    thresh = cv2.dilate(thresh, kernel, iterations=1)
    
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if len(contours) > 0:
        contour = max(contours, key=cv2.contourArea)
        if cv2.contourArea(contour) < 500:
            return None

        x, y, w, h = cv2.boundingRect(contour)
        
        if len(contour) >= 2:
            [vx, vy, x, y] = cv2.fitLine(contour, cv2.DIST_L2, 0, 0.01, 0.01)
            approx = cv2.approxPolyDP(contour, 0.002 * cv2.arcLength(contour, True), True)
            (a, b), radius = cv2.minEnclosingCircle(contour)
            circle_area = math.pi * (radius ** 2)
            contour_area = cv2.contourArea(contour)
            circularity = (4 * math.pi * contour_area) / (contour_area ** 2)
            angle = math.degrees(math.atan2(vy, vx))
            
            if (-20 <= angle <= 20) or (160 <= angle <= 200):
                if w > h * 2:
                    return "horizontal"
            
            elif (70 <= angle <= 110) or (-110 <= angle <= -70):
                if h > w * 2:
                    return "vertical"
            
            elif 25 <= angle <= 65:
                if abs(w - h) < min(w, h) * 0.5:
                    return "diagonal_right"
            
            elif len(contour) > 10:
                hull = cv2.convexHull(contour)
                if len(hull) >= 5:
                    hull_area = cv2.contourArea(hull)
                    contour_area = cv2.contourArea(contour)
                    if contour_area / hull_area < 0.75 and w > h * 0.8 and h > w * 0.8:
                        return "v_shape"
            if len(approx) > 8 and (contour_area / circle_area) > 0.5 and (4 * math.pi * contour_area) / (cv2.arcLength(contour, True) ** 2) > 0.5:
                return "circle"
    
    return None

def event_enemy(screen):
    for enemy in enemyList[:]:
        if enemy.event == 1 and enemy.pos[0] > 0:
            if enemy.start == 0:
                enemy.start = pygame.time.get_ticks()

            current= pygame.time.get_ticks()
            countdown= (current- enemy.start) // 1000
            num= max(0, 5- countdown)
            font= pygame.font.SysFont("Arial", 20, bold=True)
            text= font.render(str(num), 2, (0, 0, 0))
            text_rect = text.get_rect(center=enemy.rect.center)
            screen.blit(text, text_rect)

            if num==0: 
                startList. append(pygame.time.get_ticks())
                enemy.kill()
            print(startList)

def draw_cloud():
        if len(startList) > 0:
            e= startList[0]
            current = pygame.time.get_ticks()
            countdown = max (0, (current - startList[0]) // 1000)  
            if len(startList) > 1 and startList[1] - e < 2300: startList[1]= e
            if countdown < 3: 
                return True
            else: 
                startList.remove(e)
                return False
            
class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.start_time = pygame.time.get_ticks()
        self.img= None
        self.duration = 300  

    def draw(self, screen):
        boom1 = pygame.image.load("images/boom1.png").convert_alpha()
        boom1= pygame.transform.scale(boom1, (100, 100))
        boom2 = pygame.image.load("images/boom2.png").convert_alpha()
        boom2= pygame.transform.scale(boom2, (100, 100))
        boom3 = pygame.image.load("images/boom3.png").convert_alpha()
        boom3= pygame.transform.scale(boom3, (100, 100))
        current_time = pygame.time.get_ticks() - self.start_time
        if current_time < 100:
            self.img = boom1
            self.rect= self.img.get_rect(center=(self.x, self.y))
            screen.blit(self.img, self.rect)
        elif current_time < 200:
            self.img = boom2
            self.rect= self.img.get_rect(center=(self.x, self.y))
            screen.blit(self.img, self.rect)
        elif current_time < 300:
            self.img = boom3
            self.rect= self.img.get_rect(center=(self.x, self.y))
            screen.blit(self.img, self.rect)

    def is_done(self):
        return pygame.time.get_ticks() - self.start_time > self.duration

def check_collision_with_enemies(drawn_shape, surface_temp, screen):
    img = pygame.surfarray.array3d(surface_temp)
    img = numpy.transpose(img, (1, 0, 2))
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        contour = max(contours, key=cv2.contourArea)
        contour_rect = cv2.boundingRect(contour)

        for enemy in enemyList[:]:
                rdm = random.randint(1, 2)
                if enemy.shape_type == 0 and drawn_shape == "horizontal":
                    if rdm==1:
                        enemy.speedup()
                    else:
                        enemy.nextLayer()
                        if enemy.layer> -1: enemy.draw_health_bar(screen)
                elif enemy.shape_type == 1 and drawn_shape == "vertical":
                    if rdm==1:
                        enemy.speedup()
                    else:
                        enemy.nextLayer()
                        if enemy.layer> -1: enemy.draw_health_bar(screen)
                elif enemy.shape_type == 2 and drawn_shape == "diagonal_right":
                    if rdm==1:
                        enemy.speedup()
                    else:
                        enemy.nextLayer()
                        if enemy.layer> -1: enemy.draw_health_bar(screen)
                elif enemy.shape_type == 3 and drawn_shape == "v_shape":
                    if rdm==1:
                        enemy.speedup()
                    else:
                        enemy.nextLayer()
                        if enemy.layer> -1: enemy.draw_health_bar(screen)
                elif enemy.shape_type == 4 and drawn_shape == "circle":
                    rdm = random.randint(1, 3)
                    if rdm==1:
                        enemy.speedup()
                    else:
                        enemy.nextLayer()
                        if enemy.layer> -1: enemy.draw_health_bar(screen)

class Hail:
    def __init__(self, x, y):
        self.x, self.y = random.choice([
            (0, random.randint(-10, int(screenHeight/10))), 
            (random.randint(-10, screenWidth), 0)
        ])
        self.target= (x, y)
        self.speed = 10
        self.image = pygame.image.load("images/meteor1.png").convert_alpha()
        self.rect= self.image.get_rect(center=(self.x, self.y))
        self.angle = None

    def draw(self, screen):
        img= random.randint(1, 3)
        if img==1:
            self.image = pygame.image.load("images/meteor1.png").convert_alpha()
        elif img==2:
            self.image = pygame.image.load("images/meteor2.png").convert_alpha()
        elif img==3:
            self.image = pygame.image.load("images/meteor3.png").convert_alpha()
        self.image = pygame.transform.rotate(self.image, 90- math.degrees(math.atan2(self.y, self.x)))
        self.image = pygame.transform.scale(self.image, (100, 100))
        if self.angle/math.pi*180 > -180 and self.angle/math.pi*180 < -90:
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect(center=self.rect.center) 
        screen.blit(self.image, self.rect)
        print("angle", self.angle/math.pi*180)

    def move(self, screen):
        dx = self.target[0] - self.x
        dy = self.target[1] - self.y

        self.angle= -math.atan2(dy, dx)
        print("angle chuột", self.angle/math.pi*180)
        print("angle enemy", math.atan2(self.y,self.x)/math.pi*180)
        print(self.target)
        x_target = math.cos(self.angle) * self.speed
        y_target = -math.sin(self.angle) * self.speed
        next_pos = (self.x + x_target, self.y + y_target)
        distance= math.sqrt(dx**2 + dy**2)
        if distance < self.speed:
            self.x, self.y = self.target
            hailList.remove(self)
        else:
            self.x += x_target
            self.y += y_target

        self.rect.center = (self.x, self.y)

class Menu:
    def __init__(self):
        self.font_big = pygame.font.Font(None, 74)
        self.font_small = pygame.font.Font(None, 36)
        self.buttons = [
            {'text': 'START', 'color': (255, 255, 255), 'hover_color': (0, 255, 0), 'rect': None},
            {'text': 'HUONG DAN', 'color': (255, 255, 255), 'hover_color': (0, 255, 0), 'rect': None},
            {'text': 'ECS', 'color': (255, 255, 255), 'hover_color': (0, 255, 0), 'rect': None}
        ]
        self.game_title = self.font_big.render('TOWER DEFENSE', True, (255, 215, 0))
        self.title_rect = self.game_title.get_rect(center=(screenWidth // 2, 100))
        self.button_spacing = 80
        self.initialize_buttons()

    def initialize_buttons(self):
        for i, button in enumerate(self.buttons):
            text_surface = self.font_small.render(button['text'], True, button['color'])
            text_rect = text_surface.get_rect(center=(screenWidth // 2, 250 + i * self.button_spacing))
            button['rect'] = text_rect

    def draw(self, screen, mouse_pos):
        screen.fill((0, 0, 0))
        screen.blit(self.game_title, self.title_rect)
        for button in self.buttons:
            color = button['hover_color'] if button['rect'].collidepoint(mouse_pos) else button['color']
            text_surface = self.font_small.render(button['text'], True, color)
            screen.blit(text_surface, button['rect'])

    def handle_click(self, mouse_pos):
        for i, button in enumerate(self.buttons):
            if button['rect'].collidepoint(mouse_pos):
                return i
        return None

def show_instructions(screen):
    running = True
    font = pygame.font.Font(None, 36)
    instructions = [
        "HUONG DAN CHOI:",
        "- Dat cac thap de bao ve duong di",
        "- Tieu diet ke dich de nhan tien",
        "- Bao ve can cu khong de ke dich di qua",
        "- Nhan SPACE de bat dau wave quai",
        "- Ve hinh tuong ung voi ky hieu tren quai de tieu diet",
        "",
        "Nhan ESC de quay lai"
    ]

    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        screen.fill((0, 0, 0))
        for i, line in enumerate(instructions):
            text = font.render(line, True, (255, 255, 255))
            screen.blit(text, (screenWidth // 4, 150 + i * 50))
        pygame.display.flip()

def play_sound(file, volume=0.5):
    sound = pygame.mixer.Sound(file)
    sound.set_volume(volume)
    sound.play()

class Sender:
    def __init__(self,wave):
        self.wave = wave
        self.timer = 0 
        self.rate = 1
        self.enemies = []
        enemies = mapvar.waves[wave-1].split(',')
        for enemy in enemies:
            amount,layer = enemy.split('*')
            self.enemies += [eval(layer)-1]*eval(amount)
        senderList.append(self)

    def update(self,frametime,wave):
        if not self.enemies:
            if not enemyList: 
                senderList.remove(self)
                wave+=1
                player.money+=99+self.wave
        elif self.timer > 0: 
            self.timer -= frametime
        else: 
            self.timer = self.rate
            Enemy(self.enemies[0])
            del self.enemies[0]
        return wave

class GameOver:
    def __init__(self):
        self.font_big = pygame.font.Font(None, 74)
        self.font_small = pygame.font.Font(None, 36)
        self.game_over_text = self.font_big.render('GAME OVER', True, (255, 0, 0))
        self.title_rect = self.game_over_text.get_rect(center=(screenWidth // 2, 200))
        
        self.menu_button = {
            'text': 'QUAY LAI MENU',
            'color': (255, 255, 255),
            'hover_color': (0, 255, 0),
            'rect': None
        }
        self.initialize_button()

    def initialize_button(self):
        text_surface = self.font_small.render(self.menu_button['text'], True, self.menu_button['color'])
        text_rect = text_surface.get_rect(center=(screenWidth // 2, 300))
        self.menu_button['rect'] = text_rect

    def draw(self, screen, mouse_pos):
        screen.fill((0, 0, 0))
        screen.blit(self.game_over_text, self.title_rect)
        
        color = self.menu_button['hover_color'] if self.menu_button['rect'].collidepoint(mouse_pos) else self.menu_button['color']
        text_surface = self.font_small.render(self.menu_button['text'], True, color)
        screen.blit(text_surface, self.menu_button['rect'])

    def handle_click(self, mouse_pos):
        if self.menu_button['rect'].collidepoint(mouse_pos):
            return True
        return False

def main():
    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.display.set_caption('Bloons Tower Defence')
    screen = pygame.display.set_mode((screenWidth,screenHeight))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None,20)

    # Add this line to load enemy images
    loadImages()
    
    mapvar.getmovelist()

    pygame.time.set_timer(SPAWN_HAIL, 3000)
    drawing= False
    pos=[]
    spawn= True

    menu = Menu()
    game_over = GameOver()
    game_state = "menu"

    background = pygame.Surface((800,600)); background.set_colorkey((0,0,0))
    heart,money,plank = imgLoad('images/hearts.png'),imgLoad('images/moneySign.png'),imgLoad('images/plankBlank.png')
    w,h = plank.get_size()
    for y in range(screenHeight//h): background.blit(plank,(screenWidth-w,y*h))
    for y in range(3):
        for x in range(screenWidth//w): background.blit(plank,(x*w,screenHeight-(y+1)*h))
    background.blit(money,(screenWidth-w+6,h//2-money.get_height()//2))
    background.blit(heart,(screenWidth-w+6,h+h//2-heart.get_height()//2))
    
    level_img,t1,t2 = mapvar.get_background()

    selected = None
    speed = 3
    wave = 1

    play_music('music/maintheme.mp3')
    while True:
        if game_state == "menu":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    button_clicked = menu.handle_click(event.pos)
                    if button_clicked == 0:
                        game_state = "game"
                    elif button_clicked == 1:
                        game_state = "instructions"
                    elif button_clicked == 2:
                        pygame.quit()
                        sys.exit()

            menu.draw(screen, pygame.mouse.get_pos())
            pygame.display.flip()
            clock.tick(fps)

        elif game_state == "instructions":
            show_instructions(screen)
            game_state = "menu"
        elif game_state == "game":
            starttime = time.time()
            clock.tick(fps)
            frametime = (time.time()-starttime)*speed
            
            # Kiểm tra health = 0
            if player.health <= 0:
                game_state = "game_over"
                continue
                
            screen.blit(level_img,(0,0))
            mpos = pygame.mouse.get_pos()

            if senderList: wave = senderList[0].update(frametime,wave)

            z0,z1 = [],[]
            for enemy in enemyList:
                d = enemy.distance
                if d<580: z1+=[enemy]
                elif d<950: z0+=[enemy]
                elif d<2392: z1+=[enemy]
                elif d<2580: z0+=[enemy]
                else: z0+=[enemy]

            for enemy in z0:
                enemy.move(frametime)
                screen.blit(enemy.image,enemy.rect)
                enemy.draw_health_bar(screen)
                screen.blit(t1,(0,0))
                screen.blit(t2,(0,0))
            for enemy in z1: 
                enemy.move(frametime)
                screen.blit(enemy.image,enemy.rect)
                enemy.draw_health_bar(screen)

            screen.blit(background,(0,0))
            selected,wave,speed, pos, drawing = workEvents(selected,wave,speed, pos, drawing, spawn)
            surface_temp= pygame.Surface((800,600)).convert_alpha()
            surface_temp.fill((0,0,0,0))
            if (len(pos)>1):
                pygame.draw.aalines(surface_temp, (255, 255, 255), False, pos, 8)
                if drawing:
                    guide_surface = pygame.Surface((screenWidth, screenHeight), pygame.SRCALPHA)
                    pygame.draw.aalines(guide_surface, (100, 100, 255, 128), False, pos, 12)
                    screen.blit(guide_surface, (0, 0))
            dispText(screen,wave)
            if len(pos) > 10:
                shape_detected = detect(surface_temp)
                if shape_detected:
                    check_collision_with_enemies(shape_detected, surface_temp, screen)
                    if shape_detected == "horizontal":
                        font = pygame.font.SysFont('arial', 22)
                        text = font.render("Ban da ve gach ngang", 2, (255, 255, 255))
                        surface_temp.blit(text, (screenWidth // 2 - w, screenHeight - 2 * h))
                    elif shape_detected == "vertical":
                        font = pygame.font.SysFont('arial', 22)
                        text = font.render("Ban da ve gach đung", 2, (255, 255, 255))
                        surface_temp.blit(text, (screenWidth // 2 - w, screenHeight - 2 * h))
                    elif shape_detected == "diagonal_right":
                        font = pygame.font.SysFont('arial', 22)
                        text = font.render("Ban da ve gach cheo phai", 2, (255, 255, 255))
                        surface_temp.blit(text, (screenWidth // 2 - w, screenHeight - 2 * h))
                    elif shape_detected == "v_shape":
                        font = pygame.font.SysFont('arial', 22)
                        text = font.render("Ban da ve hinh chu V", 2, (255, 255, 255))
                        surface_temp.blit(text, (screenWidth // 2 - w, screenHeight - 2 * h))
            screen.blit(surface_temp,(0,0))
            event_enemy(screen)
            cloud_image = pygame.image.load("images/mud.png")
            cloud_image= pygame.transform.scale(cloud_image, (screenWidth, screenHeight))
            if draw_cloud()== True:
                screen.blit(cloud_image, (0, 0))
                for enemy in enemyList[:]:
                    enemy.move(frametime)
                pygame.display.flip()

            for hail in hailList[:]:
                hail.move(screen)
                hail.draw(screen)
                
                for enemy in enemyList[:]:
                    if hail.rect.colliderect(enemy.rect):
                        enemy.kill()
                        if (hail in hailList): 
                            start_time= pygame.time.get_ticks()
                            hailList.remove(hail)
                            explosionList.append(Explosion(enemy.rect.centerx, enemy.rect.centery))
            for explosion in explosionList[:]:
                explosion.draw(screen)
                if explosion.is_done():
                    explosionList.remove(explosion)
                        
            pygame.display.flip()

        elif game_state == "game_over":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if game_over.handle_click(event.pos):
                        # Reset game state
                        player.health = 1
                        player.money = 30000000
                        player.score = 0
                        player.level = 1
                        player.exp = 0
                        player.exp_to_next_level = 1000
                        enemyList.clear()
                        bulletList.clear()
                        iconList.clear()
                        senderList.clear()
                        startList.clear()
                        hailList.clear()
                        explosionList.clear()
                        game_state = "menu"

            game_over.draw(screen, pygame.mouse.get_pos())
            pygame.display.flip()
            clock.tick(fps)

if __name__ == '__main__':
     main()