
from game.base_weapon import BaseWeapon
from game.bullet import Bullet


class MachineGunWeapon(BaseWeapon):

    def __init__(self):
        self.fire_rate = 0.1
        self.fire_rate_acc = 0.0
        self.weapon_force = 100.0

    def fire_key_held(self, dt, player, projectiles):
        if self.fire_rate_acc > self.fire_rate:
            self.fire_rate_acc = 0.0
            projectiles.append(Bullet(player, player.position, player.aim_angle, self.weapon_force))
        else:
            self.fire_rate_acc += dt
