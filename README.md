# Tower Defense Game

Một game Tower Defense được phát triển bằng Python và Pygame, lấy cảm hứng từ Bloons Tower Defense.

## Mục Lục
1. [Giới Thiệu](#giới-thiệu)
2. [Tính Năng Chính](#tính-năng-chính)
3. [Cài Đặt](#cài-đặt)
4. [Cách Chơi](#cách-chơi)
5. [Hệ Thống Thành Tích](#hệ-thống-thành-tích)
6. [Hệ Thống Shop](#hệ-thống-shop)
7. [Yêu Cầu Hệ Thống](#yêu-cầu-hệ-thống)
8. [Tác Giả](#tác-giả)
9. [Giấy Phép](#giấy-phép)

## Giới Thiệu

Đây là một game Tower Defense được phát triển bằng Python và Pygame. Game lấy cảm hứng từ Bloons Tower Defense với nhiều tính năng độc đáo và thú vị.

### Mục Tiêu Dự Án
- Tạo ra một game Tower Defense hấp dẫn và thách thức
- Áp dụng các kỹ thuật lập trình hiện đại
- Xây dựng giao diện người dùng trực quan
- Tối ưu hóa hiệu suất và trải nghiệm người dùng

### Đối Tượng Sử Dụng
- Người chơi yêu thích thể loại Tower Defense
- Nhà phát triển muốn học hỏi về lập trình game
- Giáo viên và học sinh trong lĩnh vực lập trình

## Tính Năng Chính

- Hệ thống wave quái vật với độ khó tăng dần
- Hệ thống vẽ hình để tiêu diệt quái vật
- Hệ thống shop để mua sức khỏe và các power-up
- Hệ thống thành tích (Achievements)
- Hệ thống âm thanh và nhạc nền
- Hệ thống lưu game
- Hệ thống level và kinh nghiệm
- Hệ thống thiên thạch (Hail) để hỗ trợ tiêu diệt quái vật

## Cài Đặt

### Yêu Cầu Hệ Thống
- Python 3.x
- Pygame
- Các thư viện phụ thuộc khác (numpy, cv2)

### Cài Đặt Môi Trường
1. Clone repository:
```bash
git clone [URL_REPOSITORY]
cd gamepython
```

2. Cài đặt các thư viện cần thiết:
```bash
pip install pygame numpy opencv-python
```

## Cách Chơi

1. Chạy game:
```bash
python source/main.py
```

2. Điều khiển:
- SPACE: Bắt đầu wave quái vật
- W: Tăng tốc độ game
- S: Giảm tốc độ game
- H: Mua thiên thạch (chi phí: 2000 tiền)
- ESC: Quay lại menu

3. Mục tiêu:
- Tiêu diệt quái vật để nhận tiền
- Bảo vệ căn cứ không để quái vật đi qua
- Vẽ hình tương ứng với ký hiệu trên quái vật để tiêu diệt chúng
- Nâng cấp sức khỏe và mua power-up từ shop

## Hệ Thống Thành Tích

- Tiêu diệt 100 quái vật
- Sống sót qua 10 wave
- Đạt level 10
- Kiếm được 1000 tiền

## Hệ Thống Shop

- Mua sức khỏe
- Mua thiên thạch
- Các power-up khác

## Cấu Trúc Dự Án

```
gamepython/
├── source/           # Mã nguồn chính
├── images/          # Hình ảnh game
├── sounds/          # Âm thanh game
├── music/           # Nhạc nền
├── buttons/         # Hình ảnh nút
├── background/      # Hình nền
├── fonts/           # Font chữ
├── entities/        # Các thực thể trong game
├── game/            # Logic game
├── base/            # Các lớp cơ bản
├── effects/         # Hiệu ứng
├── maps/            # Bản đồ
├── enemies/         # Kẻ thù
├── game_save.json   # File lưu game
├── achievements.json # Thành tích
└── settings.json    # Cài đặt
```

## Tác Giả

Game được phát triển bởi:
- Vinh
- Nhàn
- Minh

## Giấy Phép

Giấy phép bản thân tự cấp :))))

## Logic Game và Cách Làm

### Nguyên Lý Hoạt Động

#### Vòng Lặp Game
1. Khởi tạo game:
   - Load các tài nguyên (hình ảnh, âm thanh, font chữ)
   - Khởi tạo các đối tượng game
   - Load dữ liệu đã lưu (nếu có)

2. Vòng lặp chính:
   - Xử lý sự kiện người dùng
   - Cập nhật trạng thái game
   - Xử lý va chạm
   - Render đồ họa
   - Xử lý âm thanh

3. Kết thúc game:
   - Lưu dữ liệu
   - Giải phóng tài nguyên

### Hệ Thống Vật Lý

#### Va Chạm
- Sử dụng hệ thống va chạm đơn giản dựa trên hình chữ nhật
- Kiểm tra va chạm giữa:
  - Quái vật và đạn
  - Quái vật và tháp
  - Quái vật và căn cứ

#### Chuyển Động
- Quái vật di chuyển theo đường đi được định nghĩa trước
- Đạn bay theo quỹ đạo parabol
- Hiệu ứng nổ và hiệu ứng đặc biệt

### Hệ Thống AI

#### Pathfinding
- Sử dụng thuật toán A* để tìm đường đi cho quái vật
- Tối ưu hóa đường đi để tránh tắc nghẽn
- Các quái vật có thể đi theo nhiều đường khác nhau

#### Hành Vi Quái Vật
- Quái vật có các loại khác nhau với hành vi riêng
- Quái vật có thể tấn công tháp và căn cứ
- Quái vật có thể né tránh đạn

### Hệ Thống Vẽ Hình

#### Nhận Diện Hình Vẽ
- Sử dụng OpenCV để nhận diện hình vẽ
- So sánh hình vẽ với mẫu có sẵn
- Tính toán độ chính xác của hình vẽ

#### Tương Tác
- Người chơi vẽ hình bằng chuột
- Hệ thống kiểm tra hình vẽ trong thời gian thực
- Thưởng điểm dựa trên độ chính xác

### Hệ Thống Kinh Tế

#### Tiền và Tài Nguyên
- Tiền được kiếm từ việc tiêu diệt quái vật
- Chi phí xây dựng và nâng cấp tháp
- Chi phí mua power-up và thiên thạch

#### Nâng Cấp
- Tháp có thể được nâng cấp nhiều cấp độ
- Mỗi cấp độ tăng sát thương và tầm bắn
- Chi phí nâng cấp tăng theo cấp độ

### Hệ Thống Lưu Game

#### Dữ Liệu Được Lưu
- Tiến độ game
- Thành tích đã đạt được
- Cài đặt người dùng
- Trạng thái các tháp và quái vật

#### Cơ Chế Lưu
- Lưu tự động sau mỗi wave
- Lưu thủ công khi người chơi yêu cầu
- Khôi phục dữ liệu khi khởi động lại game

### Tối Ưu Hóa

#### Hiệu Suất
- Sử dụng sprite sheet để giảm số lần load texture
- Tối ưu hóa thuật toán va chạm
- Giảm số lượng đối tượng được render

#### Bộ Nhớ
- Quản lý bộ nhớ hiệu quả
- Giải phóng tài nguyên không cần thiết
- Tối ưu hóa kích thước file lưu

### Công Nghệ Sử Dụng

#### Thư Viện Chính
- Pygame: Xử lý đồ họa và âm thanh
- OpenCV: Nhận diện hình vẽ
- NumPy: Xử lý ma trận và tính toán

#### Công Cụ Phát Triển
- Visual Studio Code: IDE chính
- Git: Quản lý phiên bản
- PyInstaller: Đóng gói game

### Quy Trình Phát Triển

#### Thiết Kế
1. Phân tích yêu cầu
2. Thiết kế kiến trúc
3. Lập kế hoạch phát triển

#### Lập Trình
1. Viết code theo module
2. Kiểm thử từng module
3. Tích hợp các module

#### Kiểm Thử
1. Unit testing
2. Integration testing
3. User testing

#### Tối Ưu Hóa
1. Phân tích hiệu suất
2. Tối ưu hóa code
3. Kiểm tra lại hiệu suất

## Chi Tiết Kỹ Thuật và Code

### 1. Cấu Trúc Lớp Cơ Bản

```python
class GameObject:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.velocity = [0, 0]
        self.health = 100
        self.max_health = 100
        
    def update(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.rect.x = self.x
        self.rect.y = self.y
        
    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)
        
    def check_collision(self, other):
        return self.rect.colliderect(other.rect)
```

Giải thích:
- Lớp `GameObject` là lớp cơ sở cho tất cả các đối tượng trong game
- Mỗi đối tượng có vị trí (x, y), kích thước (width, height) và hình chữ nhật va chạm (rect)
- Phương thức `update()` cập nhật vị trí dựa trên vận tốc
- Phương thức `draw()` vẽ đối tượng lên màn hình
- Phương thức `check_collision()` kiểm tra va chạm với đối tượng khác

### 2. Hệ Thống Quái Vật

```python
class Enemy(GameObject):
    def __init__(self, x, y, path, enemy_type):
        super().__init__(x, y, 32, 32)
        self.path = path
        self.path_index = 0
        self.enemy_type = enemy_type
        self.speed = self.get_speed()
        self.health = self.get_health()
        self.reward = self.get_reward()
        self.symbol = self.get_symbol()
        
    def get_speed(self):
        speeds = {
            'normal': 2,
            'fast': 4,
            'tank': 1
        }
        return speeds.get(self.enemy_type, 2)
        
    def update(self):
        if self.path_index < len(self.path):
            target = self.path[self.path_index]
            dx = target[0] - self.x
            dy = target[1] - self.y
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance < self.speed:
                self.path_index += 1
            else:
                self.velocity[0] = (dx/distance) * self.speed
                self.velocity[1] = (dy/distance) * self.speed
                
        super().update()
        
    def draw(self, screen):
        # Vẽ quái vật
        pygame.draw.circle(screen, self.get_color(), 
                         (int(self.x + self.width/2), 
                          int(self.y + self.height/2)), 
                         self.width/2)
        # Vẽ ký hiệu
        font = pygame.font.Font(None, 24)
        text = font.render(self.symbol, True, (255, 255, 255))
        screen.blit(text, (self.x + 8, self.y + 8))
```

Giải thích:
- Lớp `Enemy` kế thừa từ `GameObject`
- Mỗi quái vật có loại riêng (normal, fast, tank) với tốc độ và máu khác nhau
- Quái vật di chuyển theo đường đi được định nghĩa trước (path)
- Mỗi quái vật có một ký hiệu để người chơi vẽ hình tương ứng

### 3. Hệ Thống Tháp

```python
class Tower(GameObject):
    def __init__(self, x, y, tower_type):
        super().__init__(x, y, 64, 64)
        self.tower_type = tower_type
        self.level = 1
        self.damage = self.get_damage()
        self.range = self.get_range()
        self.cooldown = self.get_cooldown()
        self.last_shot = 0
        self.target = None
        
    def get_damage(self):
        damages = {
            'basic': 10,
            'sniper': 30,
            'aoe': 15
        }
        return damages.get(self.tower_type, 10) * self.level
        
    def update(self, enemies, current_time):
        if current_time - self.last_shot > self.cooldown:
            self.find_target(enemies)
            if self.target:
                self.shoot()
                self.last_shot = current_time
                
    def find_target(self, enemies):
        self.target = None
        min_distance = self.range
        
        for enemy in enemies:
            distance = math.sqrt((enemy.x - self.x)**2 + 
                               (enemy.y - self.y)**2)
            if distance < min_distance:
                self.target = enemy
                min_distance = distance
                
    def shoot(self):
        if self.target:
            bullet = Bullet(self.x + self.width/2,
                          self.y + self.height/2,
                          self.target,
                          self.damage)
            return bullet
        return None
```

Giải thích:
- Lớp `Tower` kế thừa từ `GameObject`
- Mỗi tháp có loại riêng (basic, sniper, aoe) với sát thương và tầm bắn khác nhau
- Tháp tự động tìm mục tiêu trong tầm bắn
- Tháp bắn đạn sau mỗi khoảng thời gian cooldown

### 4. Hệ Thống Vẽ Hình

```python
class DrawingSystem:
    def __init__(self):
        self.current_drawing = []
        self.symbols = {
            'circle': self.load_symbol('circle'),
            'square': self.load_symbol('square'),
            'triangle': self.load_symbol('triangle')
        }
        
    def start_drawing(self, pos):
        self.current_drawing = [pos]
        
    def add_point(self, pos):
        self.current_drawing.append(pos)
        
    def end_drawing(self):
        if len(self.current_drawing) > 2:
            return self.recognize_shape()
        return None
        
    def recognize_shape(self):
        # Chuyển đổi drawing thành ảnh
        drawing_img = self.convert_to_image()
        
        # So sánh với các mẫu
        best_match = None
        best_score = 0
        
        for symbol_name, symbol_img in self.symbols.items():
            score = self.compare_shapes(drawing_img, symbol_img)
            if score > best_score:
                best_score = score
                best_match = symbol_name
                
        return best_match if best_score > 0.7 else None
        
    def convert_to_image(self):
        # Tạo ảnh trắng
        img = np.ones((100, 100), dtype=np.uint8) * 255
        
        # Vẽ các điểm
        for i in range(len(self.current_drawing)-1):
            cv2.line(img, 
                    self.current_drawing[i],
                    self.current_drawing[i+1],
                    0, 2)
                    
        return img
```

Giải thích:
- Lớp `DrawingSystem` quản lý việc vẽ và nhận diện hình
- Hệ thống lưu trữ các điểm vẽ và chuyển đổi thành ảnh
- Sử dụng OpenCV để so sánh hình vẽ với các mẫu có sẵn
- Trả về tên của hình được nhận diện nếu độ chính xác > 70%

### 5. Hệ Thống Wave

```python
class WaveSystem:
    def __init__(self):
        self.current_wave = 0
        self.enemies_per_wave = 10
        self.enemy_types = ['normal', 'fast', 'tank']
        self.spawn_timer = 0
        self.spawn_delay = 1000  # milliseconds
        self.enemies_spawned = 0
        self.wave_in_progress = False
        
    def start_wave(self):
        self.current_wave += 1
        self.enemies_spawned = 0
        self.wave_in_progress = True
        self.enemies_per_wave = 10 + self.current_wave * 2
        
    def update(self, current_time, game_state):
        if not self.wave_in_progress:
            return
            
        if self.enemies_spawned < self.enemies_per_wave:
            if current_time - self.spawn_timer > self.spawn_delay:
                self.spawn_enemy(game_state)
                self.spawn_timer = current_time
                self.enemies_spawned += 1
        elif len(game_state.enemies) == 0:
            self.wave_in_progress = False
            game_state.money += self.calculate_reward()
            
    def spawn_enemy(self, game_state):
        enemy_type = self.get_enemy_type()
        path = game_state.map.get_spawn_path()
        enemy = Enemy(path[0][0], path[0][1], path, enemy_type)
        game_state.enemies.append(enemy)
        
    def get_enemy_type(self):
        weights = {
            'normal': 0.6,
            'fast': 0.3,
            'tank': 0.1
        }
        return random.choices(list(weights.keys()), 
                            weights=list(weights.values()))[0]
```

Giải thích:
- Lớp `WaveSystem` quản lý việc tạo và điều khiển các wave quái vật
- Mỗi wave có số lượng quái vật tăng dần
- Quái vật được spawn sau mỗi khoảng thời gian delay
- Tỷ lệ xuất hiện của các loại quái vật khác nhau
- Phần thưởng được tính dựa trên wave hiện tại

### 6. Hệ Thống Lưu Game

```python
class SaveSystem:
    def __init__(self):
        self.save_file = 'game_save.json'
        
    def save_game(self, game_state):
        save_data = {
            'wave': game_state.wave_system.current_wave,
            'money': game_state.money,
            'towers': [],
            'achievements': game_state.achievements
        }
        
        for tower in game_state.towers:
            tower_data = {
                'type': tower.tower_type,
                'level': tower.level,
                'x': tower.x,
                'y': tower.y
            }
            save_data['towers'].append(tower_data)
            
        with open(self.save_file, 'w') as f:
            json.dump(save_data, f)
            
    def load_game(self):
        try:
            with open(self.save_file, 'r') as f:
                save_data = json.load(f)
            return save_data
        except FileNotFoundError:
            return None
```

Giải thích:
- Lớp `SaveSystem` quản lý việc lưu và tải game
- Dữ liệu được lưu dưới dạng JSON
- Lưu trữ thông tin về wave, tiền, tháp và thành tích
- Có thể tải lại game từ file lưu

### 7. Vòng Lặp Game Chính

```python
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_state = GameState()
        self.drawing_system = DrawingSystem()
        
    def run(self):
        while self.running:
            current_time = pygame.time.get_ticks()
            
            # Xử lý sự kiện
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.drawing_system.start_drawing(event.pos)
                elif event.type == pygame.MOUSEMOTION:
                    if pygame.mouse.get_pressed()[0]:
                        self.drawing_system.add_point(event.pos)
                elif event.type == pygame.MOUSEBUTTONUP:
                    symbol = self.drawing_system.end_drawing()
                    if symbol:
                        self.check_symbol_match(symbol)
                        
            # Cập nhật game
            self.game_state.update(current_time)
            
            # Vẽ game
            self.screen.fill((0, 0, 0))
            self.game_state.draw(self.screen)
            pygame.display.flip()
            
            # Giới hạn FPS
            self.clock.tick(60)
            
    def check_symbol_match(self, symbol):
        for enemy in self.game_state.enemies:
            if enemy.symbol == symbol:
                enemy.health -= 50
                if enemy.health <= 0:
                    self.game_state.money += enemy.reward
                    self.game_state.enemies.remove(enemy)
```

Giải thích:
- Lớp `Game` quản lý vòng lặp game chính
- Xử lý các sự kiện người dùng (nhấn chuột, di chuyển chuột)
- Cập nhật trạng thái game và vẽ lên màn hình
- Kiểm tra kết quả vẽ hình và xử lý tương ứng

### 8. Tối Ưu Hóa Hiệu Suất

```python
class PerformanceOptimizer:
    def __init__(self):
        self.sprite_sheet = {}
        self.cached_images = {}
        
    def load_sprite_sheet(self, filename):
        if filename not in self.sprite_sheet:
            sheet = pygame.image.load(filename).convert_alpha()
            self.sprite_sheet[filename] = sheet
            
    def get_sprite(self, filename, rect):
        key = f"{filename}_{rect}"
        if key not in self.cached_images:
            sheet = self.sprite_sheet[filename]
            image = pygame.Surface(rect.size, pygame.SRCALPHA)
            image.blit(sheet, (0, 0), rect)
            self.cached_images[key] = image
        return self.cached_images[key]
        
    def optimize_collision(self, objects):
        # Sử dụng spatial partitioning
        grid = {}
        for obj in objects:
            cell_x = int(obj.x / 100)
            cell_y = int(obj.y / 100)
            key = (cell_x, cell_y)
            if key not in grid:
                grid[key] = []
            grid[key].append(obj)
            
        return grid
```

Giải thích:
- Lớp `PerformanceOptimizer` quản lý việc tối ưu hóa hiệu suất
- Sử dụng sprite sheet để giảm số lần load texture
- Cache các hình ảnh đã được cắt
- Tối ưu hóa kiểm tra va chạm bằng spatial partitioning

## Chi Tiết Kỹ Thuật Nâng Cao

### 9. Hệ Thống Camera và Viewport

```python
class Camera:
    def __init__(self, width, height):
        self.x = 0
        self.y = 0
        self.width = width
        self.height = height
        self.zoom = 1.0
        self.target = None
        self.smooth_speed = 0.1
        self.bounds = None
        
    def set_bounds(self, min_x, min_y, max_x, max_y):
        self.bounds = (min_x, min_y, max_x, max_y)
        
    def follow(self, target):
        self.target = target
        
    def update(self):
        if self.target:
            target_x = self.target.x - self.width/2
            target_y = self.target.y - self.height/2
            
            # Áp dụng smooth follow
            self.x += (target_x - self.x) * self.smooth_speed
            self.y += (target_y - self.y) * self.smooth_speed
            
            # Giới hạn camera trong bounds
            if self.bounds:
                min_x, min_y, max_x, max_y = self.bounds
                self.x = max(min_x, min(self.x, max_x - self.width))
                self.y = max(min_y, min(self.y, max_y - self.height))
                
    def apply(self, obj):
        # Áp dụng camera transform cho đối tượng
        return (obj.x - self.x, obj.y - self.y)
        
    def apply_zoom(self, obj):
        # Áp dụng zoom cho đối tượng
        return (obj.x * self.zoom, obj.y * self.zoom)
        
    def screen_to_world(self, screen_x, screen_y):
        # Chuyển đổi tọa độ màn hình sang tọa độ thế giới
        return (screen_x + self.x, screen_y + self.y)
        
    def world_to_screen(self, world_x, world_y):
        # Chuyển đổi tọa độ thế giới sang tọa độ màn hình
        return (world_x - self.x, world_y - self.y)

class Viewport:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.camera = Camera(width, height)
        
    def update(self):
        self.camera.update()
        
    def draw(self, screen, draw_func):
        # Lưu trạng thái hiện tại
        old_clip = screen.get_clip()
        
        # Thiết lập viewport
        screen.set_clip(pygame.Rect(self.x, self.y, self.width, self.height))
        
        # Vẽ nội dung
        draw_func(screen, self.camera)
        
        # Khôi phục trạng thái
        screen.set_clip(old_clip)
```

Giải thích:
- Lớp `Camera` quản lý việc theo dõi và hiển thị game
- Hỗ trợ smooth follow và giới hạn camera
- Có thể zoom và chuyển đổi tọa độ
- Lớp `Viewport` quản lý vùng hiển thị trên màn hình
- Tự động cắt xén nội dung ngoài viewport

### 10. Hệ Thống Shader và Hiệu Ứng Hình Ảnh

```python
class ShaderSystem:
    def __init__(self):
        self.shaders = {}
        self.current_shader = None
        
    def load_shader(self, name, vertex_path, fragment_path):
        # Load và compile shader
        vertex_shader = self.compile_shader(vertex_path, GL_VERTEX_SHADER)
        fragment_shader = self.compile_shader(fragment_path, GL_FRAGMENT_SHADER)
        
        # Tạo shader program
        program = glCreateProgram()
        glAttachShader(program, vertex_shader)
        glAttachShader(program, fragment_shader)
        glLinkProgram(program)
        
        self.shaders[name] = program
        
    def use_shader(self, name):
        if name in self.shaders:
            self.current_shader = self.shaders[name]
            glUseProgram(self.current_shader)
            
    def set_uniform(self, name, value):
        if self.current_shader:
            location = glGetUniformLocation(self.current_shader, name)
            if isinstance(value, (int, bool)):
                glUniform1i(location, value)
            elif isinstance(value, float):
                glUniform1f(location, value)
            elif isinstance(value, tuple) and len(value) == 2:
                glUniform2f(location, value[0], value[1])
            elif isinstance(value, tuple) and len(value) == 3:
                glUniform3f(location, value[0], value[1], value[2])
                
class PostProcessing:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.framebuffer = self.create_framebuffer()
        self.texture = self.create_texture()
        self.renderbuffer = self.create_renderbuffer()
        
    def create_framebuffer(self):
        framebuffer = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, framebuffer)
        return framebuffer
        
    def create_texture(self):
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, self.width, self.height, 
                     0, GL_RGB, GL_UNSIGNED_BYTE, None)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, 
                              GL_TEXTURE_2D, texture, 0)
        return texture
        
    def begin(self):
        glBindFramebuffer(GL_FRAMEBUFFER, self.framebuffer)
        glViewport(0, 0, self.width, self.height)
        
    def end(self):
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        glViewport(0, 0, self.width, self.height)
        
    def apply_effect(self, shader_name):
        self.shader_system.use_shader(shader_name)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        # Vẽ fullscreen quad với shader
```

Giải thích:
- Lớp `ShaderSystem` quản lý các shader trong game
- Hỗ trợ load và compile shader từ file
- Có thể set các uniform cho shader
- Lớp `PostProcessing` quản lý hiệu ứng hậu kỳ
- Sử dụng framebuffer để render hiệu ứng

### 11. Hệ Thống Networking Cho Multiplayer

```python
class NetworkManager:
    def __init__(self):
        self.socket = None
        self.connected = False
        self.peers = {}
        self.message_queue = []
        self.sequence_number = 0
        
    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        self.connected = True
        self.start_receive_thread()
        
    def start_receive_thread(self):
        thread = threading.Thread(target=self.receive_loop)
        thread.daemon = True
        thread.start()
        
    def receive_loop(self):
        while self.connected:
            try:
                data = self.socket.recv(4096)
                if data:
                    self.process_message(data)
            except:
                self.connected = False
                
    def process_message(self, data):
        message = json.loads(data.decode())
        if message['type'] == 'game_state':
            self.update_game_state(message['state'])
        elif message['type'] == 'player_action':
            self.handle_player_action(message['action'])
            
    def send_message(self, message_type, data):
        if self.connected:
            message = {
                'type': message_type,
                'sequence': self.sequence_number,
                'data': data
            }
            self.socket.send(json.dumps(message).encode())
            self.sequence_number += 1
            
    def update_game_state(self, state):
        # Cập nhật trạng thái game từ server
        pass
        
    def handle_player_action(self, action):
        # Xử lý hành động của người chơi khác
        pass

class GameServer:
    def __init__(self, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('0.0.0.0', port))
        self.socket.listen(5)
        self.clients = []
        self.game_state = {}
        
    def start(self):
        while True:
            client, address = self.socket.accept()
            self.clients.append(client)
            self.handle_client(client)
            
    def handle_client(self, client):
        while True:
            try:
                data = client.recv(4096)
                if data:
                    self.process_client_message(client, data)
            except:
                self.clients.remove(client)
                break
                
    def broadcast_state(self):
        for client in self.clients:
            client.send(json.dumps({
                'type': 'game_state',
                'state': self.game_state
            }).encode())
```

Giải thích:
- Lớp `NetworkManager` quản lý kết nối mạng cho client
- Hỗ trợ gửi và nhận message
- Tự động xử lý mất kết nối
- Lớp `GameServer` quản lý server game
- Hỗ trợ nhiều client kết nối cùng lúc
- Broadcast trạng thái game cho tất cả client

### 12. Hệ Thống Modding và Mở Rộng

```python
class ModManager:
    def __init__(self):
        self.mods = {}
        self.mod_order = []
        self.mod_config = {}
        
    def load_mod(self, mod_path):
        # Load mod từ thư mục
        mod_info = self.load_mod_info(mod_path)
        if mod_info:
            mod = {
                'name': mod_info['name'],
                'version': mod_info['version'],
                'path': mod_path,
                'enabled': True
            }
            self.mods[mod_info['name']] = mod
            self.mod_order.append(mod_info['name'])
            
    def load_mod_info(self, mod_path):
        try:
            with open(os.path.join(mod_path, 'mod.json'), 'r') as f:
                return json.load(f)
        except:
            return None
            
    def enable_mod(self, mod_name):
        if mod_name in self.mods:
            self.mods[mod_name]['enabled'] = True
            self.load_mod_assets(mod_name)
            
    def disable_mod(self, mod_name):
        if mod_name in self.mods:
            self.mods[mod_name]['enabled'] = False
            self.unload_mod_assets(mod_name)
            
    def load_mod_assets(self, mod_name):
        mod = self.mods[mod_name]
        # Load assets từ thư mục mod
        self.load_textures(mod)
        self.load_sounds(mod)
        self.load_scripts(mod)
        
    def load_textures(self, mod):
        texture_path = os.path.join(mod['path'], 'textures')
        if os.path.exists(texture_path):
            for file in os.listdir(texture_path):
                if file.endswith('.png'):
                    texture = pygame.image.load(os.path.join(texture_path, file))
                    self.texture_manager.add_texture(file, texture)
                    
    def load_scripts(self, mod):
        script_path = os.path.join(mod['path'], 'scripts')
        if os.path.exists(script_path):
            for file in os.listdir(script_path):
                if file.endswith('.py'):
                    self.load_script(os.path.join(script_path, file))
                    
    def load_script(self, script_path):
        # Load và thực thi script Python
        with open(script_path, 'r') as f:
            code = f.read()
        exec(code, globals())
```

Giải thích:
- Lớp `ModManager` quản lý các mod trong game
- Hỗ trợ load mod từ thư mục
- Có thể bật/tắt mod
- Tự động load assets và scripts từ mod
- Hỗ trợ nhiều loại tài nguyên (texture, sound, script)

## Code Đầy Đủ Của Game

### 1. Main Game Loop

```python
import pygame
import sys
import json
import os
from game_state import GameState
from drawing_system import DrawingSystem
from wave_system import WaveSystem
from save_system import SaveSystem
from performance_optimizer import PerformanceOptimizer
from camera import Camera
from viewport import Viewport
from shader_system import ShaderSystem
from network_manager import NetworkManager
from mod_manager import ModManager

class Game:
    def __init__(self):
        # Khởi tạo pygame
        pygame.init()
        pygame.display.set_caption("Tower Defense Game")
        
        # Thiết lập màn hình
        self.screen_width = 1280
        self.screen_height = 720
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        
        # Khởi tạo các hệ thống
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_state = GameState()
        self.drawing_system = DrawingSystem()
        self.wave_system = WaveSystem()
        self.save_system = SaveSystem()
        self.performance_optimizer = PerformanceOptimizer()
        self.camera = Camera(self.screen_width, self.screen_height)
        self.viewport = Viewport(0, 0, self.screen_width, self.screen_height)
        self.shader_system = ShaderSystem()
        self.network_manager = NetworkManager()
        self.mod_manager = ModManager()
        
        # Load các tài nguyên
        self.load_resources()
        
        # Khởi tạo UI
        self.init_ui()
        
    def load_resources(self):
        # Load sprite sheets
        self.performance_optimizer.load_sprite_sheet("images/spritesheet.png")
        
        # Load shaders
        self.shader_system.load_shader("default", "shaders/default.vert", "shaders/default.frag")
        self.shader_system.load_shader("blur", "shaders/blur.vert", "shaders/blur.frag")
        
        # Load mods
        self.mod_manager.load_mod("mods/example_mod")
        
    def init_ui(self):
        # Khởi tạo các nút và UI elements
        self.ui_elements = {
            'start_wave': Button(100, 600, 200, 50, "Start Wave", self.start_wave),
            'shop': Button(400, 600, 200, 50, "Shop", self.open_shop),
            'settings': Button(700, 600, 200, 50, "Settings", self.open_settings)
        }
        
    def start_wave(self):
        self.wave_system.start_wave()
        
    def open_shop(self):
        # Hiển thị shop menu
        pass
        
    def open_settings(self):
        # Hiển thị settings menu
        pass
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_down(event)
            elif event.type == pygame.MOUSEMOTION:
                self.handle_mouse_motion(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.handle_mouse_up(event)
            elif event.type == pygame.KEYDOWN:
                self.handle_key_down(event)
                
    def handle_mouse_down(self, event):
        # Xử lý nhấn chuột
        if event.button == 1:  # Left click
            self.drawing_system.start_drawing(event.pos)
            
    def handle_mouse_motion(self, event):
        # Xử lý di chuyển chuột
        if pygame.mouse.get_pressed()[0]:  # Left button held
            self.drawing_system.add_point(event.pos)
            
    def handle_mouse_up(self, event):
        # Xử lý thả chuột
        if event.button == 1:  # Left click
            symbol = self.drawing_system.end_drawing()
            if symbol:
                self.check_symbol_match(symbol)
                
    def handle_key_down(self, event):
        # Xử lý nhấn phím
        if event.key == pygame.K_SPACE:
            self.start_wave()
        elif event.key == pygame.K_ESCAPE:
            self.open_settings()
            
    def update(self):
        current_time = pygame.time.get_ticks()
        
        # Cập nhật các hệ thống
        self.game_state.update(current_time)
        self.wave_system.update(current_time, self.game_state)
        self.camera.update()
        self.viewport.update()
        
        # Cập nhật UI
        for element in self.ui_elements.values():
            element.update()
            
    def draw(self):
        # Bắt đầu render với shader
        self.shader_system.use_shader("default")
        
        # Vẽ background
        self.screen.fill((0, 0, 0))
        
        # Vẽ game world
        self.viewport.draw(self.screen, self.draw_game_world)
        
        # Vẽ UI
        self.draw_ui()
        
        # Áp dụng hiệu ứng hậu kỳ
        self.apply_post_processing()
        
        # Cập nhật màn hình
        pygame.display.flip()
        
    def draw_game_world(self, screen, camera):
        # Vẽ map
        self.game_state.map.draw(screen, camera)
        
        # Vẽ towers
        for tower in self.game_state.towers:
            tower.draw(screen, camera)
            
        # Vẽ enemies
        for enemy in self.game_state.enemies:
            enemy.draw(screen, camera)
            
        # Vẽ bullets
        for bullet in self.game_state.bullets:
            bullet.draw(screen, camera)
            
        # Vẽ effects
        for effect in self.game_state.effects:
            effect.draw(screen, camera)
            
    def draw_ui(self):
        # Vẽ các UI elements
        for element in self.ui_elements.values():
            element.draw(self.screen)
            
        # Vẽ HUD
        self.draw_hud()
        
    def draw_hud(self):
        # Vẽ thông tin game
        font = pygame.font.Font(None, 36)
        money_text = font.render(f"Money: {self.game_state.money}", True, (255, 255, 255))
        wave_text = font.render(f"Wave: {self.wave_system.current_wave}", True, (255, 255, 255))
        
        self.screen.blit(money_text, (10, 10))
        self.screen.blit(wave_text, (10, 50))
        
    def apply_post_processing(self):
        # Áp dụng hiệu ứng blur
        self.shader_system.use_shader("blur")
        self.shader_system.set_uniform("blur_amount", 0.5)
        
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
```

### 2. Game State

```python
class GameState:
    def __init__(self):
        self.money = 1000
        self.health = 100
        self.towers = []
        self.enemies = []
        self.bullets = []
        self.effects = []
        self.map = Map()
        self.achievements = {}
        self.settings = {
            'sound_volume': 0.5,
            'music_volume': 0.5,
            'graphics_quality': 'medium'
        }
        
    def update(self, current_time):
        # Cập nhật towers
        for tower in self.towers:
            tower.update(self.enemies, current_time)
            
        # Cập nhật enemies
        for enemy in self.enemies[:]:
            enemy.update()
            if enemy.health <= 0:
                self.money += enemy.reward
                self.enemies.remove(enemy)
                
        # Cập nhật bullets
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.lifetime <= 0:
                self.bullets.remove(bullet)
                
        # Cập nhật effects
        for effect in self.effects[:]:
            effect.update()
            if effect.finished:
                self.effects.remove(effect)
                
    def add_tower(self, tower):
        if self.money >= tower.cost:
            self.money -= tower.cost
            self.towers.append(tower)
            return True
        return False
        
    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.game_over()
            
    def game_over(self):
        # Xử lý game over
        pass
```

### 3. Map System

```python
class Map:
    def __init__(self):
        self.width = 2000
        self.height = 2000
        self.tiles = []
        self.paths = []
        self.spawn_points = []
        self.base_position = (1000, 1000)
        self.load_map("maps/default.json")
        
    def load_map(self, filename):
        with open(filename, 'r') as f:
            data = json.load(f)
            
        # Load tiles
        for tile_data in data['tiles']:
            tile = Tile(tile_data['x'], tile_data['y'], 
                       tile_data['type'], tile_data['walkable'])
            self.tiles.append(tile)
            
        # Load paths
        self.paths = data['paths']
        
        # Load spawn points
        self.spawn_points = data['spawn_points']
        
    def get_spawn_path(self):
        # Chọn ngẫu nhiên một spawn point
        spawn_point = random.choice(self.spawn_points)
        return self.find_path(spawn_point, self.base_position)
        
    def find_path(self, start, end):
        # Sử dụng A* để tìm đường đi
        return self.a_star(start, end)
        
    def a_star(self, start, end):
        # Implement A* algorithm
        pass
        
    def draw(self, screen, camera):
        # Vẽ tiles
        for tile in self.tiles:
            tile.draw(screen, camera)
            
        # Vẽ paths
        for path in self.paths:
            pygame.draw.lines(screen, (255, 255, 0), False, path, 2)
```

### 4. Tower System

```python
class Tower(GameObject):
    def __init__(self, x, y, tower_type):
        super().__init__(x, y, 64, 64)
        self.tower_type = tower_type
        self.level = 1
        self.damage = self.get_damage()
        self.range = self.get_range()
        self.cooldown = self.get_cooldown()
        self.cost = self.get_cost()
        self.last_shot = 0
        self.target = None
        self.upgrade_cost = self.get_upgrade_cost()
        
    def get_damage(self):
        damages = {
            'basic': 10,
            'sniper': 30,
            'aoe': 15
        }
        return damages.get(self.tower_type, 10) * self.level
        
    def get_range(self):
        ranges = {
            'basic': 200,
            'sniper': 400,
            'aoe': 150
        }
        return ranges.get(self.tower_type, 200)
        
    def get_cooldown(self):
        cooldowns = {
            'basic': 1000,
            'sniper': 2000,
            'aoe': 1500
        }
        return cooldowns.get(self.tower_type, 1000)
        
    def get_cost(self):
        costs = {
            'basic': 100,
            'sniper': 200,
            'aoe': 150
        }
        return costs.get(self.tower_type, 100)
        
    def get_upgrade_cost(self):
        return self.cost * (self.level + 1)
        
    def upgrade(self):
        if self.game_state.money >= self.upgrade_cost:
            self.game_state.money -= self.upgrade_cost
            self.level += 1
            self.damage = self.get_damage()
            self.range = self.get_range()
            self.upgrade_cost = self.get_upgrade_cost()
            return True
        return False
        
    def update(self, enemies, current_time):
        if current_time - self.last_shot > self.cooldown:
            self.find_target(enemies)
            if self.target:
                bullet = self.shoot()
                if bullet:
                    self.game_state.bullets.append(bullet)
                self.last_shot = current_time
                
    def find_target(self, enemies):
        self.target = None
        min_distance = self.range
        
        for enemy in enemies:
            distance = math.sqrt((enemy.x - self.x)**2 + 
                               (enemy.y - self.y)**2)
            if distance < min_distance:
                self.target = enemy
                min_distance = distance
                
    def shoot(self):
        if self.target:
            return Bullet(self.x + self.width/2,
                         self.y + self.height/2,
                         self.target,
                         self.damage,
                         self.tower_type)
        return None
        
    def draw(self, screen, camera):
        # Vẽ tower
        screen.blit(self.get_texture(), camera.apply(self))
        
        # Vẽ range circle
        pygame.draw.circle(screen, (255, 255, 0, 100),
                         camera.apply(self),
                         self.range, 1)
```

### 5. Enemy System

```python
class Enemy(GameObject):
    def __init__(self, x, y, path, enemy_type):
        super().__init__(x, y, 32, 32)
        self.path = path
        self.path_index = 0
        self.enemy_type = enemy_type
        self.speed = self.get_speed()
        self.health = self.get_health()
        self.max_health = self.health
        self.reward = self.get_reward()
        self.damage = self.get_damage()
        self.symbol = self.get_symbol()
        self.effects = []
        
    def get_speed(self):
        speeds = {
            'normal': 2,
            'fast': 4,
            'tank': 1
        }
        return speeds.get(self.enemy_type, 2)
        
    def get_health(self):
        healths = {
            'normal': 100,
            'fast': 50,
            'tank': 300
        }
        return healths.get(self.enemy_type, 100)
        
    def get_reward(self):
        rewards = {
            'normal': 10,
            'fast': 15,
            'tank': 20
        }
        return rewards.get(self.enemy_type, 10)
        
    def get_damage(self):
        damages = {
            'normal': 10,
            'fast': 5,
            'tank': 20
        }
        return damages.get(self.enemy_type, 10)
        
    def get_symbol(self):
        symbols = {
            'normal': 'circle',
            'fast': 'triangle',
            'tank': 'square'
        }
        return symbols.get(self.enemy_type, 'circle')
        
    def update(self):
        if self.path_index < len(self.path):
            target = self.path[self.path_index]
            dx = target[0] - self.x
            dy = target[1] - self.y
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance < self.speed:
                self.path_index += 1
            else:
                self.velocity[0] = (dx/distance) * self.speed
                self.velocity[1] = (dy/distance) * self.speed
                
        super().update()
        
        # Cập nhật effects
        for effect in self.effects[:]:
            effect.update()
            if effect.finished:
                self.effects.remove(effect)
                
    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            return True
        return False
        
    def add_effect(self, effect):
        self.effects.append(effect)
        
    def draw(self, screen, camera):
        # Vẽ enemy
        screen.blit(self.get_texture(), camera.apply(self))
        
        # Vẽ health bar
        health_percent = self.health / self.max_health
        health_width = self.width * health_percent
        health_rect = pygame.Rect(camera.apply(self)[0],
                                camera.apply(self)[1] - 10,
                                health_width, 5)
        pygame.draw.rect(screen, (255, 0, 0), health_rect)
        
        # Vẽ symbol
        font = pygame.font.Font(None, 24)
        text = font.render(self.symbol, True, (255, 255, 255))
        screen.blit(text, (camera.apply(self)[0] + 8,
                         camera.apply(self)[1] + 8))
        
        # Vẽ effects
        for effect in self.effects:
            effect.draw(screen, camera)
```

### 6. Bullet System

```python
class Bullet(GameObject):
    def __init__(self, x, y, target, damage, bullet_type):
        super().__init__(x, y, 8, 8)
        self.target = target
        self.damage = damage
        self.bullet_type = bullet_type
        self.speed = self.get_speed()
        self.lifetime = self.get_lifetime()
        self.trail = []
        self.max_trail_length = 10
        
    def get_speed(self):
        speeds = {
            'basic': 10,
            'sniper': 20,
            'aoe': 8
        }
        return speeds.get(self.bullet_type, 10)
        
    def get_lifetime(self):
        lifetimes = {
            'basic': 1000,
            'sniper': 2000,
            'aoe': 1500
        }
        return lifetimes.get(self.bullet_type, 1000)
        
    def update(self):
        if self.target and self.target.health > 0:
            dx = self.target.x - self.x
            dy = self.target.y - self.y
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance < self.speed:
                self.hit_target()
            else:
                self.velocity[0] = (dx/distance) * self.speed
                self.velocity[1] = (dy/distance) * self.speed
                
        super().update()
        
        # Cập nhật trail
        self.trail.append((self.x, self.y))
        if len(self.trail) > self.max_trail_length:
            self.trail.pop(0)
            
        self.lifetime -= 16  # Giả sử 60 FPS
        
    def hit_target(self):
        if self.target.take_damage(self.damage):
            # Tạo hiệu ứng khi enemy chết
            effect = ExplosionEffect(self.target.x, self.target.y)
            self.game_state.effects.append(effect)
            
        # Tạo hiệu ứng khi đạn trúng
        effect = HitEffect(self.x, self.y, self.bullet_type)
        self.game_state.effects.append(effect)
        
    def draw(self, screen, camera):
        # Vẽ trail
        if len(self.trail) > 1:
            pygame.draw.lines(screen, (255, 255, 255, 100), False,
                            [camera.apply_point(p) for p in self.trail], 2)
            
        # Vẽ bullet
        screen.blit(self.get_texture(), camera.apply(self))
```

### 7. Effect System

```python
class Effect:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.lifetime = 500
        self.current_time = 0
        self.finished = False
        
    def update(self):
        self.current_time += 16  # Giả sử 60 FPS
        if self.current_time >= self.lifetime:
            self.finished = True
            
class ExplosionEffect(Effect):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.radius = 0
        self.max_radius = 50
        self.color = (255, 0, 0)
        
    def update(self):
        super().update()
        self.radius = (self.current_time / self.lifetime) * self.max_radius
        
    def draw(self, screen, camera):
        pygame.draw.circle(screen, self.color,
                         camera.apply_point((self.x, self.y)),
                         int(self.radius))
                         
class HitEffect(Effect):
    def __init__(self, x, y, effect_type):
        super().__init__(x, y)
        self.effect_type = effect_type
        self.particles = []
        self.create_particles()
        
    def create_particles(self):
        count = 10 if self.effect_type == 'basic' else 20
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 5)
            particle = {
                'x': self.x,
                'y': self.y,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'lifetime': random.uniform(200, 500)
            }
            self.particles.append(particle)
            
    def update(self):
        super().update()
        for particle in self.particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['lifetime'] -= 16
            if particle['lifetime'] <= 0:
                self.particles.remove(particle)
                
    def draw(self, screen, camera):
        for particle in self.particles:
            pygame.draw.circle(screen, (255, 255, 255),
                             camera.apply_point((particle['x'], particle['y'])),
                             2)
```

### 8. UI System

```python
class Button:
    def __init__(self, x, y, width, height, text, callback):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.hovered = False
        self.clicked = False
        
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.hovered = self.rect.collidepoint(mouse_pos)
        
        if self.hovered and pygame.mouse.get_pressed()[0]:
            if not self.clicked:
                self.clicked = True
                self.callback()
        else:
            self.clicked = False
            
    def draw(self, screen):
        # Vẽ background
        color = (200, 200, 200) if self.hovered else (150, 150, 150)
        pygame.draw.rect(screen, color, self.rect)
        
        # Vẽ border
        pygame.draw.rect(screen, (100, 100, 100), self.rect, 2)
        
        # Vẽ text
        font = pygame.font.Font(None, 24)
        text_surface = font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
class Shop:
    def __init__(self):
        self.items = [
            {'name': 'Basic Tower', 'cost': 100, 'type': 'basic'},
            {'name': 'Sniper Tower', 'cost': 200, 'type': 'sniper'},
            {'name': 'AOE Tower', 'cost': 150, 'type': 'aoe'},
            {'name': 'Health', 'cost': 50, 'type': 'health'},
            {'name': 'Hail', 'cost': 2000, 'type': 'hail'}
        ]
        self.visible = False
        
    def draw(self, screen):
        if not self.visible:
            return
            
        # Vẽ background
        pygame.draw.rect(screen, (50, 50, 50), (200, 100, 400, 400))
        
        # Vẽ items
        for i, item in enumerate(self.items):
            y = 120 + i * 60
            pygame.draw.rect(screen, (100, 100, 100), (220, y, 360, 50))
            
            # Vẽ text
            font = pygame.font.Font(None, 24)
            name_text = font.render(item['name'], True, (255, 255, 255))
            cost_text = font.render(f"Cost: {item['cost']}", True, (255, 255, 255))
            
            screen.blit(name_text, (240, y + 10))
            screen.blit(cost_text, (240, y + 30))
```

### 9. Save System

```python
class SaveSystem:
    def __init__(self):
        self.save_file = 'game_save.json'
        
    def save_game(self, game_state):
        save_data = {
            'wave': game_state.wave_system.current_wave,
            'money': game_state.money,
            'towers': [],
            'achievements': game_state.achievements
        }
        
        for tower in game_state.towers:
            tower_data = {
                'type': tower.tower_type,
                'level': tower.level,
                'x': tower.x,
                'y': tower.y
            }
            save_data['towers'].append(tower_data)
            
        with open(self.save_file, 'w') as f:
            json.dump(save_data, f)
            
    def load_game(self):
        try:
            with open(self.save_file, 'r') as f:
                save_data = json.load(f)
            return save_data
        except FileNotFoundError:
            return None
```

Giải thích:
- Lớp `SaveSystem` quản lý việc lưu và tải game
- Dữ liệu được lưu dưới dạng JSON
- Lưu trữ thông tin về wave, tiền, tháp và thành tích
- Có thể tải lại game từ file lưu

### 10. Achievement System

```python
class AchievementSystem:
    def __init__(self):
        self.achievements = {
            'first_kill': {
                'name': 'First Blood',
                'description': 'Tiêu diệt quái vật đầu tiên',
                'completed': False,
                'progress': 0,
                'target': 1
            },
            'wave_10': {
                'name': 'Survivor',
                'description': 'Sống sót qua 10 wave',
                'completed': False,
                'progress': 0,
                'target': 10
            },
            'rich': {
                'name': 'Rich',
                'description': 'Kiếm được 1000 tiền',
                'completed': False,
                'progress': 0,
                'target': 1000
            },
            'level_10': {
                'name': 'Master',
                'description': 'Đạt level 10',
                'completed': False,
                'progress': 0,
                'target': 10
            }
        }
        
    def update(self, game_state):
        # Cập nhật thành tích
        self.check_kills(game_state)
        self.check_wave(game_state)
        self.check_money(game_state)
        self.check_level(game_state)
        
    def check_kills(self, game_state):
        if not self.achievements['first_kill']['completed']:
            self.achievements['first_kill']['progress'] = game_state.total_kills
            if game_state.total_kills >= 1:
                self.achievements['first_kill']['completed'] = True
                self.show_achievement('first_kill')
                
    def check_wave(self, game_state):
        if not self.achievements['wave_10']['completed']:
            self.achievements['wave_10']['progress'] = game_state.wave_system.current_wave
            if game_state.wave_system.current_wave >= 10:
                self.achievements['wave_10']['completed'] = True
                self.show_achievement('wave_10')
                
    def check_money(self, game_state):
        if not self.achievements['rich']['completed']:
            self.achievements['rich']['progress'] = game_state.money
            if game_state.money >= 1000:
                self.achievements['rich']['completed'] = True
                self.show_achievement('rich')
                
    def check_level(self, game_state):
        if not self.achievements['level_10']['completed']:
            self.achievements['level_10']['progress'] = game_state.level
            if game_state.level >= 10:
                self.achievements['level_10']['completed'] = True
                self.show_achievement('level_10')
                
    def show_achievement(self, achievement_id):
        achievement = self.achievements[achievement_id]
        # Hiển thị thông báo thành tích
        print(f"Achievement Unlocked: {achievement['name']}")
```
