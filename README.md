# Tower Defense Game

Game phòng thủ tháp (Tower Defense) được phát triển bằng Python và Pygame, với cơ chế vẽ hình độc đáo để tiêu diệt kẻ địch.

## Mục Lục
1. [Giới Thiệu](#giới-thiệu)
2. [Các Class Chính](#các-class-chính)
3. [Cơ Chế Game Đặc Biệt](#cơ-chế-game-đặc-biệt)
4. [Yêu Cầu Hệ Thống](#yêu-cầu-hệ-thống)
5. [Cách Chơi](#cách-chơi)
6. [Tác Giả](#tác-giả)
7. [Giấy Phép](#giấy-phép)

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

## Các Class Chính

### 1. Enemy (enemy.py)
Quản lý kẻ địch trong game:
- Thuộc tính: vị trí, máu, tốc độ, phần thưởng khi tiêu diệt
- Di chuyển theo đường đi định sẵn
- Hệ thống máu và thanh máu
- Xử lý va chạm và chết
- Mỗi kẻ địch có một biểu tượng riêng để người chơi vẽ

### 2. Map (map.py)
Quản lý bản đồ và đường đi:
- Load bản đồ từ file
- Quản lý điểm spawn và đường đi của kẻ địch
- Load và quản lý các wave của kẻ địch
- Xử lý background và layer của bản đồ

### 3. Player (player.py)
Quản lý thông tin người chơi:
- Điểm số, tiền, máu
- Hệ thống level và kinh nghiệm
- Lưu và load dữ liệu người chơi
- Tương tác với shop và nâng cấp

### 4. ShopSystem (features.py)
Hệ thống cửa hàng:
- Mua vật phẩm và nâng cấp
- Quản lý tiền và giá cả
- Giao diện mua sắm
- Các item như máu, thiên thạch

### 5. AchievementSystem (achievements.py)
Hệ thống thành tích:
- Theo dõi tiến độ thành tích
- Hiển thị thông báo thành tích
- Lưu trữ thành tích đã đạt được
- Các mục tiêu như: tiêu diệt kẻ địch, vượt qua wave, đạt level

### 6. Menu (menu.py)
Quản lý menu game:
- Menu chính với các nút: Start, Shop, Hướng dẫn
- Điều hướng giữa các màn hình
- Xử lý âm thanh và cài đặt
- Giao diện người dùng

### 7. Explosion và Hail (explosion.py, hail.py)
Hiệu ứng đặc biệt:
- Explosion: Hiệu ứng nổ khi kẻ địch chết
- Hail: Thiên thạch có thể mua để tấn công kẻ địch

### 8. SaveSystem (save_system.py)
Quản lý lưu trữ:
- Lưu và load dữ liệu game
- Lưu tiến độ người chơi
- Lưu cài đặt và thành tích

## Cơ Chế Game Đặc Biệt

### Hệ Thống Vẽ Hình
Game sử dụng OpenCV để nhận diện hình vẽ:
- Người chơi vẽ hình để tiêu diệt kẻ địch
- Các hình cơ bản: ngang, dọc, chéo, tròn, chữ V
- Độ chính xác vẽ ảnh hưởng đến kết quả
- Phản hồi trực quan khi vẽ đúng/sai

### Hệ Thống Wave
- Kẻ địch xuất hiện theo wave
- Độ khó tăng dần theo thời gian
- Nhiều loại kẻ địch khác nhau
- Phần thưởng sau mỗi wave

### Power-ups và Vật Phẩm
- Thiên thạch (Hail): Tấn công diện rộng
- Nâng cấp máu
- Vật phẩm đặc biệt từ shop

## Yêu Cầu Hệ Thống
- Python 3.x
- Pygame
- OpenCV
- NumPy

## Cách Chơi
1. SPACE: Bắt đầu wave
2. H: Mua thiên thạch (2000 tiền)
3. ESC: Quay lại menu
4. Vẽ hình tương ứng với ký hiệu trên kẻ địch
5. W/S: Tăng/giảm tốc độ game

## Tác Giả

Game được phát triển bởi:
- Vinh
- Nhàn
- Minh

## Giấy Phép

Giấy phép bản thân tự cấp :))))
