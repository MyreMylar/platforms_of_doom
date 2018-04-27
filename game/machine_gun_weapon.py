
from game.base_weapon import BaseWeapon
from game.bullet import Bullet


class MachineGunWeapon(BaseWeapon):

    def __init__(self):
        self.fire_rate = 0.1
        self.fire_rate_acc = 0.0
        self.weapon_force = 100.0
