import json
import os
from datetime import datetime

class SaveSystem:
    def __init__(self):
        self.save_file = 'game_save.json'
        self.default_data = {
            'money': 0,
            'achievements': {
                'kill_100': {'name': 'SAT THU', 'desc': 'Tieu diet 100 quai', 'unlocked': False},
                'survive_10': {'name': 'KIEN NGHI', 'desc': 'Song sot 10 wave', 'unlocked': False},
                'level_10': {'name': 'HUYEN THOAI', 'desc': 'Dat level 10', 'unlocked': False},
                'money_1000': {'name': 'TY PHU', 'desc': 'Co 1000 tien', 'unlocked': False}
            },
            'shop_items': {
                'health_1': {'name': 'Tang 1 Mau', 'cost': 1000, 'bought': 0},
                'health_2': {'name': 'Tang 2 Mau', 'cost': 1900, 'bought': 0},
                'health_3': {'name': 'Tang 3 Mau', 'cost': 2700, 'bought': 0}
            },
            'last_save': None
        }
        self.data = self.load_data()

    def load_data(self):
        # neu file dang ton tai thi doc du lieu tu file, neu khong thi tra ve du lieu mac dinh
        if os.path.exists(self.save_file):
            # nếu dữ liệu lỗi thì nó trả về dữ liệu mặc định
            try:
                with open(self.save_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return self.default_data
        return self.default_data
    
    # dùng để save
    def save_data(self):
        self.data['last_save'] = datetime.now().isoformat()
        with open(self.save_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)
    # tạo 1 biến trung gian và gán biến đó thành số tiền
    def update_money(self, amount):
        if isinstance(amount, (int, float)) and amount >= 0:
            self.data['money'] = amount
            self.save_data()
        else:
            print("Số tiền không hợp lệ")
    
    def get_money(self):
        return self.data['money']
# cập nhật trạng thái hoàn thành thành tựu
    def update_achievement(self, achievement_id, unlocked):
        if achievement_id in self.data['achievements']:
            self.data['achievements'][achievement_id]['unlocked'] = unlocked
            self.save_data()

    def get_achievements(self):
        return self.data['achievements']

    def update_shop_items(self, items):
        self.data['shop_items'] = items
        self.save_data()

    def get_shop_items(self):
        return self.data['shop_items']
# function mua shop
    def buy_shop_item(self, item_id):
        # check xem item_id co trong data shop items khong
        if item_id in self.data['shop_items']:
            # gán item thay cho tên gốc health_1 và item này chứa các thuộc tính của thằng kia 
            item = self.data['shop_items'][item_id]
            # nếu money trong data lớn hơn giá tiền hiện tại thì thực thi câu lệnh bên dưới
            if self.data['money'] >= item['cost']:
                # trừ số tiền hiện tại cho giá của item hiện tại
                self.data['money'] -= item['cost']
                # tăng số lượng item lên sau khi mua
                item['bought'] += 1
                # lưu lại data
                self.save_data()
                return True
        return False

    def get_total_health(self):
        total_health = 1  # Máu mặc định
        # items() là phương thức có sẵn dùng để đuyệt key và value của shop_items nó sẽ trả về 2 kiểu data đó
        for item_id, item in self.data['shop_items'].items():
            # nếu phát hiện bought lớn hơn 0 thì thực thi câu lệnh
            if item['bought'] > 0:
                # tách số ra từ chữ để lấy số máu ở đây là health_1 thì nó tách đc số 1 tương đương với 1 máu
                health_amount = int(item_id.split('_')[1])
                # tổng máu bằng số máu hiện tại nhân với số lượng máu 
                total_health += health_amount * item['bought']
        return total_health 