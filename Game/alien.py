import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    # Класс представляющий одного пришельца #

    def __init__(self, ai_game):
        # Инициализирует пришельца и задает его начальную позицию #
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings  # Инициализирует скорость прищельца #

        # Загрузка изображения пришельца и назначение атрибута rect #
        self.image = pygame.image.load('My_projects/Game/cosmo_alien.png')
        self.rect = self.image.get_rect()

        # Каждый новый пришелец появляется в левом верхнем углу #
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Сохранение точечной горизонтальной позиции пришельца #
        self.x = float(self.rect.x)

    def check_edges(self):
        # Возвращает True, если прищелец находится у края экрана #
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0: 
            return True
        
    def update(self):
        # Перемещает прищельца влево или вправо #
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)  # смещаем прищельца в право  #
        self.rect.x = self.x                 # обновление позиции прямоугольника прищельца #


