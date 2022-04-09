# -*- coding: utf-8 -*-

import pygame, sys
from settings import *
from Airplane import Airplane
from utilities import load_image
from Buttons import Button



def settings():
    print('settings')

def pause():
    global GAME_STATUS
    if GAME_STATUS:
        GAME_STATUS = False
    else:
        GAME_STATUS = True



def run():

    airplanes = []
    destroyed_airplanes = []
    airplane = Airplane(position_vector=(70,170),speed_vector=(10,0),num_img=0)# Cоздаем объект
    airplane.set_keys(pygame.K_a,pygame.K_d,pygame.K_w,pygame.K_s,pygame.K_SPACE)

    second_airplane = Airplane(position_vector=(1000,170),speed_vector=(-10,0),num_img=1)# Cоздаем объект
    second_airplane.set_keys(pygame.K_LEFT,pygame.K_RIGHT,pygame.K_UP,pygame.K_DOWN,pygame.K_KP0)

    airplanes.append(airplane)
    airplanes.append(second_airplane)

    clock = pygame.time.Clock() #Создаем таймер для контроля фпс

    button_pause = Button(pos=(535,5),path='images/buttons',image_names =('pause_off.png','pause_hover.png','pause_click.png'),
                    function=pause, text='', w =30 , h = 35)

    interface = load_image('interface2.png',alpha_cannel=1)


    while len(airplanes)>1: #главный цикл программы
        for e in pygame.event.get(): #цикл обработки очереди событий окна
            button_pause.event(e)
            for airplane in airplanes:
                airplane.event(e)
            if e.type == pygame.QUIT:
                sys.exit() #Закрытие окна программы

        dt = clock.tick(FPS)            #Устанавливаем FPS

        if GAME_STATUS == True:
            for airplane in airplanes:
                airplane.update(dt)

        screen.blit(BACKGROUND,(0,0))

        if len(airplanes)>1:
            airplanes[0].collide_bullet_with_airplane(airplanes[1])
            airplanes[1].collide_bullet_with_airplane(airplanes[0])

        for airplane in airplanes:
            airplane.render(screen)


        for airplane in airplanes:
            if airplane.status_airplane == False:
                destroyed_airplanes.append(airplane)
                airplanes.remove(airplane)

        for airplane in destroyed_airplanes:
            airplane.render(screen)

        screen.blit(interface,(0,0))

        button_pause.update(dt)
        button_pause.render(screen)

        for airplane in airplanes:
                airplane.render_hp(screen)

        pygame.display.flip()           #отображаем на мониторе все, что нарисовали на экране

    start_game()


def start_game():
    button_start = Button(pos = (478,240),path='images/buttons',image_names =('start_off.png','start_hover.png','start_click.png'),
                        function=run, w =144, h=35)
    button_players = Button(pos = (478,320),path='images/buttons',image_names =('best_players_off.png','best_players_hover.png','best_players_click.png'),
                        function=run, w =144, h=35)
    button_settings = Button(pos = (478,400),path='images/buttons',image_names =('settings_off.png','settings_hover.png','settings_click.png'),
                        function=run, w =144, h=35)
    button_exit = Button(pos = (478,480),path='images/buttons',image_names =('exit_off.png','exit_hover.png','exit_click.png'),
                        function=sys.exit, w =144, h=35)


    buttons = (button_start,button_players,button_settings,button_exit)



    while True:
        screen.blit(load_image('main_background.png',alpha_cannel=0),(0,0))

        for event in pygame.event.get():
            for button in buttons:
                #Пересылаем все события кнопке
                button.event(event)
                if event.type == pygame.QUIT:
                    sys.exit()

            #Обновляем и отрисовываем кнопку на экране
        for button in buttons:
            button.update(0)
            button.render(screen)

        pygame.display.flip()


pygame.init() #инициализация
display = pygame.display.set_mode((RES_X,RES_Y)) #создание окна
screen = pygame.display.get_surface() #получаем поверхность для рисования

BACKGROUND = load_image("Background.png",alpha_cannel=0) # фон
GAME_STATUS = True# ( True -игра, False - пауза)
start_game()


