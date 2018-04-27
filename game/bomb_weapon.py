from game.base_weapon import BaseWeapon
from game.bomb import Bomb


class BombWeapon(BaseWeapon):

    def __init__(self):
        self.fire_big_bombs = False

    def make_weapon_more_explosive(self):
        self.fire_big_bombs = True

    def make_weapon_normal(self):
        self.fire_big_bombs = False

    def fire_key_pressed(self, player, projectiles):
        projectiles.append(Bomb(player, player.position, player.aim_angle, player.x_acceleration, self.fire_big_bombs))
