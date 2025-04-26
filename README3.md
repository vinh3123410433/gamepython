# Cấu Trúc Dự Án

## Thư Mục Gốc
```
gamepython/
├── main.py                 # File chạy chính của game
├── game_save.json         # File lưu trữ dữ liệu game
├── achievements.json      # File lưu trữ thành tích
├── settings.json         # File cấu hình game
└── README.md            # Hướng dẫn sử dụng
```

## Thư Mục Source
```
source/
├── main.py              # Điểm khởi đầu của game
├── achievements.py      # Hệ thống thành tích
├── enemy.py            # Quản lý kẻ thù
├── explosion.py        # Hiệu ứng nổ
├── features.py         # Các tính năng bổ sung
├── gameover.py         # Màn hình game over
├── hail.py            # Hệ thống thiên thạch
├── map.py             # Quản lý bản đồ
├── menu.py            # Menu game
├── player.py          # Quản lý người chơi
├── save_system.py     # Hệ thống lưu game
├── sender.py          # Xử lý gửi dữ liệu
├── setting.py         # Cài đặt game
└── sound_button.py    # Quản lý âm thanh
```

## Thư Mục Assets

### Background
```
background/
├── Background_Layer_01.png    # Layer nền 1
├── Background_Layer_02.png    # Layer nền 2
├── Background_Layer_03.png    # Layer nền 3
├── Background_Layer_04.png    # Layer nền 4
├── Background_Layer_05.png    # Layer nền 5
├── Background_MergedForReference.jpg
├── bg_open_meadow.png
├── Paper.jpg
├── Sunny Cloud Background.png
└── WDT1.PNG, WDT2.PNG
```

### Buttons
```
buttons/
├── blue_soft cut.PNG
├── blue_soft.png
├── GreenButtons.png
└── ok.png
```

### Images & Effects
```
images/
├── boom1.png, boom2.png, boom3.png    # Hiệu ứng nổ
├── cloud.png                          # Hiệu ứng mây
├── hearts.png                         # Icon mạng sống
├── meteor.png, meteor1.png...         # Thiên thạch
├── moneySign.png                      # Icon tiền
└── mud.png                           # Hiệu ứng bùn
```

### Maps
```
maps/
├── bloon4/
│   ├── tracks.jpeg
│   └── Tracks.jpg
├── maze/
│   └── maze.png
├── monkey lane/
│   ├── image.png
│   ├── targets.txt
│   └── waves.txt
├── park path/
│   ├── image.png
│   ├── targets.txt
│   └── waves.txt
└── sprint track/
    ├── sprint track.png
    └── sprint.png
```

### Audio
```
music/
├── maintheme.mp3              # Nhạc nền chính
├── Party in Paradise.ogg      # Nhạc menu
└── Ruby_chan1.mp3, Ruby_chan2.mp3

sounds/
├── buy upgrade.mp3           # Âm thanh nâng cấp
├── buy.mp3                  # Âm thanh mua
├── click.mp3                # Âm thanh click
├── Explosion.wav            # Âm thanh nổ
├── Fire.wav                 # Âm thanh bắn
├── GameOver.wav            # Âm thanh game over
├── life_lost.mp3           # Âm thanh mất mạng
├── new tower intro.mp3     # Âm thanh tháp mới
├── place tower.mp3         # Âm thanh đặt tháp
├── pop1.mp3...pop4.mp3     # Âm thanh tiêu diệt quái
└── sell tower.mp3          # Âm thanh bán tháp
```

## Mô Tả Chi Tiết Các Module

### Core Modules

1. **main.py**
   - Khởi tạo game
   - Quản lý vòng lặp game chính
   - Xử lý sự kiện người chơi

2. **map.py**
   - Quản lý bản đồ game
   - Xử lý đường đi của quái vật
   - Quản lý vị trí đặt tháp

3. **enemy.py**
   - Định nghĩa các loại quái vật
   - Quản lý hành vi của quái
   - Xử lý va chạm và sát thương

4. **player.py**
   - Quản lý thông tin người chơi
   - Xử lý điều khiển và tương tác
   - Quản lý tiền và tài nguyên

### Feature Modules

1. **features.py**
   - Các tính năng đặc biệt
   - Power-ups và bonus
   - Hệ thống nhiệm vụ

2. **hail.py**
   - Hệ thống thiên thạch
   - Hiệu ứng và sát thương
   - Cơ chế mua và sử dụng

3. **explosion.py**
   - Hiệu ứng nổ
   - Particle effects
   - Visual feedback

### UI Modules

1. **menu.py**
   - Menu chính
   - Menu tạm dừng
   - Menu cài đặt

2. **setting.py**
   - Cài đặt âm thanh
   - Cài đặt đồ họa
   - Tùy chỉnh điều khiển

3. **sound_button.py**
   - Quản lý âm thanh UI
   - Hiệu ứng âm thanh
   - Phản hồi người dùng

### Save System

1. **save_system.py**
   - Lưu trữ tiến độ
   - Quản lý thành tích
   - Backup và khôi phục

2. **achievements.py**
   - Hệ thống thành tích
   - Theo dõi tiến độ
   - Phần thưởng

## Quy Ước Lập Trình

1. **Naming Conventions**
   - Classes: PascalCase
   - Functions: snake_case
   - Variables: snake_case
   - Constants: UPPERCASE

2. **File Structure**
   - Imports đầu file
   - Constants
   - Classes
   - Helper functions

3. **Documentation**
   - Docstrings cho classes và functions
   - Comments cho logic phức tạp
   - README cho mỗi module

## Workflow Development

1. **Version Control**
   - Git flow
   - Feature branches
   - Pull requests

2. **Testing**
   - Unit tests
   - Integration tests
   - Playtest

3. **Deployment**
   - Build process
   - Asset packaging
   - Distribution

## Hướng Dẫn Phát Triển

1. **Setup Development Environment**
   ```bash
   # Clone repository
   git clone [repository_url]
   cd gamepython

   # Install dependencies
   pip install -r requirements.txt
   ```

2. **Run Development Server**
   ```bash
   python source/main.py
   ```

3. **Build Distribution**
   ```bash
   # Create distribution
   pyinstaller main.spec

   # Package assets
   python tools/package_assets.py
   ```