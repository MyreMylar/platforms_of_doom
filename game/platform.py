import pygame


class Platform:
    def __init__(self, top_left, bottom_right):
        self.rect = pygame.Rect(top_left, (bottom_right[0]-top_left[0], bottom_right[1]-top_left[1]))
        self.screen_rect = pygame.Rect(top_left, (bottom_right[0]-top_left[0], bottom_right[1]-top_left[1]))

        percentage_of_screen = (top_left[1]/700.0)
        self.bottomCol = pygame.Color(30, 40, 36, 255)
        self.topCol = pygame.Color(199, 231, 143, 255)
        red_col = int(self.lerp(self.bottomCol.r, self.topCol.r, percentage_of_screen))
        green_col = int(self.lerp(self.bottomCol.g, self.topCol.g, percentage_of_screen))
        blue_col = int(self.lerp(self.bottomCol.b, self.topCol.b, percentage_of_screen))
        self.colour = pygame.Color(red_col, green_col, blue_col, 255)

    def update_screen_offset(self, screen_offset):
        self.screen_rect.x = self.rect.x - screen_offset[0]
        self.screen_rect.y = self.rect.y - screen_offset[1]
            
    @staticmethod
    def lerp(start, end, percentage):
        return (percentage * end) + ((1.0-percentage) * start)

    def render(self, screen):
        pygame.draw.rect(screen, self.colour, self.screen_rect)
