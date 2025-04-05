import pygame, sys, os, time, math, random, cv2, numpy
sys.path.append('source')
from player import Player
from map import Map
from enemy import Enemy
from setting import *
from sender import Sender
from menu import Menu
from gameover import GameOver
from explosion import Explosion
from achievements import AchievementSystem  # Thêm import
from features import ShopSystem
from save_system import SaveSystem
from hail import Hail

player = Player()
mapvar = Map()
# store images using a dictionary 
EnemyImageArray = dict()

def buy_hail():
    hail_cost = 100  # Chi phí để mua một thiên thạch
    if player.money >= hail_cost:
        player.money -= hail_cost
        player.save_system.update_money(player.money)  # Lưu tiền sau khi mua
        spawn_hail()
        return True
    return False

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

def workEvents(selected, wave, speed, pos, drawing):
    buy= False
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
                if wave<=len(mapvar.waves): Sender(wave, player, mapvar)
                else: print('Congratulations!! You survived the swarm')
            if event.key == pygame.K_w and speed<10: speed+=1
            if event.key == pygame.K_s and speed>1: speed-=1
            if event.key == pygame.K_h and buy == False:  # Thêm phím tắt H để mua thiên thạch
                buy = True
            if event.key == pygame.K_h and buy== True:
                if buy_hail():
                    buy = True
                    print("Da mua thien thach thanh cong!")
                    try:
                        play_sound('sounds/buy.mp3', 0.3)
                    except:
                        print("Khong tim thay file am thanh")
                else:
                    print("Khong du tien de mua thien thach!")
        
        # if event.type == SPAWN_HAIL:
        #     spawn_hail()

    return selected,wave,speed, pos, drawing

def spawn_hail():
        for i in range(20):
            pos = (random.randint(0, screenWidth), random.randint(0, screenHeight))
            hail = Hail(pos[0], pos[1])
            hailList.append(hail)

        # Phát âm thanh khi hỏa cầu xuất hiện
        try:
            play_sound('sounds/Fire.wav', 1 )
        except:
            print("Không tìm thấy file âm thanh ")

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


def main():
    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.display.set_caption('Bloons Tower Defence')
    screen = pygame.display.set_mode((screenWidth,screenHeight))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None,20)

    # Khởi tạo các hệ thống
    achievement_system = AchievementSystem()
    shop_system = ShopSystem()
    
    # Khởi tạo player sau khi pygame đã được khởi tạo
    global player
    player = Player()
    
    # Add this line to load enemy images
    loadImages()
    
    mapvar.getmovelist()

    drawing= False
    pos=[]
    spawn= pygame.time.get_ticks()
    index_to_draw = 0

    menu = Menu(player)
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
                        # Cập nhật tiền trước khi vào shop
                        player.money = player.save_system.get_money()
                        game_state = "shop"
                    elif button_clicked == 2:
                        game_state = "instructions"
                    elif button_clicked == 3:
                        pygame.quit()
                        sys.exit()

            menu.draw(screen, pygame.mouse.get_pos())
            pygame.display.flip()
            clock.tick(fps)

        elif game_state == "shop":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_state = "menu"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    y_offset = 200
                    for item_id, item in shop_system.items.items():
                        item_rect = pygame.Rect(screen.get_width() // 4, y_offset, screen.get_width() // 2, 80)
                        buy_rect = pygame.Rect(item_rect.right - 100, item_rect.centery - 20, 80, 40)
                        
                        if buy_rect.collidepoint(mouse_pos):
                            if player.money >= item['cost']:
                                if shop_system.buy_item(item_id, player):
                                    try:
                                        play_sound('sounds/buy.mp3', 0.3)
                                    except:
                                        print("Khong tim thay file am thanh")
                                    print(f"Da mua {item['name']}")
                            else:
                                print("Khong du tien de mua!")
                        y_offset += 100

            screen.fill((0, 0, 0))
            shop_system.draw_shop(screen)
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

            if senderList: 
                wave = senderList[0].update(frametime,wave)
                player.wave = wave  # Cập nhật wave cho player

            # Kiểm tra thành tích
            achievement_system.check_achievements(player)

            # Cập nhật tiền
            player.update_money(player.money)

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
            cloud_image = pygame.image.load("images/mud.png")
            cloud_image= pygame.transform.scale(cloud_image, (screenWidth, screenHeight))
            if draw_cloud()== True:
                screen.blit(cloud_image, (0, 0))
                for enemy in enemyList[:]:
                    enemy.move(frametime)
                pygame.display.flip()

            # Vẽ thông báo thành tích
            achievement_system.draw_notifications(screen)
            
            # Vẽ tiến độ thành tích
            achievement_system.draw_progress(screen)

            print(len(hailList))

            current = pygame.time.get_ticks()
            if current - spawn > 3000:
                if index_to_draw < min(5, len(hailList)):
                    spawn = current
                    index_to_draw += 1  # mỗi 3s cho phép vẽ thêm 5 hail

            # Vẽ các hail được phép vẽ ra
            for i in range(min(index_to_draw, len(hailList))):
                    hailList[i].move(screen)
                    hailList[i].draw(screen)
            for hail in hailList[:]:
                if hail.x== hail.target[0] and hail.y==hail.target[1]:
                    hailList.remove(hail)
                    explosionList.append(Explosion(hail.x, hail.y))

            for hail in hailList[:]:
                if hail.x != 0 and hail.y != 0:
                    for enemy in enemyList[:]:
                        if enemy.rect.colliderect(hail.rect):
                            enemy.kill()
                            if (hail in hailList): 
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
                        player.health = shop_system.get_total_health()
                        player.money = player.save_system.get_money()
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