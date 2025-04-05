class Player:
    def __init__(self):
        self.health = 10
        self.money = 30000000
        self.score = 0
        self.level = 1
        self.exp = 0
        self.exp_to_next_level = 1000

    def add_exp(self, amount):
        self.exp += amount
        if self.exp >= self.exp_to_next_level:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.exp -= self.exp_to_next_level
        self.exp_to_next_level = int(self.exp_to_next_level * 1.5)
        self.health += 1
        self.money += 1000
        print(f"Level Up! Bạn đã đạt level {self.level}!")
