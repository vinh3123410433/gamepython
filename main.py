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
towerList = []
bulletList = []
iconList = []
senderList = []
startList= []
hailList = []
# initalize empty arrays of items on new map

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
    # load music from file mp3
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(loop)
# comment out if you don't want music

def stop_music(): pygame.mixer.music.stop()
#
def imgLoad(file,size=None):
    image = pygame.image.load(file).convert_alpha()
    return pygame.transform.scale(image,size) if size else image

class Player:
    towers = [ # Name of monkey tower
        'Dart Monkey',
        'Tack Shooter',
        'Sniper Monkey',
        'Boomerang Thrower',
        'Ninja Monkey',
        'Bomb Tower',
        'Ice Tower',
        'Glue Gunner',
        'Monkey Buccaneer',
        'Super Monkey',
        'Monkey Apprentice',
        'Spike Factory',
        'Road Spikes',
        'Exploding Pineapple',]
    def __init__(self):
        self.health = 10
        self.money = 30000000
        self.score = 0
        self.level = 1
        self.exp = 0
        self.exp_to_next_level = 1000
        self.tower_upgrades = {}  # Lưu trữ trạng thái nâng cấp của tháp

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
TowerImageArray = dict()
def loadImages():
    for tower in player.towers: TowerImageArray[tower] = imgLoad('towers/'+tower.lower()+'.png')
    # load selected tower

    bloon = imgLoad('enemies/bloonImg.png')
    EnemyImageArray['red'] = bloon
    width,height = bloon.get_size()
    for name in colors:
        image = bloon.copy()
        for x in range(width):
            for y in range(height):
                p = image.get_at((x,y))[:-1]
                if p not in ((0,0,0),(255,255,255)):
                    # check if in rgb colour bounds
                    c = colors[name]
                    r,g,b = p[0]*c[0]/255, p[0]*c[1]/255, p[0]*c[2]/255
                    image.set_at((x,y),(min(int(r),255),min(int(g),255),min(int(b),255)))
        EnemyImageArray[name] = image

def get_angle(a,b):
    # return 180-(math.atan2(b[0]-a[0],b[1]-a[1]))/(math.pi/180)
    return (math.atan2(b[1]-a[1],b[0]-a[0]))/(math.pi/180) +90

class Map:
    # setup map
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
        # load from background png
        background = imgLoad('maps/%s/image.png' % self.map)
        background2 = imgLoad('maps/%s/image2.png' % self.map).convert_alpha()
        background3 = imgLoad('maps/%s/image3.png' % self.map).convert_alpha()
        # for i in range(len(self.targets)-1):
        #     pygame.draw.line(background,(0,0,0),self.targets[i],self.targets[i+1])

        return background,background2,background3

mapvar = Map()



class Enemy:
    layers = [ # Name Health Speed CashReward ExpReward
        ('red',      1, 1.0, 0, 10),
        ('darkblue', 1, 1.0, 0, 15),
        ('green',    1, 1.2, 0, 20),
        ('yellow',   1, 2.0, 0, 25),
        ('purple',   2, 1.5, 0, 30),
        ('brown',    2, 1.8, 0, 35),
        ('magenta',  3, 1.3, 0, 40),
        ('aqua',     3, 1.6, 0, 45),]

    # initalize enemy
    def __init__(self,layer):
        self.layer = layer #index
        self.setLayer()
        self.targets = mapvar.targets
        self.pos = list(self.targets[0])
        self.target = 0 #index
        self.next_target()
        self.rect = self.image.get_rect(center=self.pos)
        self.distance = 0
        # Chọn ngẫu nhiên loại hình và màu khi khởi tạo
        self.shape_type = random.randint(0, 4)
        self.shape_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.event= 2
        self.start= 0
        enemyList.append(self) #sau khi khởi tạo thì tự thêm chính nó vào mảng

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
        # check if bloons reached the ending
        if self.target<len(self.targets)-1: #index tọa đô
            self.target+=1
            t=self.targets[self.target]
            self.angle = -((math.atan2(t[1]-self.pos[1],t[0]-self.pos[0]))/(math.pi/180)) # vì y bị ngược nên dấu trừ để lật lại hướng

            self.vx,self.vy = math.cos(math.radians(self.angle)),-math.sin(math.radians(self.angle)) #tính từ điểm bắt đầu

            #self.angle = 180-((math.atan2(t[0]-self.pos[0],t[1]-self.pos[1]))/(math.pi/180)) #tác giả truyển input ngược(x,y) thay vì (y,x) nên lật bằng 180 - alpha

            #self.vx,self.vy = math.sin(math.radians(self.angle)),-math.cos(math.radians(self.angle)) #tính từ điểm kết thúc
            
        # end game / player if so (no health)
        else: self.kill(); player.health -= (self.layer+1) #index layer hiện tại +1

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
        # Add optional effects or sounds for smoother feedback
        print(f"Enemy {self.name} popped!")
        player.score += 100
        player.add_exp(self.exp_reward)
        try:
            play_sound('sounds/pop3.mp3', 0.3)
        except:
            print("Không tìm thấy file âm thanh")

    def move(self,frametime, ):
        speed = frametime*fps*self.speed

        a,b = self.pos,self.targets[self.target] #list, tuple
        c= a.copy()
        a[0] += self.vx*speed
        #
        a[1] += self.vy*speed
        
        # if (b[0]-a[0])**2+(b[1]-a[1])**2<=speed**2: self.next_target()
        if (a[0]-c[0])**2 + (a[1]-c[1])**2 >(b[0]-c[0])**2 + (b[1]-c[1])**2: self.next_target()
        self.rect.center = self.pos
        self.distance+=speed
    def draw_health_bar(self, screen):
        # Vẽ thanh máu trên đầu kẻ địch
        bar_width = self.rect.width
        bar_height = 5  # Chiều cao thanh máu

        # Tỷ lệ máu còn lại
        current_health_ratio = self.health / self.layers[self.layer][1]

        # Vẽ thanh máu (viền đỏ)
        pygame.draw.rect(screen, (255, 0, 0), (self.rect.left, self.rect.top - bar_height, bar_width, bar_height))

        # Vẽ thanh máu còn lại (xanh lá)
        pygame.draw.rect(screen, (0, 255, 0), (self.rect.left, self.rect.top - bar_height, bar_width * current_health_ratio, bar_height))

        # Vẽ ký hiệu gạch
        line_length = 16  # Tăng độ dài của gạch từ 13 lên 16
        line_y = self.rect.top - bar_height - 10  # Vị trí y của gạch
        
        if self.shape_type == 0:
            # Vẽ viền đen cho gạch ngang
            pygame.draw.line(screen, (0, 0, 0), 
                           (self.rect.centerx - line_length//2, line_y),
                           (self.rect.centerx + line_length//2, line_y), 5)
            # Vẽ gạch ngang có màu 
            pygame.draw.line(screen, self.shape_color, 
                           (self.rect.centerx - line_length//2, line_y),
                           (self.rect.centerx + line_length//2, line_y), 3)
        elif self.shape_type == 1:
            # Vẽ viền đen cho gạch dọc
            pygame.draw.line(screen, (0, 0, 0),
                           (self.rect.centerx, line_y - line_length//2),
                           (self.rect.centerx, line_y + line_length//2), 4)
            # Vẽ gạch dọc có màu
            pygame.draw.line(screen, self.shape_color,
                           (self.rect.centerx, line_y - line_length//2),
                           (self.rect.centerx, line_y + line_length//2), 2)
        elif self.shape_type == 2:
            # Vẽ viền đen cho gạch chéo xuống
            pygame.draw.line(screen, (0, 0, 0),
                           (self.rect.centerx - line_length//2, line_y - line_length//2),
                           (self.rect.centerx + line_length//2, line_y + line_length//2), 5)
            # Vẽ gạch chéo xuống có màu
            pygame.draw.line(screen, self.shape_color,
                           (self.rect.centerx - line_length//2, line_y - line_length//2),
                           (self.rect.centerx + line_length//2, line_y + line_length//2), 3)
        #elif self.shape_type == 3:
            # Vẽ gạch chéo lên
            #pygame.draw.line(screen, self.shape_color,
                           #(self.rect.centerx - line_length//2, line_y + line_length//2),
                           #(self.rect.centerx + line_length//2, line_y - line_length//2), 2)
        elif self.shape_type == 3:
            # Vẽ viền đen cho chữ V
            pygame.draw.line(screen, (0, 0, 0),
                           (self.rect.centerx - line_length//2, line_y - line_length//2),
                           (self.rect.centerx, line_y + line_length//2), 5)
            pygame.draw.line(screen, (0, 0, 0),
                           (self.rect.centerx + line_length//2, line_y - line_length//2),
                           (self.rect.centerx, line_y + line_length//2), 5)
            # Vẽ chữ V có màu
            pygame.draw.line(screen, self.shape_color,
                           (self.rect.centerx - line_length//2, line_y - line_length//2),
                           (self.rect.centerx, line_y + line_length//2), 3)
            pygame.draw.line(screen, self.shape_color,
                           (self.rect.centerx + line_length//2, line_y - line_length//2),
                           (self.rect.centerx, line_y + line_length//2), 3)
        elif self.shape_type == 4:
            # Vẽ viền đen cho hình tròn
            pygame.draw.circle(screen, (0, 0, 0),
                             (self.rect.centerx, line_y), line_length//1.5, 5)
            # Vẽ hình tròn có màu
            pygame.draw.circle(screen, self.shape_color,
                             (self.rect.centerx, line_y), line_length//1.5, 3)

class Tower:
    def __init__(self,pos):
        self.targetTimer = 0
        self.rect = self.image.get_rect(center=pos)
        self.level = 1
        self.max_level = 3
        towerList.append(self)

    def upgrade(self):
        if self.level < self.max_level:
            self.level += 1
            self.damage *= 1.5
            self.range *= 1.2
            self.firerate *= 1.2
            self.cost = int(self.cost * 1.5)
            print(f"Tháp đã được nâng cấp lên level {self.level}!")
            try:
                play_sound('sounds/new upgrade.mp3', 0.3)
            except:
                print("Không tìm thấy file âm thanh")

    def takeTurn(self,frametime,screen):
        self.startTargetTimer = self.firerate
        self.targetTimer -= frametime
        if self.targetTimer<=0:
            enemypoint = self.target()
            if enemypoint:
                pygame.draw.line(screen,(255,255,255),self.rect.center,enemypoint)
                self.targetTimer=self.startTargetTimer
                try:
                    play_sound('sounds/shoot.mp3', 0.2)
                except:
                    print("Không tìm thấy file âm thanh")
    def target(self):
        # for each enemy loop
        for enemy in sorted(enemyList,key=lambda i: i.distance,reverse=True):
            if (self.rect.centerx-enemy.rect.centerx)**2+(self.rect.centery-enemy.rect.centery)**2<=self.rangesq:
                self.angle = int(get_angle(self.rect.center,enemy.rect.center))
                print(self.angle)
                self.image = pygame.transform.rotate(self.imagecopy,-self.angle)
                self.rect = self.image.get_rect(center=self.rect.center)
                enemy.hit(self.damage)
                return enemy.rect.center

class createTower(Tower):
    # generate the tower
    def __init__(self,tower,pos,info):
        self.tower = tower
        self.cost,self.firerate,self.range,self.damage = info
        self.rangesq = self.range**2

        # set properties (damage, firerate, range)
        
        self.image = TowerImageArray[tower]
        self.imagecopy = self.image.copy()
        self.angle = 0
        Tower.__init__(self,pos)

class Icon:
    # adjust icons of the towers here
    towers = { # Cost Fire speed Range Damage
        'Dart Monkey'         : [ 215, 1.3, 100, 1],
        # [ Cost, Fire speed , Range, Damage]
        'Tack Shooter'        : [ 360, 1.0, 70, 1],
        'Sniper Monkey'       : [ 430, 2.9, 300, 2],
        'Boomerang Thrower'   : [ 430, 1.0, 90, 1],
        'Ninja Monkey'        : [ 650, 1.0, 90, 1],
        'Bomb Tower'          : [ 700, 1, 90, 2],
        'Ice Tower'           : [ 410, 1.3, 90, 1],
        'Glue Gunner'         : [ 325, 1.1, 100, 1],
        'Monkey Buccaneer'    : [ 650, 0.99, 100, 1],
        'Super Monkey'        : [ 3000, 0.15, 200, 1],
        'Monkey Apprentice'   : [ 595, 1.0, 60, 1],
        'Spike Factory'       : [ 650, 2.0, 40, 1],
        'Road Spikes'         : [  30, 5.0, 40, 1],
        'Exploding Pineapple' : [  25, 2.0, 60, 1],}

    def __init__(self,tower):
        # initalize tower and it's properties
        self.tower = tower
        self.cost,self.firerate,self.range,self.damage = self.towers[tower]
        iconList.append(self)
        self.img = pygame.transform.scale(TowerImageArray[tower],(41,41))
        i = player.towers.index(tower); x,y = i%2,i//2
        self.rect = self.img.get_rect(x=700+x*(41+6)+6,y=100+y*(41+6)+6)


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

# https://realpython.com/lessons/using-blit-and-flip/

# Block Transfer, and .blit() is how you copy the contents of one Surface to another
def drawTower(screen,tower,selected):
    screen.blit(tower.image,tower.rect)
    if tower == selected:
        rn = tower.range
        surface = pygame.Surface((2*rn,2*rn)).convert_alpha(); surface.fill((0,0,0,0))
        pygame.draw.circle(surface,(0,255,0,85),(rn,rn),rn)
        screen.blit(surface,tower.rect.move((-1*rn,-1*rn)).center)

    elif tower.rect.collidepoint(pygame.mouse.get_pos()):
        rn = tower.range
        surface = pygame.Surface((2*rn,2*rn)).convert_alpha(); surface.fill((0,0,0,0))
        pygame.draw.circle(surface,(255,255,255,85),(rn,rn),rn)
        screen.blit(surface,tower.rect.move((-1*rn,-1*rn)).center)

def selectedIcon(screen,selected):

    mpos = pygame.mouse.get_pos()
    # using active mouse position
    image = TowerImageArray[selected.tower]
    rect = image.get_rect(center=mpos)
    screen.blit(image,rect)

    collide = False
    rn = selected.range
    surface = pygame.Surface((2*rn,2*rn)).convert_alpha(); surface.fill((0,0,0,0))
    pygame.draw.circle(surface,(255,0,0,75) if collide else (0,0,255,75),(rn,rn),rn)
    screen.blit(surface,surface.get_rect(center=mpos))

def selectedTower(screen,selected,mousepos):
#testing
    selected.genButtons(screen)

    for img,rect,info,infopos,cb in selected.buttonlist:
        screen.blit(img,rect)
        if rect.collidepoint(mousepos): screen.blit(info,infopos)

def drawIcon(screen,icon,mpos,font):
    screen.blit(icon.img,icon.rect)

    if icon.rect.collidepoint(mpos):
        text = font.render("%s Tower (%d)" % (icon.tower,icon.cost),2,(0,0,0))
        textpos = text.get_rect(right=700-6,centery=icon.rect.centery)
        screen.blit(text,textpos)

class Sender:
    def __init__(self,wave):
        self.wave = wave; self.timer = 0; self.rate = 1
        self.enemies = []; enemies = mapvar.waves[wave-1].split(',')
        for enemy in enemies:
            amount,layer = enemy.split('*')
            self.enemies += [eval(layer)-1]*eval(amount)
        senderList.append(self)

    def update(self,frametime,wave):
        if not self.enemies:
            if not enemyList: senderList.remove(self); wave+=1; player.money+=99+self.wave
        elif self.timer > 0: self.timer -= frametime
        else: self.timer = self.rate; Enemy(self.enemies[0]); del self.enemies[0]
        return wave

def workEvents(selected, wave, speed, pos, drawing):
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

            if event.key == pygame.K_k and selected in towerList: player.money+=int(selected.cost*0.9); towerList.remove(selected); selected = None
            if event.key == pygame.K_w and speed<10: speed+=1
            if event.key == pygame.K_s and speed>1: speed-=1
            
               
        keys = pygame.key.get_pressed()  # Lấy trạng thái phím

        if keys[pygame.K_a]:
            mpos = pygame.mouse.get_pos()
            hailList.append(Hail(mpos[0], mpos[1]))

    return selected,wave,speed, pos, drawing

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
                    # Refine the v_shape detection to avoid conflicts with diagonal_left
                    if contour_area / hull_area < 0.75 and w > h * 0.8 and h > w * 0.8:
                        return "v_shape"
            if len(approx) > 8 and (contour_area / circle_area) > 0.5 and (4 * math.pi * contour_area) / (cv2.arcLength(contour, True) ** 2) > 0.5:
                return "circle"
    
    return None

def event_enemy(screen):
    for enemy in enemyList[:]:
        if enemy.event == 1 and enemy.pos[0] > 0:
            if enemy.start == 0:  # Chỉ gán start nếu chưa có giá trị
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
            # if enemy.rect.colliderect(contour_rect):
                rdm = random.randint(1, 2)
                if enemy.shape_type == 0 and drawn_shape == "horizontal":
                    # enemy.kill()
                    if rdm==1:
                        enemy.speedup()
                    else:
                        enemy.nextLayer()
                        if enemy.layer> -1: enemy.draw_health_bar(screen)
                elif enemy.shape_type == 1 and drawn_shape == "vertical":
                    # enemy.kill()
                    if rdm==1:
                        enemy.speedup()
                    else:
                        enemy.nextLayer()
                        if enemy.layer> -1: enemy.draw_health_bar(screen)
                elif enemy.shape_type == 2 and drawn_shape == "diagonal_right":
                    # enemy.kill()
                    if rdm==1:
                        enemy.speedup()
                    else:
                        enemy.nextLayer()
                        if enemy.layer> -1: enemy.draw_health_bar(screen)
                elif enemy.shape_type == 3 and drawn_shape == "v_shape":
                    # enemy.kill()
                    if rdm==1:
                        enemy.speedup()
                    else:
                        enemy.nextLayer()
                        if enemy.layer> -1: enemy.draw_health_bar(screen)
                elif enemy.shape_type == 4 and drawn_shape == "circle":
                    # enemy.kill()
                    rdm = random.randint(1, 3)
                    if rdm==1:
                        enemy.speedup()
                    else:
                        enemy.nextLayer()
                        if enemy.layer> -1: enemy.draw_health_bar(screen)

class Hail:
    def __init__(self, x, y):
        self.x, self.y = random.choice([(0, random.randint(-10, screenHeight/10)), (random.randint(-10, screenWidth), 0)])
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
        self.image = pygame.transform.rotate(self.image, math.degrees(self.angle))
        self.image = pygame.transform.scale(self.image, (100, 100))
        if self.angle/math.pi*180 > -180 and self.angle/math.pi*180 < -90:
            self.image = pygame.transform.flip(self.image, True, False)
        screen.blit(self.image, (self.x, self.y))
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

    # def hit_target(self):
    #     print("hail", self.x, self.y)
    #     print("enemy", self.target.rect.centerx, self.target.rect.centery)
    #     if self.rect.colliderect(self.target.rect):
    #         print ("Hail hit the target!")
    #         return True
    #     return False
    

    # def move(self): 
    #     if self.target:
    #         enemy_vx = self.target.vx
    #         enemy_vy = self.target.vy
    #         dx = self.target.targets[self.target.target][0] - self.x
    #         dy = self.target.targets[self.target.target][1] - self.y
    #         distance = math.sqrt(dx ** 2 + dy ** 2)

    #         t = distance / self.speed

    #         future_x = self.target.rect.centerx + enemy_vx * t
    #         future_y = self.target.rect.centery + enemy_vy * t

    #         dx_future = future_x - self.x
    #         dy_future = future_y - self.y
    #         distance_future = math.sqrt(dx_future ** 2 + dy_future ** 2)

    #         if distance_future > 0:
    #             self.x += dx_future / distance_future * self.speed
    #             self.y += dy_future / distance_future * self.speed

    #         self.rect.center = (self.x, self.y)


class Menu:
    def __init__(self):
        self.font_big = pygame.font.Font(None, 74)
        self.font_small = pygame.font.Font(None, 36)
        self.buttons = [
            {'text': 'CHƠI GAME', 'color': (255, 255, 255), 'hover_color': (0, 255, 0), 'rect': None},
            {'text': 'HƯỚNG DẪN', 'color': (255, 255, 255), 'hover_color': (0, 255, 0), 'rect': None},
            {'text': 'THOÁT', 'color': (255, 255, 255), 'hover_color': (0, 255, 0), 'rect': None}
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
        "HƯỚNG DẪN CHƠI:",
        "- Đặt các tháp để bảo vệ đường đi",
        "- Tiêu diệt kẻ địch để nhận tiền",
        "- Bảo vệ căn cứ không để kẻ địch đi qua",
        "- Nhấn SPACE để bắt đầu wave quái",
        "- Vẽ hình tương ứng với ký hiệu trên quái để tiêu diệt",
        "",
        "Nhấn ESC để quay lại"
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
 
#hhw
# main file
def main():
    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.display.set_caption('Bloons Tower Defence')
    screen = pygame.display.set_mode((screenWidth,screenHeight))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None,20)

    mapvar.getmovelist()

    drawing= False
    pos=[]
    meteor= 1

    # Khởi tạo menu
    menu = Menu()
    game_state = "menu"  # Có thể là "menu", "game", "instructions"

    background = pygame.Surface((800,600)); background.set_colorkey((0,0,0))
    heart,money,plank = imgLoad('images/hearts.png'),imgLoad('images/moneySign.png'),imgLoad('images/plankBlank.png')
    w,h = plank.get_size()
    for y in range(screenHeight//h): background.blit(plank,(screenWidth-w,y*h))
    for y in range(3):
        for x in range(screenWidth//w): background.blit(plank,(x*w,screenHeight-(y+1)*h))
    background.blit(money,(screenWidth-w+6,h//2-money.get_height()//2))
    background.blit(heart,(screenWidth-w+6,h+h//2-heart.get_height()//2))
    
    level_img,t1,t2 = mapvar.get_background()
    loadImages()
    # for tower in player.towers: Icon(tower)
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
                    if button_clicked == 0:  # CHƠI GAME
                        game_state = "game"
                    elif button_clicked == 1:  # HƯỚNG DẪN
                        game_state = "instructions"
                    elif button_clicked == 2:  # THOÁT
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
            for enemy in z1: enemy.move(frametime); screen.blit(enemy.image,enemy.rect); enemy.draw_health_bar(screen)

            for tower in towerList: tower.takeTurn(frametime,screen); drawTower(screen,tower,selected)


            screen.blit(background,(0,0))

            for icon in iconList: drawIcon(screen,icon,mpos,font)
            selected,wave,speed, pos, drawing = workEvents(selected,wave,speed, pos, drawing)
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
            cloud_image = pygame.image.load("images/cloud.png")
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
                        hailList.remove(hail)
                        break
                
            pygame.display.flip()

if __name__ == '__main__':
    main()
#'20*1','30*1',