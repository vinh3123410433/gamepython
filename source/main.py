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
from achievements import AchievementSystem
from features import ShopSystem
from save_system import SaveSystem
from hail import Hail
from sound_button import SoundButton
from hud import GameplayHUD, PauseModal, TutorialScreen

player = Player()
mapvar = Map()
EnemyImageArray = dict()

def buy_hail():
    hail_cost = 2000  # Chi phí để mua một thiên thạch
    if player.money >= hail_cost:
        player.money -= hail_cost
        player.save_system.update_money(player.money)  # Lưu tiền sau khi mua
        spawn_hail()
        try:
            play_sound('sounds/buy.mp3', 0.4)
        except Exception:
            pass
        return True
    return False

def workEvents(selected, wave, speed, pos, drawing, pos_temp, hud):
    action = None
    mpos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            selected = None

        # Check HUD buttons on all mouse events (press-down and release click)
        if hud.btn_pause.handle_event(event):
            return selected, wave, speed, pos, drawing, pos_temp, 'pause'

        if hud.btn_sound.handle_event(event):
            sound_manager.toggle_music()
            hud.btn_sound.icon = "sound_on" if sound_manager.music_enabled else "sound_off"
            return selected, wave, speed, pos, drawing, pos_temp, None

        if hud.btn_speed_down.handle_event(event):
            speed = max(1, speed - 1)
            return selected, wave, speed, pos, drawing, pos_temp, None

        if hud.btn_speed_up.handle_event(event):
            speed = min(10, speed + 1)
            return selected, wave, speed, pos, drawing, pos_temp, None

        if hud.btn_hail.handle_event(event):
            if buy_hail():
                hud.show_feedback("horizontal")  # visual cue
            return selected, wave, speed, pos, drawing, pos_temp, None

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            # Do not start drawing if clicking inside top HUD bar or bottom dock
            top_bar_rect = pygame.Rect(8, 8, screenWidth - 16, 44)
            dock_rect = pygame.Rect(screenWidth - 270, screenHeight - 54, 262, 46)
            if top_bar_rect.collidepoint(mpos) or dock_rect.collidepoint(mpos):
                return selected, wave, speed, pos, drawing, pos_temp, None

            # Start drawing gesture
            drawing = True
            pos = [mpos, mpos]

        if event.type == pygame.MOUSEMOTION and drawing:
            if len(pos) > 0:
                last_pos = pos[-1]
                dx = mpos[0] - last_pos[0]
                dy = mpos[1] - last_pos[1]
                dist = max(abs(dx), abs(dy))
                for i in range(dist):
                    x = last_pos[0] + dx * i / dist
                    y = last_pos[1] + dy * i / dist
                    pos.append((int(x), int(y)))
                    pos_temp.append((int(x), int(y)))

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            drawing = False
            pos = []

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                action = 'pause'
            elif event.key == pygame.K_SPACE and not enemyList:
                if wave <= len(mapvar.waves):
                    Sender(wave, player, mapvar)
                    try:
                        play_sound('sounds/place tower.mp3', 0.4)
                    except Exception:
                        pass
                else:
                    action = 'victory'
            elif event.key == pygame.K_w and speed < 10:
                speed += 1
            elif event.key == pygame.K_s and speed > 1:
                speed -= 1
            elif event.key == pygame.K_h:
                buy_hail()

    return selected, wave, speed, pos, drawing, pos_temp, action

def spawn_hail():
    for i in range(20):
        pos = (random.randint(0, screenWidth), random.randint(0, screenHeight))
        hail = Hail(pos[0], pos[1])
        hailList.append(hail)

    try:
        play_sound('sounds/Fire.wav', 0.8)
    except Exception:
        pass

SPAWN_HAIL = pygame.USEREVENT + 1

def detect(surface_temp):
    img = pygame.surfarray.array3d(surface_temp)
    img = numpy.transpose(img, (1, 0, 2))
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)
    
    kernel = numpy.ones((5, 5), numpy.uint8)
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
            angle = math.degrees(math.atan2(vy.item(), vx.item()))
            
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

            current = pygame.time.get_ticks()
            countdown = (current - enemy.start) // 1000
            num = max(0, 5 - countdown)

            # Modern sleek countdown badge
            badge_r = 13
            badge_pos = (enemy.rect.centerx, enemy.rect.top - 28)
            surf = pygame.Surface((badge_r * 2, badge_r * 2), pygame.SRCALPHA)
            pygame.draw.circle(surf, (220, 38, 38, 230), (badge_r, badge_r), badge_r)
            pygame.draw.circle(surf, (255, 255, 255), (badge_r, badge_r), badge_r, width=1)
            screen.blit(surf, (badge_pos[0] - badge_r, badge_pos[1] - badge_r))

            font = pygame.font.SysFont("Arial", 14, bold=True)
            text = font.render(str(num), True, (255, 255, 255))
            screen.blit(text, text.get_rect(center=badge_pos))

            if num == 0: 
                startList.append(pygame.time.get_ticks())
                enemy.kill()

def draw_cloud():
    if len(startList) > 0:
        e = startList[0]
        current = pygame.time.get_ticks()
        countdown = max(0, (current - startList[0]) // 1000)  
        if len(startList) > 1 and startList[1] - e < 2300: 
            startList[1] = e
        if countdown < 3: 
            return True
        else: 
            startList.remove(e)
            return False
    return False

def check_collision_with_enemies(drawn_shape, surface_temp, screen, check, rdm):
    img = pygame.surfarray.array3d(surface_temp)
    img = numpy.transpose(img, (1, 0, 2))
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        for enemy in enemyList[:]:
            if enemy.shape_type == 0 and drawn_shape == "horizontal":
                if rdm == 1:
                    if check == 0:
                        if enemy.tele == 0:
                            enemy.speedup()
                            enemy.tele = 1
                        else: 
                            enemy.nextLayer()
                            if enemy.layer > -1: enemy.draw_health_bar(screen)
                else:
                    enemy.nextLayer()
                    if enemy.layer > -1: enemy.draw_health_bar(screen)
            elif enemy.shape_type == 1 and drawn_shape == "vertical":
                if rdm == 1:
                    if check == 0:
                        if enemy.tele == 0:
                            enemy.speedup()
                            enemy.tele = 1
                        else: 
                            enemy.nextLayer()
                            if enemy.layer > -1: enemy.draw_health_bar(screen)
                else:
                    enemy.nextLayer()
                    if enemy.layer > -1: enemy.draw_health_bar(screen)
            elif enemy.shape_type == 2 and drawn_shape == "diagonal_right":
                if rdm == 1:
                    if check == 0:
                        if enemy.tele == 0:
                            enemy.speedup()
                            enemy.tele = 1
                        else: 
                            enemy.nextLayer()
                            if enemy.layer > -1: enemy.draw_health_bar(screen)
                else:
                    enemy.nextLayer()
                    if enemy.layer > -1: enemy.draw_health_bar(screen)
            elif enemy.shape_type == 3 and drawn_shape == "v_shape":
                if rdm == 1:
                    if check == 0:
                        if enemy.tele == 0:
                            enemy.speedup()
                            enemy.tele = 1
                        else: 
                            enemy.nextLayer()
                            if enemy.layer > -1: enemy.draw_health_bar(screen)
                else:
                    enemy.nextLayer()
                    if enemy.layer > -1: enemy.draw_health_bar(screen)
            elif enemy.shape_type == 4 and drawn_shape == "circle":
                if rdm == 1:
                    if check == 0:
                        if enemy.tele == 0:
                            enemy.speedup()
                        else: 
                            enemy.nextLayer()
                            if enemy.layer > -1: enemy.draw_health_bar(screen)
                else:
                    enemy.nextLayer()
                    if enemy.layer > -1: enemy.draw_health_bar(screen)

def main():
    pygame.init()
    sound_initialized = False
    try:
        pygame.mixer.init()
        sound_initialized = True
    except Exception as e:
        print(f"Không thể khởi tạo âm thanh: {str(e)}")
    
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.display.set_caption('Tower Defense: Spell Rush - Modern Edition')
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    clock = pygame.time.Clock()

    # Load cài đặt âm thanh
    sound_manager.load_settings()
    
    if sound_initialized and sound_manager.music_enabled:
        try:
            play_music('music/Ruby_chan1.mp3')
        except Exception as e:
            print(f"Không thể phát nhạc: {str(e)}")

    # Khởi tạo các hệ thống
    achievement_system = AchievementSystem()
    shop_system = ShopSystem()
    
    # Khởi tạo player
    global player
    player = Player()
    
    # Load enemy images
    loadImages()
    mapvar.getmovelist()

    # UI Components
    menu = Menu(player)
    game_over = GameOver()
    hud = GameplayHUD()
    pause_modal = PauseModal()
    tutorial_screen = TutorialScreen()

    game_state = "menu"
    drawing = False
    pos = []
    spawn = pygame.time.get_ticks()
    index_to_draw = 0

    shape_correct = False
    pos_temp = []
    surface_temp = pygame.Surface((screenWidth, screenHeight)).convert_alpha()
    surface_temp.fill((0, 0, 0, 0))

    level_img, t1, t2 = mapvar.get_background()

    selected = None
    speed = 3
    wave = 1
    check = 0
    rdm = 0
    z0, z1 = [], []

    cloud_image = pygame.image.load("images/mud.png")
    cloud_image = pygame.transform.scale(cloud_image, (screenWidth, screenHeight))

    while True:
        mpos = pygame.mouse.get_pos()

        # ======================================================================
        # STATE: MAIN MENU
        # ======================================================================
        if game_state == "menu":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                btn_res = menu.handle_event(event)
                if btn_res == 0:
                    game_state = "game"
                elif btn_res == 1:
                    player.money = player.save_system.get_money()
                    game_state = "shop"
                elif btn_res == 2:
                    game_state = "instructions"
                elif btn_res == 'quit':
                    pygame.quit()
                    sys.exit()

            menu.draw(screen, mpos)
            pygame.display.flip()
            clock.tick(fps)

        # ======================================================================
        # STATE: SHOP
        # ======================================================================
        elif game_state == "shop":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    game_state = "menu"

                act = shop_system.handle_event(event, player)
                if act == 'back':
                    game_state = "menu"
                    continue

            shop_system.draw_shop(screen)
            pygame.display.flip()
            clock.tick(fps)

        # ======================================================================
        # STATE: INSTRUCTIONS / TUTORIAL
        # ======================================================================
        elif game_state == "instructions":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                act = tutorial_screen.handle_event(event)
                if act == 'back':
                    game_state = "menu"

            tutorial_screen.draw(screen, mpos)
            pygame.display.flip()
            clock.tick(fps)

        # ======================================================================
        # STATE: PAUSED
        # ======================================================================
        elif game_state == "paused":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                act = pause_modal.handle_event(event)
                if act == 'resume':
                    game_state = "game"
                elif act == 'restart':
                    # Reset current wave combat
                    enemyList.clear()
                    bulletList.clear()
                    iconList.clear()
                    senderList.clear()
                    startList.clear()
                    hailList.clear()
                    explosionList.clear()
                    game_state = "game"
                elif act == 'menu':
                    enemyList.clear()
                    bulletList.clear()
                    iconList.clear()
                    senderList.clear()
                    startList.clear()
                    hailList.clear()
                    explosionList.clear()
                    game_state = "menu"

            # Render frozen gameplay under pause overlay
            screen.blit(level_img, (0, 0))
            for enemy in z0:
                screen.blit(enemy.image, enemy.rect)
                enemy.draw_health_bar(screen)
            screen.blit(t1, (0, 0))
            screen.blit(t2, (0, 0))
            for enemy in z1:
                screen.blit(enemy.image, enemy.rect)
                enemy.draw_health_bar(screen)
            hud.draw(screen, player, wave, len(mapvar.waves), speed, False, mpos)
            pause_modal.draw(screen, mpos, player, wave)
            pygame.display.flip()
            clock.tick(fps)

        # ======================================================================
        # STATE: ACTIVE GAMEPLAY
        # ======================================================================
        elif game_state == "game":
            clock.tick(fps)
            frametime = 1 / fps * speed

            # Check Game Over (Health depleted)
            if player.health <= 0:
                game_over.reset_sound(is_victory=False)
                game_state = "game_over"
                continue

            # Draw level background
            screen.blit(level_img, (0, 0))

            # Update wave senders
            if senderList:
                wave = senderList[0].update(frametime, wave)
                player.wave = wave

            # Check Victory (Surviving all waves)
            if wave > len(mapvar.waves) and not enemyList and not senderList:
                game_over.reset_sound(is_victory=True)
                game_state = "game_over"
                continue

            # Check achievements & save money
            achievement_system.check_achievements(player)
            player.update_money(player.money)

            # Sort enemies by depth/distance along path
            z0, z1 = [], []
            for enemy in enemyList:
                d = enemy.distance
                if (915 < d < 1115) or (2800 < d < 3065):
                    z0.append(enemy)
                else:
                    z1.append(enemy)

            for enemy in z0:
                enemy.move(frametime)
                screen.blit(enemy.image, enemy.rect)
                enemy.draw_health_bar(screen)

            screen.blit(t1, (0, 0))
            screen.blit(t2, (0, 0))

            for enemy in z1:
                enemy.move(frametime)
                screen.blit(enemy.image, enemy.rect)
                enemy.draw_health_bar(screen)

            # Handle gameplay input & buttons
            selected, wave, speed, pos, drawing, pos_temp, action = workEvents(
                selected, wave, speed, pos, drawing, pos_temp, hud
            )

            if action == 'pause':
                game_state = "paused"
                continue
            elif action == 'victory':
                game_over.reset_sound(is_victory=True)
                game_state = "game_over"
                continue

            # Draw magic gesture trail while drawing
            if len(pos_temp) > 2 and drawing:
                hud.draw_magic_trail(screen, pos)
                # Keep high-contrast strokes on surface_temp for OpenCV contour analysis
                pygame.draw.lines(surface_temp, (22, 62, 80), False, pos_temp, 8)

            # Gesture Recognition
            if len(pos_temp) > 10 and not drawing:
                shape_detected = detect(surface_temp)

                if shape_detected:
                    check_collision_with_enemies(shape_detected, surface_temp, screen, check, rdm)
                    hud.show_feedback(shape_detected)
                    shape_correct = True
                    try:
                        play_sound('sounds/pop2.mp3', 0.4)
                    except Exception:
                        pass
                else:
                    rdm = random.randint(1, 5)
                    check = 0

                surface_temp = pygame.Surface((screenWidth, screenHeight)).convert_alpha()
                surface_temp.fill((0, 0, 0, 0))
                pos_temp = []
                shape_correct = False

            # Enemy special countdown events
            event_enemy(screen)

            # Mud / Smoke cloud overlay
            if draw_cloud():
                screen.blit(cloud_image, (0, 0))

            # Modern Top HUD & Bottom Dock
            is_combat_active = (len(senderList) > 0 or len(enemyList) > 0)
            hud.draw(screen, player, wave, len(mapvar.waves), speed, is_combat_active, mpos)

            # Achievements toast notifications & progress bar
            achievement_system.draw_notifications(screen)
            achievement_system.draw_progress(screen)

            # Hail / Meteor Shower Updates
            current_time = pygame.time.get_ticks()
            if current_time - spawn > 3000:
                if index_to_draw < min(5, len(hailList)):
                    spawn = current_time
                    index_to_draw += 1

            for i in range(min(index_to_draw, len(hailList))):
                hailList[i].move(screen)
                hailList[i].draw(screen)

            for hail in hailList[:]:
                if hail.x == hail.target[0] and hail.y == hail.target[1]:
                    hailList.remove(hail)
                    explosionList.append(Explosion(hail.x, hail.y))

            for hail in hailList[:]:
                if hail.x != 0 and hail.y != 0:
                    for enemy in enemyList[:]:
                        if enemy.rect.colliderect(hail.rect):
                            enemy.nextLayer()
                            if hail in hailList:
                                hailList.remove(hail)
                                explosionList.append(Explosion(enemy.rect.centerx, enemy.rect.centery))

            for explosion in explosionList[:]:
                explosion.draw(screen)
                if explosion.is_done():
                    explosionList.remove(explosion)

            pygame.display.flip()

        # ======================================================================
        # STATE: GAME OVER / VICTORY SCREEN
        # ======================================================================
        elif game_state == "game_over":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if game_over.handle_event(event):
                        # Reset game state
                        player.health = shop_system.get_total_health()
                        player.money = player.save_system.get_money()
                        player.score = 0
                        player.level = 1
                        player.exp = 0
                        player.exp_to_next_level = 1000
                        wave = 1
                        enemyList.clear()
                        bulletList.clear()
                        iconList.clear()
                        senderList.clear()
                        startList.clear()
                        hailList.clear()
                        explosionList.clear()
                        
                        # Restart background music
                        if sound_manager.music_enabled:
                            try:
                                play_music('music/Ruby_chan1.mp3')
                            except Exception:
                                pass
                        game_state = "menu"

            game_over.draw(screen, mpos, player)
            pygame.display.flip()
            clock.tick(fps)

if __name__ == '__main__':
    main()
