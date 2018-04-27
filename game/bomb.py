import math
import pygame
from game.projectile import Projectile
from game.explosion import Explosion


class Bomb(Projectile):
    def __init__(self, owner, start_pos, aim_angle, player_x_movement, is_big_bomb):

        self.is_big_bomb = is_big_bomb
        self.owning_player = owner
        self.aim_angle = aim_angle
        self.current_vector = [math.cos(aim_angle), math.sin(aim_angle)]
        self.position = [start_pos[0], start_pos[1]]

        self.screen_position = [start_pos[0], start_pos[1]]
        
        self.should_die = False

        self.speed = 500.0
        self.velocity = [0.0, 0.0]
        self.velocity[0] = self.speed * self.current_vector[0] + player_x_movement / 2
        self.velocity[1] = self.speed * self.current_vector[1]

        self.image = pygame.image.load("images/bomb.png")
        self.rect = pygame.Rect((self.position[0]-4, self.position[1]-4), (8, 8))
        self.screen_rect = pygame.Rect((self.position[0]-4, self.position[1]-4), (8, 8))
        self.shot_range = 1000.0

    def update_screen_offset(self, screen_offset):
        self.screen_position[0] = self.position[0] - screen_offset[0]
        self.screen_position[1] = self.position[1] - screen_offset[1]
        self.screen_rect.x = self.rect.x - screen_offset[0]
        self.screen_rect.y = self.rect.y - screen_offset[1]

    def render(self, screen):
        screen.blit(self.image, self.rect)

    def make_explosion(self, explosions):
        if self.is_big_bomb:
            explosions.append(Explosion(self.position, pygame.Color(200,50,50,255), 20, 75.0))
        else:
            explosions.append(Explosion(self.position, pygame.Color(40,30,30,255), 10, 50.0))

    def update(self, time_delta, gravity, platforms, players, explosions):
        for platform in platforms:
            if platform.rect.colliderect(self.rect):
                self.should_die = True
                self.make_explosion(explosions)
        for player in players:
            if player != self.owning_player:
                if player.rect.colliderect(self.rect):
                    self.should_die = True
                    self.make_explosion(explosions)

        self.shot_range -= time_delta * math.sqrt(self.velocity[0] ** 2 + self.velocity[1] ** 2)
        self.velocity[0] = self.velocity[0] + time_delta * gravity[0]
        self.velocity[1] = self.velocity[1] + time_delta * gravity[1]
        
        self.position[0] += self.velocity[0] * time_delta
        self.position[1] += self.velocity[1] * time_delta
        self.rect.center = (int(self.position[0]), int(self.position[1]))

        if self.shot_range <= 0.0:
            self.should_die = True
