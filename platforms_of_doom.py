import os
import pygame
from pygame.locals import *

from game.platform import Platform
from game.player import Player, ControlScheme
# from power_up import PowerUp # import your PowerUp class here once it is made


def main():
   
    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    screen_size = (800, 700)
    pygame.display.set_caption('Platforms of Doom')
    screen = pygame.display.set_mode(screen_size)

    background = pygame.image.load("images/background.png")
    level_size = (background.get_width(), background.get_height())
    background = background.convert() 
        
    font = pygame.font.Font("fonts/Economica-Bold.ttf", 26) 

    platforms = [Platform((320, 100), (480, 115)), Platform((580, 150), (780, 165)),
                 Platform((20, 150), (140, 165)), Platform((220, 200), (400, 215)),
                 Platform((150, 300), (350, 315)), Platform((80, 400), (200, 415)),
                 Platform((320, 400), (650, 415)), Platform((580, 500), (780, 515)),
                 Platform((280, 500), (380, 515)), Platform((400, 600), (680, 615)),
                 Platform((20, 600), (280, 615))]

    projectiles = []
    explosions = []

    player1_controls = ControlScheme()
    player1_controls.left = K_a
    player1_controls.right = K_d
    player1_controls.jump = K_SPACE
    player1_controls.fire = K_LSHIFT
    player1_controls.aimUp = K_w
    player1_controls.aimDown = K_s

    player2_controls = ControlScheme()
    
    players = []
    
    player1 = Player(players, platforms, 0, player1_controls)
    players.append(player1)
    
    player2 = Player(players, platforms, 176, player2_controls)
    players.append(player2)

    # create a list to store power ups, as well as some variables to run a timer

    clock = pygame.time.Clock()

    screen_offset = [0.0, 0.0]

    gravity = [0.0, 1000.0]
    running = True  
    while running:

        frame_time = clock.tick()
        time_delta = frame_time/1000.0
             
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            for player in players:
                player.process_event(event)
                        
        screen.blit(background, (-screen_offset[0], -screen_offset[1]))  # draw the background surface to our screen

        screen_offset = player1.get_screen_offset(screen_size, level_size)

        # spawn power ups here when a time accumulator variable is greater than a timer variable that you make
        #

        for platform in platforms:
            platform.update_screen_offset(screen_offset)
            platform.render(screen)

        # for power_up in power_ups:
        #    power_up.update(players)
        #    power_up.update_screen_offset(screen_offset)
        #    power_up.render(screen)
        # power_ups[:] = [power_up for power_up in power_ups if not power_up.should_die]

        for projectile in projectiles:
            projectile.update(time_delta, gravity, platforms, players, explosions)
            projectile.update_screen_offset(screen_offset)
            projectile.render(screen)
        projectiles[:] = [projectile for projectile in projectiles if not projectile.should_die]
            
        for explosion in explosions:
            explosion.update(time_delta, players)
            explosion.update_screen_offset(screen_offset)
            explosion.render(screen)
        explosions[:] = [explosion for explosion in explosions if not explosion.should_die]

        player_index = 0
        for player in players:
            player.update(time_delta, gravity, platforms, projectiles)
            
            # All other players score if a player falls off the platforms
            if player.position[1] > level_size[1]+64:
                player.reset(players, platforms)
                for scoring_player in players:
                    if player != scoring_player:
                        scoring_player.score += 1
                        
            player.update_screen_offset(screen_offset)
            player.render(screen)
            score_string = "Score: " + str(player.score) 
            score_text_render = font.render(score_string, True, player.score_colour)
            x_score_position = 0
            if player_index == 0:
                x_score_position += 50
            elif player_index == len(players)-1:
                x_score_position = x_score_position - 150
            if len(players) > 1:
                x_score_position += (player_index * (800/(len(players)-1)))
            score_text_render_rect = score_text_render.get_rect(x=x_score_position, centery=20)
            screen.blit(score_text_render, score_text_render_rect)
            player.draw_active_power_up_icons_and_timers(screen, [x_score_position, 40])
            player_index += 1

        pygame.display.flip()  # flip all our drawn stuff onto the screen

    pygame.quit()  # exited game loop so quit pygame


if __name__ == '__main__':
    main()
