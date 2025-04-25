import pygame
# from moviepy.editor import VideoFileClip
import random
import sys


# Khởi tạo Pygame
pygame.init()

# Kích thước màn hình
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tower Defense Intro")

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Tải hình ảnh (tải trước các ảnh game và nhân vật của bạn)
intro_image = pygame.image.load('Welcome.jpg')
knight_image = pygame.image.load('Knight.jpg')
game_screen_image = knight_image
loading_story_image = pygame.image.load("Loading Tower Defense.png")


#Âm thanh
bg_music = pygame.mixer.music.load('Gunny2.mp3')
pygame.mixer.music.play(-1, 0.0)

# Thời gian
FPS = 60
clock = pygame.time.Clock()

# Hàm vẽ màn hình chính
def draw_main_scene():
    screen.fill(WHITE)
    scaled_intro = pygame.transform.scale(intro_image, (WIDTH, HEIGHT))
    screen.blit(scaled_intro, (0, 0))

    font = pygame.font.Font(None, 48)
    message = "Thank you for working! Relax with the game!"

    # Tạo surface chữ riêng để chỉnh alpha
    text_surface = font.render(message, True, WHITE).convert_alpha()
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 200))

    # Hiệu ứng fade-in
    for alpha in range(0, 256, 5):  # Tăng alpha từ 0 đến 255
        screen.blit(scaled_intro, (0, 0))  # Vẽ lại nền mỗi frame
        text_surface.set_alpha(alpha)
        screen.blit(text_surface, text_rect)
        pygame.display.flip()
        pygame.time.delay(30)  # Delay cho mượt

    pygame.time.delay(2000)  # Sau khi fade-in xong, giữ lại 2 giây

# Hàm vẽ màn hình game
def draw_game_scene():
    screen.fill(WHITE)
    scaled_knight = pygame.transform.scale(knight_image, (WIDTH, HEIGHT))
    screen.blit(scaled_knight, (0, 0))
    pygame.display.flip()
    pygame.time.delay(6000)  # Giữ ảnh Knight trong 5 giây
#Thanh loading
def draw_loading_bar(duration= 6000):
    bar_width = 600
    bar_height = 30
    bar_x = (WIDTH - bar_width) // 2
    bar_y = HEIGHT - 100

    font = pygame.font.Font(None, 32)
    start_time = pygame.time.get_ticks()

    # Âm thanh tick
    tick_sound = pygame.mixer.Sound("Sword Sound Effect.mp3")
    tick_milestones = [0.25, 0.5, 0.75, 1.0]
    tick_played = [False] * len(tick_milestones)

    while True:
        current_time = pygame.time.get_ticks()
        elapsed = current_time - start_time
        progress = min(elapsed / duration, 1)  # từ 0.0 đến 1.0

        # Phát tick sound mỗi mốc
        for i, milestone in enumerate(tick_milestones):
            if not tick_played[i] and progress >= milestone:
                tick_sound.play()
                tick_played[i] = True

        # Knight mờ dần theo progress
        knight_alpha = max(255 - int(progress * 255), 0)
        scaled_knight = pygame.transform.scale(knight_image, (WIDTH, HEIGHT)).convert_alpha()
        scaled_knight.set_alpha(knight_alpha)

        # Vẽ nền knight
        screen.fill(WHITE)
        screen.blit(scaled_knight, (0, 0))

        # Vẽ thanh loading gradient/glow
        for i in range(int(bar_width * progress)):
            color_intensity = 155 + int(100 * (i / bar_width))
            color = (color_intensity, 50, 255)  # tím xanh sci-fi
            pygame.draw.line(screen, color, (bar_x + i, bar_y + 2), (bar_x + i, bar_y + bar_height - 2))

        # Glow effect (light blur outer line)
        pygame.draw.rect(screen, (100, 0, 255), (bar_x - 2, bar_y - 2, bar_width + 4, bar_height + 4), 2)

        # Viền loading
        pygame.draw.rect(screen, (0, 0, 0), (bar_x, bar_y, bar_width, bar_height), 2)

        # Text %
        percent_text = font.render(f"{int(progress * 100)}%", True, WHITE)
        text_rect = percent_text.get_rect(center=(WIDTH // 2, bar_y + bar_height // 2))
        screen.blit(percent_text, text_rect)

        pygame.display.flip()
        clock.tick(FPS)

        if elapsed >= duration:
            break
pass
#Loading game ảnh chuyển về cốt truyện
def flash_loading_image(duration=5000):
    start_time = pygame.time.get_ticks()

    # Chuẩn bị ảnh với alpha
    scaled_image = pygame.transform.scale(loading_story_image, (WIDTH, HEIGHT)).convert_alpha()

    alpha = 255
    fade_direction = -5  # Mờ dần

    while pygame.time.get_ticks() - start_time < duration:
        screen.fill(BLACK)

        alpha += fade_direction
        if alpha <= 100 or alpha >= 255:
            fade_direction *= -1  # Đảo chiều mờ/rõ

        # Clamp alpha trong khoảng [100, 255]
        alpha = max(100, min(255, alpha))

        scaled_image.set_alpha(alpha)
        screen.blit(scaled_image, (0, 0))
        pygame.display.flip()
        pygame.time.delay(30)
# Hoạt ảnh bị hút vào game
def suck_into_game_effect():
    for i in range(10):
        screen.fill(WHITE)
        pygame.draw.circle(screen, (255, 255, 255), (WIDTH // 2, HEIGHT // 2), i * 15)
        pygame.draw.circle(screen, (0, 0, 0), (WIDTH // 2, HEIGHT // 2), i * 10)
        pygame.display.flip()
        pygame.time.delay(50)


# Vẽ nhân vật
def draw_character(x, y):
    pygame.display.flip()

# Màn hình intro ảnh và chữ động
def show_intro_screen():
    font = pygame.font.Font(None, 48)
    messages = [
        "Tower Defense Adventure Begins!",
        "Welcome to Tower Defense Adventure!"
    ]
    text_color = (255, 255, 255)
    text_pos_y = [HEIGHT -100 , HEIGHT -100]  # hai dòng, cách nhau chút

    # Resize ảnh intro vừa màn hình
    scaled_intro = pygame.transform.scale(intro_image, (WIDTH, HEIGHT))

    for msg_index, message in enumerate(messages):
        displayed_text = ""

        for i in range(len(message)):
            screen.blit(scaled_intro, (0, 0))

            displayed_text += message[i]
            text_surface = font.render(displayed_text, True, text_color)
            text_rect = text_surface.get_rect(center=(WIDTH // 2, text_pos_y[msg_index]))
            screen.blit(text_surface, text_rect)

            pygame.display.flip()
            pygame.time.delay(100)

        pygame.time.delay(1500)  # Đợi 1 giây trước khi dòng kế tiếp
# Gọi video bằng thư viện python
def play_story_video():
    pygame.mixer.music.stop()  # Ngừng nhạc nền trước khi phát video
    video_path = "Video_intro.mp4"  # ← Thay bằng tên video thật
    clip = VideoFileClip(video_path)
    clip.preview()
    clip.close()

# Chạy video intro
def main():
    character_x, character_y = WIDTH // 2 - 50, HEIGHT - 150

    show_intro_screen()  # <-- GỌI INTRO ẢNH + CHỮ ĐỘNG

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        draw_main_scene()
        pygame.time.delay(2000)
        
        suck_into_game_effect()

        draw_loading_bar()  # <-- THÊM THANH LOADING Ở ĐÂY
        flash_loading_image()  # <-- CHUYỂN QUA HÌNH LOADING NHẤP NHÁY
        draw_game_scene()
        play_story_video() 

        for i in range(5):
            character_y -= 10
            draw_character(character_x, character_y)
            pygame.time.delay(100)

        pygame.time.delay(2000)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()
