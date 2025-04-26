# Tower Defense Game

## Giới thiệu
Game phòng thủ tháp với cơ chế vẽ hình độc đáo để tiêu diệt kẻ địch. Người chơi phải vẽ các hình khác nhau tương ứng với biểu tượng trên kẻ địch để tiêu diệt chúng.

## Thư viện và Công nghệ sử dụng

### Thư viện chính

1. **Pygame (Game Development)**
   - Mục đích: Framework chính để phát triển game 2D
   - Các module chính:
     - `pygame.display`:
       + Quản lý cửa sổ game và chế độ hiển thị
       + Thiết lập độ phân giải màn hình (800x600)
       + Cập nhật và vẽ frame game

       Ví dụ:
       ```python
       # Khởi tạo màn hình game
       pygame.init()
       screen = pygame.display.set_mode((800, 600))
       pygame.display.set_caption('Tower Defense Game')
       
       # Cập nhật màn hình
       pygame.display.flip()
       
       # Giới hạn FPS
       clock = pygame.time.Clock()
       clock.tick(60)
       ```
     
     - `pygame.mixer`:
       + Xử lý âm thanh đa kênh
       + Phát nhạc nền (maintheme.mp3)
       + Phát hiệu ứng âm thanh (pop.mp3, explosion.wav)
       + Điều chỉnh âm lượng riêng cho nhạc và sound effects

       Ví dụ:
       ```python
       # Khởi tạo âm thanh
       pygame.mixer.init()
       
       # Phát nhạc nền
       pygame.mixer.music.load('music/maintheme.mp3')
       pygame.mixer.music.set_volume(0.65)
       pygame.mixer.music.play(-1)  # -1 để lặp vô hạn
       
       # Phát hiệu ứng âm thanh
       sound = pygame.mixer.Sound('sounds/pop3.mp3')
       sound.set_volume(0.3)
       sound.play()
       ```
     
     - `pygame.font`:
       + Render text với nhiều font khác nhau
       + Hỗ trợ hiển thị điểm số, thông báo
       + Tùy chỉnh màu sắc và kích thước chữ

       Ví dụ:
       ```python
       # Tạo font chữ
       font = pygame.font.Font(None, 36)  # None = font mặc định, size 36
       font_bold = pygame.font.SysFont('arial', 22, bold=True)
       
       # Render text
       text = font.render(f"Score: {score}", True, (255, 255, 255))
       screen.blit(text, (10, 10))  # Vẽ text lên màn hình
       ```
     
     - `pygame.Surface`:
       + Xử lý và vẽ đồ họa 2D
       + Tạo surface cho việc vẽ hình
       + Xử lý alpha và độ trong suốt
       + Blend và transform hình ảnh

       Ví dụ:
       ```python
       # Tạo surface cho việc vẽ
       surface = pygame.Surface((800, 600))
       surface.set_colorkey((0, 0, 0))  # Màu trong suốt
       
       # Vẽ hình và blend
       pygame.draw.circle(surface, (255, 0, 0), (100, 100), 50)
       pygame.draw.rect(surface, (0, 255, 0), (200, 200, 50, 50))
       
       # Set alpha và blend mode
       surface.set_alpha(128)  # 0-255
       surface.set_colorkey((0, 0, 0))  # Màu trong suốt
       ```
     
     - `pygame.Rect`:
       + Xử lý va chạm giữa các đối tượng
       + Kiểm tra vị trí chuột với buttons
       + Xác định vùng hit-box cho enemies

       Ví dụ:
       ```python
       # Tạo rect và kiểm tra va chạm
       rect1 = pygame.Rect(100, 100, 50, 50)
       rect2 = pygame.Rect(120, 120, 50, 50)
       
       # Kiểm tra va chạm
       if rect1.colliderect(rect2):
           print("Có va chạm!")
           
       # Kiểm tra điểm nằm trong rect
       mouse_pos = pygame.mouse.get_pos()
       if rect1.collidepoint(mouse_pos):
           print("Chuột đang trong rect!")
       ```
     
     - `pygame.event`:
       + Xử lý input từ bàn phím và chuột
       + Quản lý các sự kiện game
       + Timer và custom events

       Ví dụ:
       ```python
       # Xử lý các sự kiện
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               pygame.quit()
               sys.exit()
           
           elif event.type == pygame.MOUSEBUTTONDOWN:
               if event.button == 1:  # Chuột trái
                   start_drawing(event.pos)
                   
           elif event.type == pygame.KEYDOWN:
               if event.key == pygame.K_SPACE:
                   start_wave()
               elif event.key == pygame.K_h:
                   buy_hail()
       ```

2. **OpenCV (Computer Vision - cv2)**
   - Mục đích: Thư viện xử lý ảnh và nhận diện hình vẽ
   - Các chức năng chính:
     - Xử lý ảnh:
       + Chuyển đổi không gian màu (RGB sang BGR, grayscale)
       + Threshold và binary image processing
       + Làm mịn và lọc nhiễu
     - Nhận diện hình vẽ:
       + Phát hiện cạnh với Canny Edge Detection
       + Tìm contours của hình vẽ
       + Phân tích hình dạng geometry
     - Xử lý contour:
       + Tính diện tích và chu vi
       + Xác định hướng và góc
       + Đơn giản hóa đường nét

   Ví dụ:
   ```python
   # Xử lý ảnh từ Pygame Surface
   img = pygame.surfarray.array3d(surface)
   img = numpy.transpose(img, (1, 0, 2))
   img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
   gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
   
   # Threshold và tìm contour
   _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)
   contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
   
   # Phân tích hình dạng
   for contour in contours:
       # Tính diện tích và chu vi
       area = cv2.contourArea(contour)
       perimeter = cv2.arcLength(contour, True)
       
       # Xấp xỉ đa giác
       approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)
       
       # Nhận diện hình dạng
       if len(approx) == 2:
           shape = "line"
       elif len(approx) == 3:
           shape = "triangle"
       elif len(approx) == 4:
           shape = "rectangle"
       else:
           shape = "circle"
   ```

3. **NumPy (Numerical Python)**
   - Mục đích: Thư viện tính toán số học và xử lý mảng/ma trận
   - Các chức năng sử dụng:
     - Xử lý ma trận:
       + Chuyển đổi pygame Surface thành ndarray
       + Ma trận hóa hình ảnh để xử lý
       + Phép toán ma trận cho xử lý ảnh
     - Tính toán vector:
       + Tính toán khoảng cách và góc
       + Xử lý chuyển động của đối tượng
       + Vector hóa các phép tính
     - Tối ưu hóa:
       + Tăng tốc các phép tính số học
       + Xử lý dữ liệu song song
       + Tối ưu bộ nhớ

   Ví dụ:
   ```python
   # Chuyển đổi Pygame Surface thành ndarray
   surface_array = pygame.surfarray.array3d(surface)
   
   # Xử lý ma trận
   rotated = numpy.rot90(surface_array)  # Xoay 90 độ
   flipped = numpy.fliplr(surface_array)  # Lật ngang
   
   # Tính toán khoảng cách
   def calculate_distance(point1, point2):
       return numpy.sqrt(numpy.sum((numpy.array(point1) - numpy.array(point2)) ** 2))
   
   # Vector hóa các phép tính
   positions = numpy.array([(x1, y1), (x2, y2), (x3, y3)])
   target = numpy.array([target_x, target_y])
   distances = numpy.linalg.norm(positions - target, axis=1)
   closest_index = numpy.argmin(distances)
   ```

4. **Các thư viện hỗ trợ khác**
   - **OS**: 
     ```python
     # Quản lý đường dẫn
     game_dir = os.path.dirname(os.path.abspath(__file__))
     image_path = os.path.join(game_dir, 'images', 'sprite.png')
     
     # Kiểm tra và tạo thư mục
     save_dir = 'saves'
     if not os.path.exists(save_dir):
         os.makedirs(save_dir)
     ```
   
   - **JSON**:
     ```python
     # Lưu game
     save_data = {
         'player': {'health': 100, 'money': 1000},
         'wave': current_wave,
         'achievements': unlocked_achievements
     }
     with open('game_save.json', 'w') as f:
         json.dump(save_data, f)
     
     # Đọc cài đặt
     with open('settings.json', 'r') as f:
         settings = json.load(f)
         sound_volume = settings.get('sound_volume', 0.5)
     ```

### Cấu trúc thư mục
```
gamepython/
├── source/           # Mã nguồn chính
├── images/          # Hình ảnh game
├── sounds/          # Âm thanh game
├── music/           # Nhạc nền
├── maps/            # Dữ liệu bản đồ
├── background/      # Hình nền
└── settings.json    # Cấu hình game
```

## Các tính năng chính

### 1. Hệ thống âm thanh (SoundManager)
- Quản lý âm thanh và nhạc nền
- Lưu và tải cài đặt âm thanh
- Điều chỉnh volume và bật/tắt nhạc

### 2. Hệ thống thành tích (AchievementSystem)
- Theo dõi và cập nhật thành tích người chơi
- Hiển thị thông báo khi đạt thành tích
- Lưu trữ tiến độ thành tích

### 3. Hệ thống Shop
- Mua các nâng cấp sức mạnh
- Sử dụng tiền kiếm được trong game
- Lưu trữ các item đã mua

### 4. Hệ thống lưu trữ (SaveSystem)
- Lưu và tải tiến độ game
- Lưu cài đặt người chơi
- Quản lý dữ liệu thành tích và shop

## Cách chơi
1. Di chuyển chuột để vẽ hình
2. Vẽ hình tương ứng với biểu tượng trên kẻ địch
3. Sử dụng phím SPACE để bắt đầu wave mới
4. Phím H để mua thiên thạch (giá 2000)
5. Bảo vệ không để kẻ địch đi qua

## Yêu cầu hệ thống
- Python 3.x
- Pygame
- OpenCV-Python
- NumPy

## Cài đặt và Chạy
1. Cài đặt các thư viện:
```bash
pip install pygame==2.5.2
pip install opencv-python==4.8.1.78
pip install numpy==1.26.3
```

2. Chạy game:
```bash
python main.py
```

## Credits
- Âm thanh và nhạc: `music/` và `sounds/`
- Đồ họa: `images/` và `background/`
- Font chữ: Mặc định của hệ thống

# Chi Tiết Triển Khai Code

## 1. Cấu Trúc Core Classes

### Enemy Class
```python
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
```

Chức năng chính:
- Quản lý các loại enemy với thuộc tính khác nhau (máu, tốc độ, phần thưởng)
- Xử lý di chuyển theo đường đi định sẵn
- Hệ thống thanh máu và hiệu ứng hit
- Random các hình dạng để người chơi vẽ
- Xử lý va chạm và tiêu diệt

### Player Class
```python
class Player:
    def __init__(self):
        self.save_system = SaveSystem()
        self.shop_system = ShopSystem()
        self.health = self.shop_system.get_total_health()
        self.money = self.save_system.get_money() 
        self.score = 0
        self.level = 1
        self.exp = 0
        self.exp_to_next_level = 1000
        self.wave = 1
```

Chức năng chính:
- Quản lý thông tin người chơi (máu, tiền, điểm, level)
- Hệ thống level up và kinh nghiệm
- Tương tác với shop system
- Lưu và tải dữ liệu game

### Wave System (class Sender)
```python
class Sender:
    def __init__(self,wave, player, mapvar):
        self.wave = wave
        self.timer = 0
        self.rate = 1  # Tốc độ spawn enemy
        self.enemies = []
        # Parse wave data từ file
        enemies = mapvar.waves[wave-1].split(',')
        for enemy in enemies:
            amount,layer = enemy.split('*')
            self.enemies += [eval(layer)-1]*eval(amount)
```

Chức năng chính:
- Quản lý việc spawn enemy theo wave
- Đọc dữ liệu wave từ file cấu hình
- Tính toán phần thưởng sau mỗi wave
- Điều chỉnh độ khó theo tiến trình

## 2. Game Mechanics

### Hệ Thống Vẽ Hình
```python
def check_collision_with_enemies(drawn_shape, surface_temp, screen, check, rdm):
    # Chuyển surface thành matrix để xử lý
    img = pygame.surfarray.array3d(surface_temp)
    img = numpy.transpose(img, (1, 0, 2))
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Nhận diện contour
    _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
```

Các hình dạng có thể vẽ:
- Horizontal (gạch ngang) 
- Vertical (gạch dọc)
- Diagonal (gạch chéo)
- V-shape (hình chữ V)
- Circle (hình tròn)

### Hệ Thống Combat
- Enemy có các layer khác nhau, mỗi hit sẽ giảm 1 layer
- Vẽ đúng hình sẽ gây sát thương cho enemy tương ứng
- Thiên thạch (Hail) có thể được mua để gây sát thương diện rộng
- Hiệu ứng nổ và particle khi enemy bị tiêu diệt

### Shop System
```python
class ShopSystem:
    def __init__(self):
        self.items = {
            'health_1': {'name': 'Tang 1 Mau', 'cost': 1000, 'bought': 0},
            'health_2': {'name': 'Tang 2 Mau', 'cost': 1900, 'bought': 0},
            'health_3': {'name': 'Tang 3 Mau', 'cost': 2700, 'bought': 0}
        }
```
- Mua các nâng cấp máu
- Mua thiên thạch (2000 tiền)
- Lưu trạng thái đã mua

## 3. Audio System
```python
class SoundManager:
    def __init__(self):
        self.music_enabled = True
        self.music_volume = 0.65
        self.sound_volume = 0.5
        
    def play_sound(self, file, volume=None):
        if not self.music_enabled: return
        sound = pygame.mixer.Sound(file)
        sound.set_volume(volume if volume else self.sound_volume)
        sound.play()
```

Âm thanh trong game:
- Nhạc nền (maintheme.mp3)
- Tiêu diệt enemy (pop.mp3)
- Mua item (buy.mp3) 
- Game over (gameover2.wav)

## 4. Save System
```python
class SaveSystem:
    def __init__(self):
        self.save_file = 'game_save.json'
        self.default_data = {
            'money': 0,
            'achievements': {...},
            'shop_items': {...}
        }
```

Dữ liệu được lưu:
- Tiền của người chơi
- Thành tích đã đạt được
- Các item đã mua trong shop
- Cài đặt âm thanh

## 5. Hệ Thống Achievement

### Thành tích có sẵn
```python
achievements = {
    'kill_100': {'name': 'SAT THU', 'desc': 'Tieu diet 100 quai', 'unlocked': False},
    'survive_10': {'name': 'KIEN NGHI', 'desc': 'Song sot 10 wave', 'unlocked': False},
    'level_10': {'name': 'HUYEN THOAI', 'desc': 'Dat level 10', 'unlocked': False},
    'money_1000': {'name': 'TY PHU', 'desc': 'Co 1000 tien', 'unlocked': False}
}
```

- Hệ thống thông báo khi đạt thành tích
- Lưu trữ tiến độ vĩnh viễn
- Phần thưởng khi đạt được thành tích

## 6. Game Flow Chi Tiết

### Game States
1. Menu State
```python
def handle_menu():
    # Hiển thị các nút:
    - START
    - SHOP 
    - HUONG DAN
    - AM THANH: BAT/TAT
    - THOAT
```

2. Game State
```python
def main_game_loop():
    # Game loop chính:
    - Xử lý input người chơi
    - Update enemy movements
    - Kiểm tra va chạm
    - Vẽ hình và render
    - Cập nhật điểm số và tiền
```

3. Shop State
```python
def shop_menu():
    # Hiển thị các item có thể mua:
    - Nâng cấp máu (Health)
    - Mua thiên thạch (Hail)
    - Hiển thị số tiền hiện có
    - Nút quay lại menu
```

4. Game Over State
```python
def game_over():
    # Hiển thị màn hình thua:
    - Điểm số cuối cùng
    - Số wave đã vượt qua
    - Nút quay lại menu chính
    - Phát nhạc game over
```

## 7. Map System

### Cấu trúc map
```python
class Map:
    def __init__(self):
        self.map = 'monkey lane'  # Tên map
        self.loadmap()  # Load dữ liệu map
        
    def loadmap(self):
        # Đọc dữ liệu từ files
        self.targets = eval(open('maps/%s/targets.txt' % self.map,'r').read())
        self.waves = eval(open('maps/%s/waves.txt' % self.map,'r').read())
```

### Các thành phần map:
1. Target Points
- Các điểm mốc enemy phải đi qua
- Được định nghĩa trong targets.txt
- Format: [(x1,y1), (x2,y2),...]

2. Wave Data
- Thông tin về các wave quái
- Được định nghĩa trong waves.txt
- Format: "số lượng*cấp độ, số lượng*cấp độ,..."

3. Background Layers
- 3 layer hình ảnh chồng lên nhau
- Tạo hiệu ứng độ sâu (parallax)
- Được load từ image.png, image2.png, image3.png

## 8. Optimization

### Performance
1. Object Pooling
```python
# Tái sử dụng object thay vì tạo mới
enemyList = []  # Pool of enemies
bulletList = []  # Pool of bullets
explosionList = []  # Pool of effects
```

2. Surface Caching
```python
# Cache các surface thường xuyên sử dụng
background = pygame.Surface((800,600))
background.set_colorkey((0,0,0))
```

3. Draw Call Optimization
```python
# Nhóm các đối tượng theo độ sâu để vẽ
z0,z1 = [],[]  # Z-ordering lists
for enemy in enemyList:
    if enemy.distance > threshold:
        z0.append(enemy)
    else:
        z1.append(enemy)
```

### Memory Management
- Giải phóng surface không sử dụng
- Xóa enemy/bullet/effect khi không cần thiết
- Tối ưu hóa kích thước texture

## 9. Điều Khiển

### Keyboard Controls
- SPACE: Bắt đầu wave mới
- W: Tăng tốc độ game
- S: Giảm tốc độ game
- H: Mua thiên thạch (2000 gold)
- ESC: Quay lại menu/thoát

### Mouse Controls
- Chuột trái: Vẽ hình
- Click vào nút: Tương tác với menu/UI
- Di chuyển: Vẽ đường

## 10. Config Files

### settings.json
```json
{
    "music_enabled": true,
    "music_volume": 0.65,
    "sound_volume": 0.5
}
```

### game_save.json
```json
{
    "money": 1000,
    "achievements": {...},
    "shop_items": {...},
    "last_save": "2025-04-26T10:30:00"
}
```

## 11. Debug và Error Handling

### Debug System
```python
def debug_info(screen):
    # Hiển thị thông tin debug
    debug_text = [
        f"FPS: {clock.get_fps():.1f}",
        f"Enemies: {len(enemyList)}",
        f"Wave: {wave}",
        f"Memory: {get_memory_usage()}MB"
    ]
```

### Error Handling
```python
try:
    pygame.mixer.init()
    sound_initialized = True
except Exception as e:
    print(f"Không thể khởi tạo âm thanh: {str(e)}")
    sound_initialized = False
```

### Log System
- Log lỗi vào file
- Log các sự kiện quan trọng
- Thông tin debug khi cần

## 12. Testing

### Unit Tests
- Test các component riêng lẻ
- Kiểm tra logic game
- Validate input/output

### Integration Tests
- Test tương tác giữa các hệ thống
- Kiểm tra game flow
- Verify save/load system

### Performance Tests
- Test FPS và độ trễ
- Memory leaks check
- Load testing với nhiều enemy