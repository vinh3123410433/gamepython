from setting import senderList, enemyList
from enemy import Enemy


class Sender:
    def __init__(self,wave, player, mapvar):
        self.wave = wave
        self.timer = 0 
        self.rate = 1
        self.enemies = []
        enemies = mapvar.waves[wave-1].split(',')
        for enemy in enemies:
            amount,layer = enemy.split('*')
            self.enemies += [eval(layer)-1]*eval(amount)
        senderList.append(self)
        self.player = player
        self.mapvar = mapvar

    def update(self,frametime,wave):
        if not self.enemies:
            if not enemyList: 
                senderList.remove(self)
                wave+=1
                self.player.money+=99+self.wave
        elif self.timer > 0: 
            self.timer -= frametime
        else: 
            self.timer = self.rate
            Enemy(self.enemies[0], self.player, self.mapvar)
            del self.enemies[0]
        return wave