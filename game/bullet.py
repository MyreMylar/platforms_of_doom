import math
import pygame
from game.projectile import Projectile


class Bullet(Projectile):
    def __init__(self, owner, start_pos, aim_angle, bullet_force):

        self.owning_player = owner
        self.aim_angle = aim_angle
        self.current_vector = [math.cos(aim_angle), math.sin(aim_angle)]
        self.position = [start_pos[0], start_pos[1]]

        self.bullet_force = bullet_force

        self.screen_position = [start_pos[0], start_pos[1]]
        
        self.should_die = False

        self.speed = 500.0
        self.velocity = [0.0, 0.0]
        self.velocity[0] = self.speed * self.current_vector[0]
        self.velocity[1] = self.speed * self.current_vector[1]

        self.image = pygame.image.load("images/bullet.png")
        facing_angle = math.atan2(-self.current_vector[0], -self.current_vector[1]) * 180 / math.pi
        self.image = pygame.transform.rotate(self.image, facing_angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        self.screen_rect = self.image.get_rect()
        self.screen_rect.center = self.screen_position
        self.shotRange = 1000.0

    def update_screen_offset(self, screen_offset):
        self.screen_position[0] = self.position[0] - screen_offset[0]
        self.screen_position[1] = self.position[1] - screen_offset[1]
        self.screen_rect.x = self.rect.x - screen_offset[0]
        self.screen_rect.y = self.rect.y - screen_offset[1]

    def render(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, time_delta, gravity, platforms, players, explosions):
        for platform in platforms:
            if platform.rect.colliderect(self.rect):
                self.should_die = True
                
        for player in players:
            if player != self.owning_player:
                if player.rect.colliderect(self.rect):
                    self.should_die = True
                    player.apply_force_from(self.bullet_force, self.position)

        self.shotRange -= time_delta * math.sqrt(self.velocity[0] ** 2 + self.velocity[1] ** 2)
        
        self.position[0] += self.velocity[0] * time_delta
        self.position[1] += self.velocity[1] * time_delta
        self.rect.center = (int(self.position[0]), int(self.position[1]))

        if self.shotRange <= 0.0:
            self.should_die = True
