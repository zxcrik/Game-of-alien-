import pygame.font

# Для создания группы кораблей #
from pygame.sprite import Group   
from ship import Ship

class ScoreBoard():
    # Класс для вывода игровой информации #

    def __init__(self, ai_game):
        # Инициализирует атрибуты подсчета очков #
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        
        # настройки шрифта для вывода счета #
        self.text_color = (30,30,30)
        self.font = pygame.font.SysFont(None, 48)

        # Подготовка исходного изображения #
        self.prep_score()
        self.prep_high_score()  # Вывод рекордного счета  #
        self.prep_level() 
        self.prep_ships()

    def prep_score(self):
        # преобразует текущий счет в графическое изображение #
        rounded_score = round(self.stats.score, -1)    # Округлить до десятков #
        score_str = "{:,}".format(rounded_score)       # аккуратно отформатированный счет #
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        # Вывод счета в правой верхней части экрана #
        self.score_rect = self.score_image.get_rect()           # создание прямоугольника для ровного счета #
        self.score_rect.right = self.screen_rect.right - 20     # вправо на 20 пикселей #
        self.score_rect.top = 20                                # Вверх на 20 пикселей #

    def prep_high_score(self):
        # преобразует текущий счет в графическое изображение #
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)

        # Рекорд выравнивается по центру верхней стороны #
        self.high_score_rect = self.high_score_image.get_rect()          
        self.high_score_rect.right = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top    

    def check_high_score(self):
        # Должен вызыватся при каждом попадании в прищельца #
        # Проверяет, появился ли новый рекорд #
        if self.stats.score > self.stats.high_score:    # Сравнение с текущим рекордом #
            self.stats.high_score = self.stats.score    # Обновление рекорда #
            self.prep_high_score()

    def prep_level(self):
        # преобразует уровень в графическое изображение  #
        level_str = str(self.stats.level)
        self.level_image =  self.font.render(level_str, True, self.text_color, self.settings.bg_color)

        # уровень выводится под текущим счетом #
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10   # Сдвиг на 10 пикселов ниже нижнего края #

    def prep_ships(self):
        # Сообщает количество оставшихся кораблей #
        self.ships = Group()   # Пкстая группа для хранения экземпляров кораблей #
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)                          # Выполнение цикла 1 раз для каждого корабля #
            ship.rect.x = 10 + ship_number * ship.rect.width   # Интервал между кораблями  #
            ship.rect.y = 10      # Выравнивание по уровню счета  #
            self.ships.add(ship)  # Каждый корабль добавляется в группу Ships #

    def show_score(self):
        # Выводит очки, уровень и количество кораблей на экран #
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)   # Вывод кораблей на экрани прорисовка каждого кораюля корабля #
 
    