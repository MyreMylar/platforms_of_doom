import math
import pygame


class Explosion:
    def __init__(self, start_pos, colour, radius, base_strength):

        self.position = [int(start_pos[0]), int(start_pos[1])]
        self.screen_position = [int(start_pos[0]), int(start_pos[1])]

        self.current_radius = radius
        self.explosion_time = 0.1
        self.time_acc = 0.0

        self.base_strength = base_strength

        self.colour = colour
        self.should_die = False

    def update_screen_offset(self, screen_offset):
        self.screen_position[0] = int(self.position[0] - screen_offset[0])
        self.screen_position[1] = int(self.position[1] - screen_offset[1])
        
    def render(self, screen):
        pygame.draw.circle(screen, self.colour, self.screen_position, int(self.current_radius), 2)

    def update(self, time_delta, players):
        for player in players:
            distance = self.distance(player.position)
            if distance < self.current_radius:
                strength = self.base_strength * min(1.0, max(0.0, 1.0 - distance / self.current_radius))
                player.apply_force_from(strength, self.position)

        if self.time_acc < self.explosion_time:
            self.time_acc += time_delta
            self.current_radius += 600.0 * time_delta
        else:
            self.should_die = True

    def distance(self, position):
        x_dist = self.position[0] - position[0]
        y_dist = self.position[1] - position[1]
        return math.sqrt((x_dist ** 2) + (y_dist ** 2))
