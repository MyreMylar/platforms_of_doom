import pygame
import random


# MAKE SURE TO SCROLL DOWN TO THE CODE!!

# -------------------------------------------------------------
# Challenge 1, part a) - two lines of code
# -----------------------------------------
#
# The first part of our changes to the power_up code
# is to choose a random power up type from those
# available and activate it on the player when collected.
#
# I've prepared the code to add three
# types of power ups and stored their names
# in the self.all_types variable.
#
# HINTS
# -------
#
# 1. Assign self.type to a random type from self.all_types.
#    Use random.choice as we did last week with the platforms.
#
# 2. Call the add_active_power_up() function on the player
#    when he collides with the power up. This
#    is the same place where we kill the power up.
# -------------------------------------------------------------

# ------------------------------------------------
# Challenge 1, part b) - two lines of code
# -----------------------------------------
#
# The second part of our challenge is to change the
# simple white squares that represent
# our power ups into images so we can
# distinguish between types of power ups.
#
# HINTS
# --------
#
# - I have provided 3 power up images in
#   the images sub directory.
#
# - We will need to load a pygame image of
#   the right type. Use pygame.image.load()
#
# - We will need to blit the image instead
#   of drawing a rectangle.
#
# - check out the bomb.py file to see an example.
#
# - When you are done you can remove the self.colour
#   variable because you won't need it anymore!
# -------------------------------------------------
# To finish adding the machine gun power up
# you'll need to do Challenge 2 and create the
# machine gun weapon in the machine_gun_weapon code
# file.
# -------------------------------------------------
class PowerUp:

    def __init__(self, spawn_pos):
        self.all_types = ["double_jump", "machine_gun", "explosion"]
        self.type = ""

        if self.type == "double_jump":
            pass
        elif self.type == "machine_gun":
            pass
        else:
            pass
        
        self.rect = pygame.Rect([spawn_pos[0]-8, spawn_pos[1]-8], (16, 16))
        self.screen_rect = pygame.Rect([spawn_pos[0]-8, spawn_pos[1]-8], (16, 16))

        self.color = pygame.color.Color(255, 255, 255, 255)
        
        self.should_die = False

    def update_screen_offset(self, screen_offset):
        self.screen_rect.x = self.rect.x - screen_offset[0]
        self.screen_rect.y = self.rect.y - screen_offset[1]

    def update(self, players):
        for player in players:
            if player.rect.colliderect(self.rect):
                self.should_die = True
        
    def render(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
