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
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return self.default_data
        return self.default_data

    def save_data(self):
        self.data['last_save'] = datetime.now().isoformat()
        with open(self.save_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def update_money(self, amount):
        if isinstance(amount, (int, float)) and amount >= 0:
            self.data['money'] = amount
            self.save_data()
        else:
            print("Số tiền không hợp lệ")

    def get_money(self):
        return self.data['money']

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

    def buy_shop_item(self, item_id):
        if item_id in self.data['shop_items']:
            item = self.data['shop_items'][item_id]
            if self.data['money'] >= item['cost']:
                self.data['money'] -= item['cost']
                item['bought'] += 1
                self.save_data()
                return True
        return False

    def get_total_health(self):
        total_health = 1  # Máu mặc định
        for item_id, item in self.data['shop_items'].items():
            if item['bought'] > 0:
                health_amount = int(item_id.split('_')[1])
                total_health += health_amount * item['bought']
        return total_health 