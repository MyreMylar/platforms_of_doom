
from game.base_weapon import BaseWeapon
from game.bullet import Bullet


# -----------------------------------------------
# Challenge 2
# -------------
#
# Finish creating a Machine Gun weapon.
#
# HINTS
#
# - Check out the bomb_weapon and base_weapon
#   files, your class will need to be similar.
#
# - A machine gun usually fires automatically
#   at a certain fire rate when you *hold down*
#   the fire button/trigger. You can
#   use a timer (adding dt to the self.fire_rate_acc)
#   to achieve this. We used a timer last week
#   for the power up spawns.
#
# - I already made a Bullet class for bullets.
#
# -----------------------------------------------
# To finish the machine gun you'll need to
# edit the player code file in Challenge 3.
# -----------------------------------------------
class MachineGunWeapon(BaseWeapon):

    def __init__(self):
        self.fire_rate = 0.1
        self.fire_rate_acc = 0.0
        self.weapon_force = 100.0
