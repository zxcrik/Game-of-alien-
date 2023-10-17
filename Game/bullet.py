import pygame 
from pygame.sprite import Sprite

class Bullet(Sprite):
    # Класс для управления снарядами, выпущенными кораблем #
    def __init__(self, ai_game):
        # Создает объект снарядов в текущей позиции корабля #
        super().__init__()
        self.screen = ai_game.screen         
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # Создание снаряда в позиции (0,0) и назначение правильной позиции #
        self.rect = pygame.Rect(0,0, self.settings.bullet_width, self.settings.bullet_height) # Создается атрибут снаряда #
        self.rect.midtop = ai_game.ship.rect.midtop  # Атрибуту снаряда прсваивается значение корабля #
        
        # Позиция снаряда хранится в вещественном формате #
        self.y = float(self.rect.y)  # снаряд появляется у верхнего края корабля для имитации выстрела #

    def update(self):
        # Перемещает снаряд вверх по экрану #
        # Обновление позиции снаряда в вещественном формате #
        self.y -= self.settings.bullet_speed   # выстрел и движение снаряда по оси y #
        # Обновление позиции прямоугольника #
        self.rect.y = self.y   # self.rect.y используется для изменения значения self.y #

    def draw_bullet(self):
        # Вывод снаряда на экран #
        pygame.draw.rect(self.screen, self.color, self.rect)
    


