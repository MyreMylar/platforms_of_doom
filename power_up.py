import pygame
import random


class PowerUp:

    def __init__(self, spawn_pos):
        self.all_types = ["double_jump", "machine_gun", "explosion"]
        self.type = random.choice(self.all_types)

        if self.type == "double_jump":
            self.image = pygame.image.load("images/double_jump_power_up.png")
        elif self.type == "machine_gun":
            self.image = pygame.image.load("images/machine_gun_power_up.png")
        else:
            self.image = pygame.image.load("images/explosion_power_up.png")
        
        self.rect = pygame.Rect([spawn_pos[0]-8, spawn_pos[1]-8], (16, 16))
        self.screen_rect = pygame.Rect([spawn_pos[0]-8, spawn_pos[1]-8], (16, 16))
        
        self.should_die = False

    def update_screen_offset(self, screen_offset):
        self.screen_rect.x = self.rect.x - screen_offset[0]
        self.screen_rect.y = self.rect.y - screen_offset[1]

    def update(self, players):
        for player in players:
            if player.rect.colliderect(self.rect):
                player.add_active_power_up(self.type)
                self.should_die = True
        
    def render(self, screen):
        screen.blit(self.image, self.rect)
