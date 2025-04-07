import pygame, random, math
from map import Map
from player import Player
from setting import fps, screenWidth, screenHeight, enemyList, EnemyImageArray,play_sound


class Enemy:
    layers = [ # Name Health Speed CashReward ExpReward
        ('red',      1, 2.0, 100, 10),
        ('darkblue', 1, 2.0, 0, 15),
        ('green',    1, 3.0, 0, 20),
        ('yellow',   1, 4.0, 0, 25),
        ('purple',   2, 5.5, 0, 30),
        ('brown',    2, 5.8, 0, 35),
        ('magenta',  3, 5.3, 0, 40),
        ('aqua',     3, 5.6, 0, 45),]

    def __init__(self,layer, mapvar, player):
        self.player = player
        self.mapvar = mapvar
        self.layer = layer
        self.setLayer()
        self.targets = mapvar.targets
        self.pos = list(self.targets[0])
        self.target = 0
        self.next_target()
        self.rect = self.image.get_rect(center=self.pos)
        self.distance = 0
        self.shape_type = random.randint(1, 4)
        self.shape_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.event = 2
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
            self.player.add_exp(self.exp_reward)

    def next_target(self):
        if self.target < len(self.targets) - 1:
            self.target+=1
            t=self.targets[self.target]
            self.angle = -((math.atan2(t[1]-self.pos[1],t[0]-self.pos[0]))/(math.pi/180))
            self.vx,self.vy = math.cos(math.radians(self.angle)),-math.sin(math.radians(self.angle))
        else:
            damage = self.layer + 1
            self.player.health -= damage
            self.player.score = max(0, self.player.score - 50)
            self.kill()

    def speedup(self):
        print(self.distance, "trc")
        d1= math.sqrt((self.targets[self.target][0]- self.pos[0]) ** 2 + (self.targets[self.target][1]- self.pos[1]) ** 2)
        d2= math.sqrt((self.targets[self.target+1][0]- self.targets[self.target][0]) ** 2 + (self.targets[self.target+1][1]- self.targets[self.target][1]) ** 2)
        self.pos= list(self.targets[min (len(self.targets)-1, self.target+ 1)])
        self.target= self.targets.index(tuple(self.pos))
        self.next_target()
        self.distance= (d1 + d2) + self.distance
        print(self.distance, "sau")

    def hit(self,damage):
        self.player.money+=1
        self.health -= damage
        if self.health<=0:
            self.player.money+=self.cashprize
            self.nextLayer() if self.layer>0 else self.kill()

    def kill(self):
        if self in enemyList:
            enemyList.remove(self)
        self.player.score += 100
        self.player.money += self.cashprize
        self.player.add_exp(self.exp_reward)
        # Lưu tiền sau khi giết quái
        self.player.save_system.update_money(self.player.money)
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