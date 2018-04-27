import pygame
from pygame.locals import *

import math
import random

from game.bomb_weapon import BombWeapon
from machine_gun_weapon import MachineGunWeapon
from game.aim_reticule import Reticule


class ControlScheme:

    def __init__(self):

        self.left = K_LEFT
        self.right = K_RIGHT
        self.jump = K_RSHIFT
        self.fire = K_RCTRL
        
        self.aimUp = K_UP
        self.aimDown = K_DOWN


class Player:

    def __init__(self, players, platforms, sprite_y_offset, controls):
        self.sprite_y_offset = sprite_y_offset
        self.controls = controls
        self.score = 0
        if sprite_y_offset == 0:
            self.score_colour = pygame.Color(50,130,141,255)
        else:
            self.score_colour = pygame.Color(242,95,151)
        self.start_pos = [0.0, 0.0]
                
        self.get_random_unoccupied_start_platform(players, platforms)
        
        self.velocity = [0.0, 0.0]
        self.rect = pygame.Rect((self.start_pos[0] - 16, self.start_pos[1] - 32), (32, 64))
        self.screen_rect = pygame.Rect((self.start_pos[0] - 16, self.start_pos[1] - 32), (32, 64))
        self.tall_collision_rect = pygame.Rect((self.start_pos[0] - 15, self.start_pos[1] - 32), (30, 64))
        self.wide_collision_rect = pygame.Rect((self.start_pos[0] - 16, self.start_pos[1] - 31), (32, 62))
             
        self.position = [float(self.start_pos[0]), float(self.start_pos[1])]
        self.screen_position = [float(self.start_pos[0]), float(self.start_pos[1])]
    
        self.terminal_velocity = 8000.0
        
        self.collided = False

        self.collided_left = False
        self.collided_right = False
        self.collided_down = False
        self.collided_up = False

        self.left_pressed = False
        self.right_pressed = False
        self.x_acceleration = 0.0

        self.base_aim_angle = 0
        self.aim_angle = 0
        self.increase_aim_angle = False
        self.decrease_aim_angle = False

        self.fire_key_pressed = False
        self.fire_key_released = False
        self.fire_key_held = False

        self.movement_velocity = [0.0, 0.0]
        self.physics_velocity = [0.0, 0.0]
        self.last_move_left = False

        self.run_cycle_images = []
        self.run_sprite_sheet = None
        self.cycle_image_time = 0.08
        self.current_run_cycle_frame = 0
        self.cycle_image_acc = 0.0
        self.all_player_sprites = None
        self.sprite = None
        self.stand_sprite_image = None
        self.setup_sprite_graphics()
        self.reticule = Reticule(self.screen_position, self)

        self.jump_pressed = False
        self.air_jumps = 0

        self.active_power_ups = {}

        self.power_up_duration = 12.0

        self.power_up_icon_dict = {"double_jump": pygame.image.load("images/double_jump_power_up.png"),
                                   "machine_gun": pygame.image.load("images/machine_gun_power_up.png"),
                                   "explosion": pygame.image.load("images/explosion_power_up.png")}

        self.power_up_timer_bg_col = pygame.Color(0, 0, 0, 255)
        self.powerUpTimerMainCol = pygame.Color(200,50,50,255)

        self.bomb_weapon = BombWeapon()
        self.machine_gun_weapon = MachineGunWeapon()
        self.active_weapon = self.bomb_weapon
        self.fireBomb = False

    def update_weapon_power_ups(self):
        if self.is_active_power_up("explosion"):
            self.active_weapon.make_weapon_more_explosive()
        else:
            self.active_weapon.make_weapon_normal()

        if self.is_active_power_up("machine_gun"):
            self.active_weapon = self.machine_gun_weapon
        else:
            self.active_weapon = self.bomb_weapon

    def add_active_power_up(self, type_name):
        self.active_power_ups[type_name] = self.power_up_duration
        
    def is_active_power_up(self, name):
        is_active = False
        if name in self.active_power_ups:
            is_active = True
        return is_active

    def draw_active_power_up_icons_and_timers(self, screen, start_position):
        start_pos = [start_position[0], start_position[1]]
        timer_pos = [start_position[0] + 20, start_position[1]]
        for name, time in self.active_power_ups.items():
            icon_rect = pygame.Rect(start_pos, (16, 16))
            timer_bg_rect = pygame.Rect(timer_pos, (100, 16))
            timer_width = int((time / self.power_up_duration) * 98)
            timer_main_rect = pygame.Rect([timer_pos[0]+1, timer_pos[1]+1], (timer_width, 14))
            screen.blit(self.power_up_icon_dict[name], icon_rect)
            pygame.draw.rect(screen, self.power_up_timer_bg_col, timer_bg_rect, 1)
            pygame.draw.rect(screen, self.powerUpTimerMainCol, timer_main_rect)
            start_pos[1] += 20
            timer_pos[1] += 20

    def get_random_unoccupied_start_platform(self, players, platforms):
        random_platform = random.choice(platforms)
        self.start_pos = [random_platform.rect.centerx, random_platform.rect.centery - (64 / 2 + 10)]

        if len(players) > 0 and len(platforms) > 1:
            while True:
                shortest_x_dist_from_others = 10000.0
                # try to find out if we are on an already occupied platform
                for player in players:
                    if player != self:
                        x_dist = abs(player.position[0] - self.start_pos[0])
                        y_dist = abs(player.position[1] - self.start_pos[1])
                        if y_dist < 25.0:
                            if x_dist < shortest_x_dist_from_others:
                                shortest_x_dist_from_others = x_dist
                if shortest_x_dist_from_others > 200.0:
                    break
                random_platform = random.choice(platforms)
                self.start_pos = [random_platform.rect.centerx, random_platform.rect.centery - (64 / 2 + 10)]

    def setup_sprite_graphics(self):
        self.run_cycle_images = []
        self.run_sprite_sheet = pygame.image.load("images/character.png")
        for x in range(0, 8):
            self.run_cycle_images.append(
                self.run_sprite_sheet.subsurface(pygame.Rect(x * 64, self.sprite_y_offset, 64, 88)))
        self.run_cycle_images.append(
            self.run_sprite_sheet.subsurface(pygame.Rect(0, self.sprite_y_offset + 88, 64, 88)))
        self.run_cycle_images.append(
            self.run_sprite_sheet.subsurface(pygame.Rect(64, self.sprite_y_offset + 88, 64, 88)))

        self.stand_sprite_image = self.run_sprite_sheet.subsurface(pygame.Rect(128, self.sprite_y_offset + 88, 64, 88))

        self.all_player_sprites = pygame.sprite.Group()
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = self.run_cycle_images[0]
        self.sprite.rect = self.sprite.image.get_rect()
        self.sprite.rect.center = self.screen_position

        self.all_player_sprites.add(self.sprite)

        self.cycle_image_time = 0.08
        self.cycle_image_acc = 0.0
        self.current_run_cycle_frame = 0

    @staticmethod
    def make_random_start_vector():
        # make a normalised angle aiming roughly toward one of the goals
        y_random = random.uniform(-0.5, 0.5)
        x_random = 1.0 - abs(y_random)

        if random.randint(0, 1) == 1:
            x_random = x_random * -1.0
        
        return [x_random, y_random]

    def set_rects_to_position(self):
        self.rect.centerx = self.position[0]
        self.rect.centery = self.position[1]
        self.tall_collision_rect.centerx = self.position[0]
        self.tall_collision_rect.centery = self.position[1]
        self.wide_collision_rect.centerx = self.position[0]
        self.wide_collision_rect.centery = self.position[1]

    def reset(self, players, platforms):
        self.get_random_unoccupied_start_platform(players, platforms)
        self.position = [self.start_pos[0], self.start_pos[1]]
        
        self.collided = False

        self.collided_left = False
        self.collided_right = False
        self.collided_down = False
        self.collided_up = False

        self.left_pressed = False
        self.right_pressed = False
        self.x_acceleration = 0.0

        self.base_aim_angle = 0
        self.aim_angle = 0
        self.increase_aim_angle = False
        self.decrease_aim_angle = False

        self.fireBomb = False

        self.movement_velocity = [0.0, 0.0]
        self.physics_velocity = [0.0, 0.0]
        self.last_move_left = False
        self.set_rects_to_position()

        self.active_power_ups.clear()

        self.fire_key_pressed = False
        self.fire_key_released = False
        self.fire_key_held = False

    def process_event(self, event):
        if event.type == KEYDOWN:
            if event.key == self.controls.aimUp:
                self.increase_aim_angle = True
            if event.key == self.controls.aimDown:
                self.decrease_aim_angle = True
                
            if event.key == self.controls.jump:
                self.jump_pressed = True
            if event.key == self.controls.left:
                self.left_pressed = True
            if event.key == self.controls.right:
                self.right_pressed = True
            if event.key == self.controls.fire:
                self.fire_key_pressed = True
                
        if event.type == KEYUP:
            if event.key == self.controls.left:
                self.left_pressed = False
            if event.key == self.controls.right:
                self.right_pressed = False
                
            if event.key == self.controls.aimUp:
                self.increase_aim_angle = False
            if event.key == self.controls.aimDown:
                self.decrease_aim_angle = False

            if event.key == self.controls.fire:
                self.fire_key_released = True

    def apply_force_from(self, strength, origin):
        x_dist = self.position[0] - origin[0]
        y_dist = self.position[1] - origin[1]
        distance = math.sqrt((x_dist ** 2) + (y_dist ** 2))
        
        force_vec = [x_dist/distance, y_dist/distance]

        self.physics_velocity[1] += strength * force_vec[1]
        self.physics_velocity[0] += strength * force_vec[0]

    # work out player jumping
    def update_jump(self):
        if self.jump_pressed:
            self.jump_pressed = False
            if self.collided_down:  # regular jumping
                self.movement_velocity[1] -= 500.0
            elif self.is_active_power_up("double_jump") and self.air_jumps == 0:  # double jumping
                self.air_jumps += 1
                if self.velocity[1] < 0.0:
                    self.movement_velocity[1] -= max(0.0, (500 - abs(self.velocity[1])))
                else:
                    self.movement_velocity[1] -= 500.0

    def update_power_up_timers(self, dt):
        # update power up times and remove inactive power ups
        for name, time in self.active_power_ups.items():
            self.active_power_ups[name] -= dt
        self.active_power_ups = {name: time for name, time in self.active_power_ups.items() if time > 0.0}

    def update(self, dt, gravity, platforms, projectiles):

        self.update_power_up_timers(dt)
        self.update_jump()
        self.update_weapon_power_ups()
     
        if self.velocity[0] > 0.0:
            self.last_move_left = False
        elif self.velocity[0] < 0.0:
            self.last_move_left = True

        if self.collided_down:
            if self.cycle_image_acc > self.cycle_image_time:
                self.current_run_cycle_frame += 1
                if self.current_run_cycle_frame > 9:
                    self.current_run_cycle_frame = 0
                self.cycle_image_acc = 0.0
                
                if self.x_acceleration == 0.0:
                    self.current_run_cycle_frame = 0
                    self.cycle_image_acc = 0.0
                    if self.last_move_left:
                        self.sprite.image = pygame.transform.flip(self.stand_sprite_image, True, False)
                    else:
                        self.sprite.image = self.stand_sprite_image
                        
                elif self.velocity[0] > 0.0:
                    self.sprite.image = self.run_cycle_images[self.current_run_cycle_frame]
                else:
                    self.sprite.image = pygame.transform.flip(self.run_cycle_images[self.current_run_cycle_frame],
                                                              True, False)
            else:
                self.cycle_image_acc += dt
        else:
            if self.last_move_left:
                if self.velocity[1] < 0:
                    self.sprite.image = pygame.transform.flip(self.run_cycle_images[0], True, False)
                else:
                    self.sprite.image = pygame.transform.flip(self.run_cycle_images[2], True, False)
                
            else:
                if self.velocity[1] < 0:
                    self.sprite.image = self.run_cycle_images[0]
                else:
                    self.sprite.image = self.run_cycle_images[2]

        if self.increase_aim_angle:
            self.base_aim_angle -= dt * math.pi
            if self.base_aim_angle <= -math.pi/2:
                self.base_aim_angle = -math.pi / 2
        if self.decrease_aim_angle:
            self.base_aim_angle += dt * math.pi
            if self.base_aim_angle >= math.pi/2:
                self.base_aim_angle = math.pi / 2
            
        if self.last_move_left:
            self.aim_angle = math.pi - self.base_aim_angle
        else:
            self.aim_angle = self.base_aim_angle

        if self.fire_key_pressed:
            self.fire_key_pressed = False
            self.fire_key_held = True
            self.active_weapon.fire_key_pressed(self, projectiles)

        if self.fire_key_released:
            self.fire_key_released = False
            self.fire_key_held = False

        if self.fire_key_held:
            self.active_weapon.fire_key_held(dt, self, projectiles)

        if self.collided_down and not (self.left_pressed or self.right_pressed):
            self.x_acceleration = 0.0

        if self.right_pressed:
            if not self.collided_right:
                if self.collided_down:
                    if self.x_acceleration < 0.0:
                        self.x_acceleration = 0.0
                    self.x_acceleration += 600.0 * dt
                    if self.x_acceleration > 300.0:
                        self.x_acceleration = 300.0
                else:
                    self.x_acceleration += 300 * dt
                    if self.x_acceleration > 300.0:
                        self.x_acceleration = 300.0
            else:
                self.x_acceleration = 0.0
                
        if self.left_pressed:
            if not self.collided_left:
                if self.collided_down:
                    if self.x_acceleration > 0.0:
                        self.x_acceleration = 0.0
                        
                    self.x_acceleration -= 600.0 * dt
                    if self.x_acceleration < -300.0:
                        self.x_acceleration = -300.0
                else:
                    self.x_acceleration -= 300 * dt
                    if self.x_acceleration < -300.0:
                        self.x_acceleration = -300.0
            else:
                self.x_acceleration = 0.0

        if self.collided_left and self.x_acceleration < 0.0:
            self.x_acceleration = 0.0

        if self.collided_right and self.x_acceleration > 0.0:
            self.x_acceleration = 0.0

        self.movement_velocity[0] = self.x_acceleration

        # apply gravity to our ball's velocity every frame
        if not self.collided_down:
            self.physics_velocity[0] = self.physics_velocity[0] + dt * gravity[0]
            self.physics_velocity[1] = self.physics_velocity[1] + dt * gravity[1]

            # make sure we don't accelerate our ball forever
            if self.physics_velocity[1] > self.terminal_velocity:
                self.physics_velocity[1] = self.terminal_velocity

        if self.collided_down:
            self.physics_velocity[0] *= 0.008 ** dt
            if abs(self.physics_velocity[0]) < 0.1:
                self.physics_velocity[0] = 0.0

            if self.velocity[0] > 0.0 > self.physics_velocity[0]:
                self.physics_velocity[0] = 0.0
            if self.velocity[0] < 0.0 < self.physics_velocity[0]:
                self.physics_velocity[0] = 0.0

        # apply our player's velocity to it's position
        self.velocity[0] = self.movement_velocity[0] + self.physics_velocity[0]
        self.velocity[1] = self.movement_velocity[1] + self.physics_velocity[1]

        collided_left = False
        collided_right = False
        collided_up = False
        collided_down = False
        for platform in platforms:
            if self.wide_collision_rect.colliderect(platform.rect):
                if self.wide_collision_rect.left <= platform.rect.right <= self.wide_collision_rect.right:
                    collided_left = True
                    if not self.collided_left:
                        if self.velocity[0] < 0.0:
                            self.velocity[0] = 0.0
                            self.physics_velocity[0] = 0.0
                elif self.wide_collision_rect.right >= platform.rect.left >= self.wide_collision_rect.left:
                    collided_right = True
                    if not self.collided_right:
                        if self.velocity[0] > 0.0:
                            self.velocity[0] = 0.0
                            self.physics_velocity[0] = 0.0
                            
            if self.tall_collision_rect.colliderect(platform.rect):
                if self.tall_collision_rect.bottom >= platform.rect.top >= self.tall_collision_rect.top:
                    collided_down = True
                    collide_distance = self.tall_collision_rect.bottom - platform.rect.top
                    if collide_distance > 1:
                        self.position[1] -= collide_distance - 1
                    if not self.collided_down:
                        # stop the player dead when we hit top of platform for the first time
                        self.air_jumps = 0
                        self.velocity[1] = 0.0
                        self.physics_velocity[1] = 0.0
                        self.movement_velocity[1] = 0.0
                elif self.tall_collision_rect.top <= platform.rect.bottom <= self.tall_collision_rect.bottom:
                    collided_up = True
                    if not self.collided_up:
                        self.velocity[1] = 0.0
                        self.physics_velocity[1] = 0.0
                        self.movement_velocity[1] = 0.0

        if collided_left or collided_right:
            self.physics_velocity[0] = 0.0
        if collided_down:
            self.physics_velocity[1] = 0.0
            
        self.collided_left = collided_left
        self.collided_right = collided_right
        self.collided_up = collided_up
        self.collided_down = collided_down

        self.position[0] = self.position[0] + dt * self.velocity[0]
        self.position[1] = self.position[1] + dt * self.velocity[1]

        self.set_rects_to_position()

        self.reticule.update()

    def update_screen_offset(self, screen_offset):
        self.screen_position[0] = self.position[0] - screen_offset[0]
        self.screen_position[1] = self.position[1] - screen_offset[1]
        self.screen_rect.x = self.rect.x - screen_offset[0]
        self.screen_rect.y = self.rect.y - screen_offset[1]
        self.sprite.rect.centerx = self.screen_position[0]
        self.sprite.rect.centery = self.screen_position[1]-12
        
    def get_screen_offset(self, screen_size, level_size):
        screen_offset = [0.0, 0.0]
        if screen_size[1]/2 < self.position[1] < level_size[1] - screen_size[1]/2:
            screen_offset[1] = self.position[1] - screen_size[1]/2
        if self.position[1] >= level_size[1] - screen_size[1]/2:
            screen_offset[1] = level_size[1] - screen_size[1]       
            
        return screen_offset

    def render(self, screen):
        self.all_player_sprites.draw(screen)
        self.reticule.render(screen)
