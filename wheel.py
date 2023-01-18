# import statements
from random import randint
from typing import final
import random
import pygame
import util
clock = pygame.time.Clock()


class Wheel:

    def __init__(self):
        self.wheel_image = pygame.image.load(
            util.resourcePath('images/wheel_rnd1.png'))

        self.wheel_image = pygame.transform.smoothscale(
            self.wheel_image, (375, 375))

        self.round = 1

        # Number of degrees wheel has spun
        self.cur_angle = 0
        self.degs_to_spin = 0
        self.cat0 = 15
        self.lose_turn = 1*(15+30)
        self.cat1 = 1*(15+30*2)
        self.free_turn = 1*(15+30*3)
        self.cat2 = 1*(15+30*4)
        self.bankrupt = 1*(15+30*5)
        self.cat3 = 1*(15+30*6)
        self.play_choice = 1*(15+30*7)
        self.cat4 = 1*(15+30*8)
        self.opp_choice = 1*(15+30*9)
        self.cat5 = 1*(15+30*10)
        self.spin_again = 1*(15+30*11)
        self.cat6 = 1*(15+30*12)

    def update(self):
        self.wheel_image = pygame.image.load(
            util.resourcePath('images/wheel_rnd2.png'))
        self.wheel_image = pygame.transform.smoothscale(
            self.wheel_image, (375, 375))
        self.cur_angle = 0
        self.round = 2

    def drawTick(self, surface):
        pygame.draw.polygon(surface, (0, 0, 0),
                            ((345, 63), (355, 63), (350, 73)))

    def draw(self, surface):
        img = self.wheel_image
        img_copy = img.copy()
        wheel_disp = pygame.transform.rotozoom(img_copy, self.cur_angle, 1)
        pygame.draw.polygon(surface, (0, 0, 0),
                            ((345, 61), (355, 61), (350, 71)))
        self.drawTick(surface)
        surface.blit(wheel_disp, (350 - int(wheel_disp.get_width() / 2),
                                  250 - int(wheel_disp.get_height() / 2)))
        self.drawTick(surface)

    def set_angle(self, spin_result):
        # game logic
        if type(spin_result) == str:
            if spin_result == 'lose turn':
                new_angle = self.lose_turn
            elif spin_result == 'free turn':
                new_angle = self.free_turn
            elif spin_result == 'bankrupt':
                new_angle = self.bankrupt
            elif spin_result == 'player\'s choice':
                new_angle = self.play_choice
            elif spin_result == "opponent's choice":
                new_angle = self.opp_choice
            elif spin_result == "spin again":
                new_angle = self.spin_again

        else:  # spin result  is a category number
            if spin_result == 0:
                if self.round == 1:
                    new_angle = self.cat1
                else:
                    new_angle = self.cat6
            elif spin_result == 1:
                if self.round == 1:
                    new_angle = self.cat2
                else:
                    new_angle = self.cat1
            elif spin_result == 2:
                if self.round == 1:
                    new_angle = self.cat3
                else:
                    new_angle = self.cat2
            elif spin_result == 3:
                if self.round == 1:
                    new_angle = self.cat4
                else:
                    new_angle = self.cat3
            elif spin_result == 4:
                if self.round == 1:
                    new_angle = self.cat5
                else:
                    new_angle = self.cat4
            elif spin_result == 5:
                if self.round == 1:
                    new_angle = self.cat6
                else:
                    new_angle = self.cat5

        diff = new_angle - self.cur_angle
        self.degs_to_spin = diff + 360
        self.cur_angle = new_angle

    def spin(self, surface):
        # mainClock = pygame.time.Clock()
        img = self.wheel_image

        pygame.draw.polygon(surface, (0, 0, 0),
                            ((345, 61), (355, 61), (350, 71)))

        # Loop ------------------------------------------------------- #
        for angle in range(0, self.degs_to_spin, 2):
            pygame.draw.polygon(surface, (0, 0, 0),
                                ((345, 61), (355, 61), (350, 71)))
            self.drawTick(surface)
            img_copy = pygame.transform.rotate(img, angle)
            surface.blit(img_copy, (350 - int(img_copy.get_width() / 2),
                                    250 - int(img_copy.get_height() / 2)))
            self.drawTick(surface)

            # Update ------------------------------------------------- #
            pygame.display.update()