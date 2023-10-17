import pygame
from pygame.sprite import Sprite 

class Ship(Sprite):
    # Класс для управления кораблем #
    def __init__(self, ai_game):    # ai_game -> ссылка на текущий экземпляр класса AlienInvasion #
        # Инициализирует корабль и задает его начальную позицию #
        super().__init__()  # Наследование от Sprite #
        self.screen = ai_game.screen  # Экран присваивается атрибуту ship, к нему можно обращатся во всех модулях класса #
        self.settings = ai_game.settings     # Создание атрибута для использования в update() #
        self.screen_rect = ai_game.screen.get_rect()  # 1) обращается к rect, присваивает self.screen_rect #
                                                      # 2) позволяет разместить корабль в нужной позиции экрана #

        # Загружает изображение корабля и получает прямоугольник #
        self.image = pygame.image.load("My_projects/Game/cosmo_ship.png")  # Загружаем изображение корабля и присваиваем его self.image #
        self.rect = self.image.get_rect()   # вызов get_rect() для получения атрибута rect #
                                            # позднее используем для позиционирования корабля  #

        # Каждый новый корабль появляется в нижней части экрана #
        self.rect.midbottom = self.screen_rect.midbottom

        # Сохранение вещественной координаты центра корабля #
        self.x = float(self.rect.x)   # Новый атрибут способный хранить дробные значения для оси x #
        self.y = float(self.rect.y)   # Новый атрибут способный хранить дробные значения для оси y #

            # Флаги перемещения #
        self.moving_right = False   # Инициализируем значение, moving_right = False  #
        self.moving_left = False
        self.moving_front = False
        self.moving_back = False

    def update(self):  # Метод для перемещения корабля, вызывается через класс ship #
        # Обновляет позицию корабля с учетом флага #
            # Обновляется атрибут x, не rect #
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
            # Движение в лево #
        if self.moving_left and self.rect.left > 0: 
            self.x -= self.settings.ship_speed
            # Движение вверх #
        if self.moving_front and self.rect.top > 0:
            self.y -= self.settings.ship_speed
            # Движение вниз #
        if self.moving_back and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed
        
        # Обновление атрибута rect на основании self.x #
        self.rect.x = self.x   # Новое значение self.x используется для обновления self.rect.x #
        self.rect.y = self.y   # Новое значение self.y используется для обновления self.rect.y #


    def blitme(self):       # метод выводит изображение на экран, в заданной позиции self.rect #
        # Рисует корабль в текущей позиции #   
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        # Размещает корабль в центре нижней стороны #
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
     