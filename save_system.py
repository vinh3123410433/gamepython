import json
import os
from datetime import datetime

class SaveSystem:
    def __init__(self):
        self.save_file = 'game_save.json'
        self.default_data = {
            'money': 0,
            'achievements': {
                'kill_100': {'name': 'SAT THU', 'desc': 'Tiêu diệt 100 quái', 'unlocked': False},
                'survive_10': {'name': 'KIEN NGHI', 'desc': 'Sống sót 10 wave', 'unlocked': False},
                'level_10': {'name': 'HUYEN THOAI', 'desc': 'Đạt level 10', 'unlocked': False},
                'money_1000': {'name': 'TY PHU', 'desc': 'Có 1000 tiền', 'unlocked': False}
            },
            'shop_items': {
                'health_1': {'name': 'Tăng 1 Máu', 'cost': 100, 'bought': False},
                'health_2': {'name': 'Tăng 2 Máu', 'cost': 250, 'bought': False},
                'health_3': {'name': 'Tăng 3 Máu', 'cost': 500, 'bought': False}
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
        self.data['money'] = amount
        self.save_data()

    def get_money(self):
        return self.data['money']

    def update_achievement(self, achievement_id, unlocked):
        if achievement_id in self.data['achievements']:
            self.data['achievements'][achievement_id]['unlocked'] = unlocked
            self.save_data()

    def get_achievements(self):
        return self.data['achievements']

    def buy_shop_item(self, item_id):
        if item_id in self.data['shop_items']:
            item = self.data['shop_items'][item_id]
            if not item['bought'] and self.data['money'] >= item['cost']:
                self.data['money'] -= item['cost']
                item['bought'] = True
                self.save_data()
                return True
        return False

    def get_shop_items(self):
        return self.data['shop_items']

    def get_bought_health(self):
        health = 1  # Máu mặc định
        for item_id, item in self.data['shop_items'].items():
            if item['bought']:
                health += int(item_id.split('_')[1])
        return health 