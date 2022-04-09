# -*- coding: utf-8 -*-

import pygame, sys,os
import math
import settings
import Bullet
from utilities import load_image

class Airplane:
    def __init__(self,position_vector=(0,0),speed_vector=(0,0),num_img=0):
        if num_img == 0:
            self.name = "Airplane-1"
        elif num_img == 1:
            self.name = "Airplane-2"
        else:
          self.name = "Un-Airplane"

        self.position_vector = position_vector      # вектор позиции
        self.speed_vector = speed_vector            # вектор скорости
        self.accel_vector = (0,0)                   # вектор ускорения
        self.dir = None                             # направление
        self.angle = 8                              # угол поворота в градусах
        self.drawing_surf = pygame.Surface((45,45), pygame.SRCALPHA)
        self.rect = self.drawing_surf.get_rect()
        self.rect.x, self.rect.y = (self.position_vector)
        self.num_img = num_img                      # номер картинки(1го игрока - 0 , 2го - 1)
        self.d_acsel = 2                            # ускорение вектора скорости
        self.dir_of_accel = None                    # направление ускорения
        self.gravity_vector = (0,-0.5)              # вектор тяжести
        self.status_of_parallel_motion = False      # статус паралельного движения
        self.bullets = []                           # пули
        self.status_fire = True                     # возможность стрельбы
        self.press_button_fire = False              # статус клавиши огонь (пробел)
        self.fire_rate = 3                          #Темп стрельбы, раз в сек
        self.delay_to_fire  = 0                     # дилэй с предыдушего выстрела
        self.number_bullets = 0                     # кол-во пуль
        self.angle_of_rotate = -45                  # угол поворота
        self.images = [load_image('airplane.PNG',alpha_cannel=1),load_image('second_airplane.png',alpha_cannel=1)]
        self.hp = 5                                 # кол-во хп
        self.rendering_hit = 0
        self.key_left= None
        self.key_right= None
        self.key_up= None
        self.key_down= None
        self.key_fire= None
        self.status_airplane = True                 # состояние самолета (True - не убит/False - убит)
        self.keys = []
        self.keys_state = 0b00000 #Состояние функциональных клавишь
        #1бит - клавиша влево, 2 - вправо, 3 - вверх, 4 - вниз, 5 - огонь

    def set_keys(self,left,right,up,down,fire):
        self.key_left= left
        self.key_right= right
        self.key_up= up
        self.key_down= down
        self.key_fire= fire
        self.keys = [self.key_left,self.key_right,self.key_up,self.key_down,self.key_fire]

    def set_state(self, event_key):
        """
        Функцию вызывать когда нажата/отпущена кнопка, event_key - событие нажатия кнопки
        Изменяет переменную keys_state в зависимости от нажатых кнопок
        Пример: Если нажаты функциональные кнопки вверх и влево, то keys_state = 0b10100
        """

        keys = [self.key_left, self.key_right, self.key_up, self.key_down, self.key_fire] #Список функциональных клавиш
        if event_key.key in keys: #Обрабатываем только нужные клавиши
            if event_key.type == pygame.KEYDOWN:
             self.keys_state = self.keys_state | (0b10000 >> keys.index(event_key.key))
            if event_key.type == pygame.KEYUP:
             self.keys_state = self.keys_state ^ (0b10000 >> keys.index(event_key.key))

    def bin_mask(self):
        """
        Проверка зажатых комбинаций кнопок, с использованием битовой маски
        На данный момент функция ничего не принимает и ничего не возвращает, реализуйте как вам удобнее
        """
        #global keys_state #используем глобальную переменную, в которой хранится состояние нажатых клавишь
        #Список используемых масок
        mask_left_right = 0b11000 #Если одновременно зажаты клавиши "лево" "право", состояние остальных не интересно
        mask_up_down = 0b00110
        mask_left = 0b10000
        mask_right = 0b01000
        mask_up = 0b00100
        mask_down = 0b00010
        mask_fire = 0b00001
        mask_left_up = 0b10100
        mask_left_down = 0b10010
        mask_right_up = 0b01100
        mask_right_down = 0b01010


        if self.keys_state & mask_left_right == mask_left_right:
            self.dir = None

        elif self.keys_state & mask_up_down == mask_up_down:
            self.dir_of_accel = None

        elif self.keys_state & mask_left == mask_left:
            self.dir = "left"

        elif self.keys_state & mask_right == mask_right:
            self.dir = "right"

        elif self.keys_state & mask_up == mask_up:
            self.dir_of_accel = "up"

        elif self.keys_state & mask_down == mask_down:
            self.dir_of_accel = "down"

        if self.keys_state & mask_left_up == mask_left_up:
            self.dir_of_accel = "up"
        elif self.keys_state & mask_right_up == mask_right_up:
            self.dir_of_accel = "up"

        if self.keys_state & mask_left_down == mask_left_down:
            self.dir_of_accel = "down"
        elif self.keys_state & mask_right_down == mask_right_down:
            self.dir_of_accel = "down"

        if self.keys_state & mask_fire == mask_fire:
            self.press_button_fire = True

    def event(self, event):
        '''
        обработка событий
        '''

        if event.type == pygame.KEYUP:    # или поднята
            if event.key in self.keys:
                if event.key == self.key_left or event.key == self.key_right: # то направление отсутствует
                    self.dir = None
                if event.key == self.key_up or event.key == self.key_down: # то ускорение отсутствует
                    self.dir_of_accel = None
                if event.key == self.key_fire: # то статус огня = False
                    self.press_button_fire = False
        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            self.set_state(event)
            self.bin_mask()


    def set_angle(self, angle):
        self.angle_of_rotate = angle


    def turning(self,dt,change_speed_vector): # поворачиваем объект

        self.angle_speed = self.angle/100*dt        # расчитываем угол поворота

        if self.dir == 'left':      # поворот влево
            change_speed_vector = (change_speed_vector[0]*math.cos(math.radians(self.angle_speed*(-1))) -
                                 change_speed_vector[1]*math.sin(math.radians(self.angle_speed*(-1))),
                                 change_speed_vector[0]*math.sin(math.radians(self.angle_speed*(-1))) +
                                 change_speed_vector[1]*math.cos(math.radians(self.angle_speed*(-1))))


        elif self.dir == 'right':   # поворот вправо
            change_speed_vector = (change_speed_vector[0]*math.cos(math.radians(self.angle_speed)) -
                                 change_speed_vector[1]*math.sin(math.radians(self.angle_speed)),
                                 change_speed_vector[0]*math.sin(math.radians(self.angle_speed)) +
                                 change_speed_vector[1]*math.cos(math.radians(self.angle_speed)))


        self.speed_vector = (change_speed_vector[0]/dt*1000,change_speed_vector[1]/dt*1000) # воссанавливаем вектор скорости

    def update(self, dt):
        """
        Обновляем состояние объекта
        """
        self.turning(dt,self.change_speed(dt)) # поворачиваем объект, если есть направление поворота

        self.accel_speed(dt,self.change_speed(dt))   # ускоряем объект, если есть направление ускорения

        self.gravity(dt,self.change_speed(dt)) # высчитываем вектор скорости с учетом гравитации

        self.move(dt) # перемещаем объеект на вектор скорости

        self.parallel_motion()

        self.rect.x, self.rect.y = (self.position_vector)
        self.number_bullets = len(self.bullets)

        for bull in self.bullets:
            if bull.position() == 0: # если пули на экране нет, то удаляем ее
                self.bullets.remove(bull)
            bull.update(dt)     # вызываем метод update и draw
            bull.draw()

        if self.press_button_fire==True and self.status_fire==True: 
            self.fire()
            self.status_fire = False
            self.delay_to_fire -= 1000/self.fire_rate
        elif self.status_fire == False:
            self.delay_to_fire +=dt
            if self.delay_to_fire>(1000/self.fire_rate):
                self.status_fire = True

    def parallel_motion(self):
        if self.position_vector[0]<0:         # если объект заходит за границы слева то
            self.status_of_parallel_motion = True # cтатус становится True
            self.position_vector_2 = self.position_vector #вектор позиции параллельного движения равен вектору позиции
            self.position_vector = (self.position_vector[0]+settings.RES_X, # вектор позициии выходит с правого края
                                    self.position_vector[1])
        elif self.position_vector[1]<0:
            self.status_of_parallel_motion = True # cтатус становится True
            self.position_vector_2 = self.position_vector #вектор позиции параллельного движения равен вектору позиции
            self.position_vector = (self.position_vector[0], # вектор позициии выходит с правого края
                                    self.position_vector[1]+settings.RES_Y)
        elif self.position_vector[0]>settings.RES_X: # если объект заходит за границы справа то
            self.status_of_parallel_motion = True   # cтатус становится True
            self.position_vector_2 = self.position_vector #вектор параллельного движения равен вектору позиции
            self.position_vector = (self.position_vector[0]-settings.RES_X,# вектор позициии выходит с левого края
                                    self.position_vector[1])
        elif self.position_vector[1]>settings.RES_Y:
            self.status_of_parallel_motion = True # cтатус становится True
            self.position_vector_2 = self.position_vector #вектор позиции параллельного движения равен вектору позиции
            self.position_vector = (self.position_vector[0], # вектор позициии выходит с правого края
                                    self.position_vector[1]-settings.RES_Y)
        else:
            self.status_of_parallel_motion = False # иначе вектор позиции параллельного движения равен False

    def change_speed(self,dt): # расчитываем измененный вектор скорости
        change_speed_vector = (self.speed_vector[0]/1000*dt,self.speed_vector[1]/1000*dt)
        return change_speed_vector

    def move(self,dt): # передвигаем объект на вектор скорости
        self.position_vector = (self.position_vector[0] + self.change_speed(dt)[0],
                                self.position_vector[1] + self.change_speed(dt)[1])

    def accel_speed(self, dt,change_speed_vector):
        """
        Ускоряем объект
        """
        
        print(change_speed_vector)
        width_vector = math.sqrt(change_speed_vector[0]**2+change_speed_vector[1]**2)   # высчитываем длинну вектора скорости

	if width_vector == 0:
		normal_vector = (width_vector, width_vector)
	else:
		normal_vector = (change_speed_vector[0]/width_vector,change_speed_vector[1]/width_vector)

        if self.dir_of_accel:
            self.accel_vector = ((change_speed_vector[0]/width_vector*self.d_acsel)/1000*dt, # рассчитываем вектор ускорения
                                     (change_speed_vector[1]/width_vector*self.d_acsel)/1000*dt) # если есть направление ускрения
        else:                                                                                # иначе вектор ускорения равен (0,0)
            self.accel_vector =(0,0)

        if self.dir_of_accel == 'up' and width_vector < 6 * math.sqrt(normal_vector[0]**2 + normal_vector[1]**2):                                      # если направление ускорения вверх
            change_speed_vector = (change_speed_vector[0]+self.accel_vector[0],
                            change_speed_vector[1]+self.accel_vector[1])     # прибовляем к ветору скорости вектор ускорения

        elif self.dir_of_accel == 'down' and width_vector >  math.sqrt(normal_vector[0]**2 + normal_vector[1]**2):                                  # если направление ускорения вниз
            change_speed_vector = (change_speed_vector[0]-self.accel_vector[0],
                            change_speed_vector[1]-self.accel_vector[1])     # вычитаем к ветору скорости вектор ускорения

        self.speed_vector = (change_speed_vector[0]/dt*1000, # воссанавливаем вектор скорости
                            change_speed_vector[1]/dt*1000)

    def gravity(self, dt,change_speed_vector): # измениям вектор скорости с учетом гравитации

        gravity_vector = (self.gravity_vector[0]/1000*dt, # высчитываем вектор скорости независимый от фпс
                          self.gravity_vector[1]/1000*dt)

        change_speed_vector=(change_speed_vector[0]-gravity_vector[0],# высчитываем ветор скорости независимый о фпс
                             change_speed_vector[1]-gravity_vector[1])

        self.speed_vector = (change_speed_vector[0]/dt*1000, # воссанавливаем вектор скорости
                             change_speed_vector[1]/dt*1000)

    def fire(self): # добавляем в список пуль 1 пулю
        self.bullets.append(Bullet.Bullet((self.position_vector[0]-25,self.position_vector[1]-25),self.speed_vector,num_airplane = self.num_img))

    def collide_bullet_with_airplane(self,airplane): # проверка сталкивания пули с самолетом

        bullets = airplane.bullets

        if self.rect.collidelistall(bullets): # если список индексов сталкивающихся пуль не пуст
            self.rendering_hit = 1
            for index in self.rect.collidelistall(bullets): # то мы удаляем столкнувшиеся пули
                bullets.remove(bullets[index])
                self.damage()

        if self.rect.colliderect(airplane.rect)==True:
            self.status_airplane = False
            self.hp = 0


    def damage(self):               # наносим урон
        self.hp -= 1
        if self.hp == 0:
            self.status_airplane = False

    def __repr__(self):
        return self.name

    def render(self,screen): # блитуем

        if self.rendering_hit > 0:
            self.rendering_hit+=1
            if self.rendering_hit == 15:
                self.rendering_hit = 0
        if self.hp != 0:
            len_vector_speed = math.sqrt(self.speed_vector[0]**2+self.speed_vector[1]**2)

            normal_speed_vector =(self.speed_vector[0]/len_vector_speed,self.speed_vector[1]/len_vector_speed)

            self.angle_of_rotate = math.acos(normal_speed_vector[0])*180/math.pi
            if self.speed_vector[1]>0:
                self.angle_of_rotate *= -1
            else:
                self.angle_of_rotate = math.fabs(self.angle_of_rotate)

            rotated_airplane_img = pygame.transform.rotate(self.images[self.num_img],self.angle_of_rotate) # поворачиваем картинку аэроплана
            rect_img = rotated_airplane_img.get_rect()

            rect_img.center = self.position_vector  # центр картинки приравниваем вектору позиции

            screen.blit(rotated_airplane_img, rect_img) # блитуем все на скрин
        else:
            screen.blit(load_image('collision.png',alpha_cannel=1),(self.position_vector[0]-25,self.position_vector[1]-25))


        if self.rendering_hit!=0:
            screen.blit(load_image('hit.png',alpha_cannel=1),(self.position_vector[0]-15,self.position_vector[1]-15))

        if self.status_of_parallel_motion == True: # если статус параллельного движения True
            screen.blit(rotated_airplane_img, self.position_vector_2)# то блитуем паралельный объект

        #отрисовывываем пули
        if self.status_airplane == True:
            for bull in self.bullets:
                bull.render(screen)

    def render_hp(self,screen):
        if self.name == "Airplane-1":
            if self.hp == 5:
                screen.blit(load_image('hp_5.png',alpha_cannel=1),(260,0))
            elif self.hp == 4:
                screen.blit(load_image('hp_4.png',alpha_cannel=1),(260,0))
            elif self.hp == 3:
                screen.blit(load_image('hp_3.png',alpha_cannel=1),(260,0))
            elif self.hp == 2:
                screen.blit(load_image('hp_2.png',alpha_cannel=1),(260,0))
            elif self.hp == 1:
                screen.blit(load_image('hp_1.png',alpha_cannel=1),(260,0))

        elif self.name == "Airplane-2":
            if self.hp == 5:
                screen.blit(load_image('hp_5.png',alpha_cannel=1),(650,0))
            elif self.hp == 4:
                screen.blit(load_image('hp_4.png',alpha_cannel=1),(689,0))
            elif self.hp == 3:
                screen.blit(load_image('hp_3.png',alpha_cannel=1),(728,0))
            elif self.hp == 2:
                screen.blit(load_image('hp_2.png',alpha_cannel=1),(767,0))
            elif self.hp == 1:
                screen.blit(load_image('hp_1.png',alpha_cannel=1),(806,0))















