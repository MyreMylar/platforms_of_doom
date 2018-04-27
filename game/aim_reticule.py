import math
import pygame


class Reticule:
    def __init__(self, start_pos, owning_player):

        self.screen_position = [int(start_pos[0]), int(start_pos[1])]

        self.owning_player = owning_player
        self.current_radius = 10
        self.center_gap_radius = 2
        self.colour = pygame.Color(150,20,10)

        self.aim_vector = [0.0, 0.0]
        
    def render(self, screen):
        pygame.draw.circle(screen, self.colour, self.screen_position, int(self.current_radius), 2)
        pygame.draw.line(screen, self.colour,
                         [self.screen_position[0], self.screen_position[1] + self.center_gap_radius],
                         [self.screen_position[0], self.screen_position[1] + self.current_radius], 1)
        pygame.draw.line(screen, self.colour,
                         [self.screen_position[0], self.screen_position[1] - self.center_gap_radius],
                         [self.screen_position[0], self.screen_position[1] - self.current_radius], 1)
        pygame.draw.line(screen, self.colour,
                         [self.screen_position[0] + self.center_gap_radius, self.screen_position[1]],
                         [self.screen_position[0] + self.current_radius, self.screen_position[1]], 1)
        pygame.draw.line(screen, self.colour,
                         [self.screen_position[0] - self.center_gap_radius, self.screen_position[1]],
                         [self.screen_position[0] - self.current_radius, self.screen_position[1]], 1)

    def update(self):
        self.aim_vector = [math.cos(self.owning_player.aim_angle), math.sin(self.owning_player.aim_angle)]
        self.screen_position[0] = int(self.owning_player.screen_position[0] + self.aim_vector[0] * 48.0)
        self.screen_position[1] = int(self.owning_player.screen_position[1] + self.aim_vector[1] * 48.0)
