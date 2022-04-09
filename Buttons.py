# -*- coding: utf-8 -*-

import pygame,os, sys

"""
Для создания кнопки необходимо передать следующие аргументы:
image_names - кортеж из трех имен картинок для кнопки. 1-Обычное сосояние, 2-при наведении, 3-при нажатии.
path - путь к картинкам, относительно корня проекта. (значения по умолчанию см. в конструкторе класса)
pos - Координаты верхнего левого угла кнопки относительно верхнего левого угла окна программы
function - имя функции, которая запускается при клике на кнопку
parent - оставлено для совместимости с другим проектом
text - надпись на кнопке
w,h - ширина и высота кнопки. Если не заданы, размер кнопки равен размеру картинки. Если задано только одно значение,
размер картинки изменяется пропорционально.
"""


class Button:  #основная кнопка
    def __init__(self,image_names, path='Images/Buttons',pos=(0,0),function=None,parent = None, text = '',w=0,h=0):
        self.image_normal = load_image(image_names[0],alpha_channel=True,dir_name=path)   #изображение кнопки в базовом состоянии
        self.image_on_over = load_image(image_names[1],alpha_channel=True,dir_name=path)  #изображение кнопки в базовом состоянии
        self.image_on_click = load_image(image_names[2],alpha_channel=True,dir_name=path) #изображение кнопки в базовом состоянии
        self.images = [self.image_normal,self.image_on_over,self.image_on_click] #список с кнопками

        if w != 0 and h != 0:             #изменение размера картинки, если заданы ширина и высота
            for i in range(0,3):
                self.images[i] = pygame.transform.scale(self.images[i],(w,h))
        elif w != 0 and h == 0:          #если задан один размер, то второй изменяется пропорционально
            for i in range(0,3):
                rect = self.images[i].get_rect()
                h = int(rect.h*(w/rect.w))
                self.images[i] = pygame.transform.scale(self.images[i],(w,h))
        elif w == 0 and h != 0:
            for i in range(0,3):
                rect = self.images[i].get_rect()
                w = int(rect.w*(h/rect.h))
                self.images[i] = pygame.transform.scale(self.images[i],(w,h))
 
        self.current_image = self.images[0]     #текущая картинка
 
        self.rect = self.current_image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
 
        self.text = Text(text)                  #текст кнопки
        self.text_surf = self.text.font.render(text, True, (0,0,0))   #поверхность текста
        self.rect_text = self.text_surf.get_rect()    #рект текста
        self.rect_text.x = self.rect.x+self.rect.w/2-self.rect_text.w/2  #смещение текста на центр картинки кнопки,
        # к координате кнопки прибавляется половина длины картинки и отнимается половина длины текста
        self.rect_text.y = self.rect.y+self.rect.h/2-self.rect_text.h/2
 
        self.function = function     #функция кнопки
        self.parent = parent         #родитель кнопки, по умолчанию отсутствует
 
    def event(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.check_mouse_coords(event.pos):
                if self.parent:
                    parametrs = self.parent.get_parametrs_for_function() #получает от родителя
                    self.function(parametrs) #вызывает с функцию с передачей аргументов
                elif self.function:
                    self.function()          #если родителя нет, то функция вызывается без передачи аргументов
                self.change_image('click')
 
        if event.type == pygame.MOUSEBUTTONUP:
            if self.check_mouse_coords(event.pos):
                self.change_image('over')
 
        if event.type == pygame.MOUSEMOTION:
            if self.check_mouse_coords(event.pos):       #если курсор на картинке, смена картинки
                self.change_image('over')                 #метод смены картинки
            elif not self.check_mouse_coords(event.pos):
                self.change_image('normal')
 
    def change_image(self,status):   #cмена картинки в зависимости от статуса
        if status == 'normal':
            self.current_image = self.images[0]
        elif status == 'over':
            self.current_image = self.images[1]
        elif status == 'click':
            self.current_image = self.images[2]
 
    def check_mouse_coords(self,xy):           #проверяет, находятся ли координаты мыши в ректе картинки
        if self.rect.collidepoint(xy):
            return True
        else:
            return False
 
    def update(self, dt):
        pass
 
    def render(self,screen):
        screen.blit(self.current_image,self.rect) #на экран рисуется картинка кнопка
        # pygame.draw.rect(screen,(250,0,0),self.rect, 5) # рисуем границы surface
        screen.blit(self.text_surf,self.rect_text)
 
 
class Text:   #простой класс, для вывода текста
    def __init__(self,text,x = 0,y = 0):
        self.x = x
        self.y = y
        self.text = text
        self.font = pygame.font.Font(None, 24)
 

def load_image(name,alpha_channel,dir_name): #функция загрузки картинки (взята из примера)
    fullname = os.path.join(dir_name,name) #путь картинки
    try:
        image = pygame.image.load(fullname) #загрузка картинки
    except (pygame.error):
        print("Cannot load image:", fullname)
        return 0
    if (alpha_channel): #если есть альфа канал, конвертирование картинки с учетом альфа канала
        image = image.convert_alpha()
    else:
        image = image.convert() #если альфа канала нету, конвертирование без учета альфа канала (непонятно зачем, но надо)

    return image
 


#Демонстрация использования класса для создания кнопки
def hello_world():
    print('Hello world!')

if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode((640, 480))
    render_list = []
    #Создаем кнопку
    button = Button(pos = (210,240),image_names =('button_off.png','button_hover.png','button_click.png'),
                    function=hello_world, text='New Button', w =200)


 
    while True:
        screen.fill((10,100,10))
 
        for event in pygame.event.get():
            #Пересылаем все события кнопке
            button.event(event)
            if event.type == pygame.QUIT:
                sys.exit()

        #Обновляем и отрисовываем кнопку на экране
        button.update(0)
        button.render(screen)

 
        pygame.display.flip()





class Window:
    def __init__(self,coords,width,height,control_button):
        self.x = coords[0]
        self.y = coords[1]
        self.width = width
        self.height = height
        self.cotrol_button = control_button
        self.text_cotrol_button = 'a'
        self.image_off = load_image('window_off.png',1,'images')
        self.image_hover = load_image('window_hover.png',1,'images')
        self.image_click = load_image('window_click.png',1,'images')
        self.drawing_image = self.image_off
        self.rect = self.drawing_image.get_rect()
        self.rect.x = coords[0]
        self.rect.y = coords[1]
        self.status_window = False
        self.text = Text(self.cotrol_button)                  #текст кнопки
        self.text_surf = self.text.font.render(self.cotrol_button, True, (0,0,0))   #поверхность текста
        self.rect_text = self.text_surf.get_rect()    #рект текста
        self.second_rect_text = self.rect_text
        self.rect_text.x = self.rect.x+self.rect.w/2-self.rect_text.w/2  #смещение текста на центр картинки кнопки,
        # к координате кнопки прибавляется половина длины картинки и отнимается половина длины текста
        self.rect_text.y = self.rect.y+self.rect.h/2-self.rect_text.h/2


    def check_mouse_coords(self,xy):           #проверяет, находятся ли координаты мыши в ректе картинки
        if self.rect.collidepoint(xy):
            return True
        else:
            return False

    def change_image(self,num_img):
        if num_img == 'off':
            self.drawing_image = self.image_off
        elif num_img == 'hover':
            self.drawing_image = self.image_hover
        elif num_img == 'click':
            self.drawing_image = self.image_click

    def update(self):
        self.text_surf = self.text.font.render(self.text_cotrol_button, True, (0,0,100))   #поверхность текста
        #self.rect_text = self.text_surf.get_rect()    #рект текста

    def event(self,event):
        if self.status_window == False:
            if event.type == pygame.MOUSEMOTION and self.check_mouse_coords(event.pos):
                self.change_image('hover')
            elif event.type == pygame.MOUSEBUTTONDOWN and self.check_mouse_coords(event.pos):
                self.change_image('click')
                self.status_window = True
            else:
                self.change_image('off')

        else:
            if  event.type == pygame.MOUSEBUTTONDOWN and self.check_mouse_coords(event.pos):
                self.change_image('off')
                self.status_window = False
            elif event.type == pygame.KEYDOWN:
                self.cotrol_button = event.unicode
                print("key = ",event.unicode)

                self.second_rect_text = self.rect_text
                print(self.second_rect_text)
                if event.key == 32:
                    self.text_cotrol_button = "K SP"
                    self.second_rect_text.x = self.rect_text.x - 13
                elif event.key == 276:
                    self.text_cotrol_button = "K L"
                    self.second_rect_text.x = self.rect_text.x - 8
                elif event.key == 273:
                    self.text_cotrol_button = "K UP"
                    self.second_rect_text.x = self.rect_text.x - 13
                elif event.key == 274:
                    self.text_cotrol_button = "K D"
                    self.second_rect_text.x = self.rect_text.x - 8
                elif event.key == 275:
                    self.text_cotrol_button = "K R"
                    self.second_rect_text.x = self.rect_text.x - 8


    def render(self,screen):
        screen.blit(self.drawing_image,(self.rect.x,self.rect.y))
        screen.blit(self.text_surf,self.rect_text)
