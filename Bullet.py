# -*- coding: utf-8 -*-

import pygame,sys,math
import settings
from utilities import load_image

class Bullet:
    def __init__(self,position_vector,speed_vector_airplane,num_airplane):
        self.num_airplane = num_airplane
        self.position_vector = (position_vector[0]+22,position_vector[1]+22)
        self.width_vector = math.sqrt(speed_vector_airplane[0]**2 + speed_vector_airplane[1]**2)
        self.normal_vector = (speed_vector_airplane[0]/self.width_vector*500,
                              speed_vector_airplane[1]/self.width_vector*500)

        self.speed_vector = (speed_vector_airplane[0]+self.normal_vector[0],
                             speed_vector_airplane[1]+self.normal_vector[1])

        self.drawing_surf = pygame.Surface((6,6), pygame.SRCALPHA)
        self.rect = self.drawing_surf.get_rect()

    def update(self,dt):
        self.move(dt)

    def render(self,screen):
        # pygame.draw.rect(screen,(250,0,0),self.rect, 2) # рисуем границы surface
        screen.blit(self.drawing_surf, self.position_vector)

    def move(self,dt):
        self.speed_vector = (self.speed_vector[0]/1000*dt,
                             self.speed_vector[1]/1000*dt)

        self.position_vector = (self.position_vector[0]+self.speed_vector[0],
                                self.position_vector[1]+self.speed_vector[1])

        self.speed_vector = (self.speed_vector[0]/dt*1000,
                             self.speed_vector[1]/dt*1000)
        self.rect.x, self.rect.y = (self.position_vector)

    def draw(self):
        # self.drawing_surf.fill(pygame.SRCALPHA)
        # pygame.draw.circle(self.drawing_surf,(0,0,200), (3,3),2)


        if self.num_airplane == 0:
            self.drawing_surf.blit(load_image('bullet_blue.png',alpha_cannel=1),(0,0))
        elif self.num_airplane == 1:
            self.drawing_surf.blit(load_image('bullet_yellow.png',alpha_cannel=1),(0,0))
    def position(self): # проверка позиции (1 - на экране, 0 за границами экрана)
        screen = pygame.display.get_surface()
        screen_rect = screen.get_rect()
        if screen_rect.collidepoint(self.position_vector) == True:
            return 1
        else:
            return 0
