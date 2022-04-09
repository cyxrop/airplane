# -*- coding: utf-8 -*-
# Доп. функции

import pygame, os

def load_image(name, path="images",alpha_cannel=0):
    fullname = os.path.join(path, name)

    try:
        image = pygame.image.load(fullname) # Загружаем картинку и сохраняем поверхность (Surface)
    except (pygame.error): # Если картинки нет на месте
        print("Cannot load image:", name)
        return 0
    if(alpha_cannel):
        image = image.convert_alpha()
    else:
        image = image.convert()

    return image





