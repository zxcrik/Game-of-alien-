import sys                    # Завершает игру по команде игрока #
from time import sleep        # Для короткой остановки игры при столкновении с кораблем #
import pygame

from settings import Settings     # Импортирование класса Settings из другого файла #
from ship import Ship             # Импортирование класса ship из другого файла #
from bullet import Bullet         # Импортирование класса Bullet из другого файла #
from alien import Alien           # Импортирование класса Alien из другого файла #
from game_stats import GameStats  # Импортирование класса game_stats из другого файла #
from button import Button
from scoreboard import ScoreBoard


class AlienInvasion:            # Класс для управляния ресурсами и поведения игры #
    def __init__(self):   
        pygame.init()               # Инициализация игры и создание игровых ресурсов #

        self.settings = Settings()   # Создает экземпляр класса Settings и сохраняет его для использования его атрибутов #

            # Запуск игры в полноэкранном режиме #
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        self.screen = pygame.display.set_mode( # Используются атрибуты ширины и высоты из обьекта self.settings #
            (self.settings.screen_width, self.settings.screen_height))  
        
        # Создает окно с прорисовкой всех графических элементов игры #
        self.screen = pygame.display.set_mode((1350,715))               # Кортеж определяющий размеры игрового экрана #
        pygame.display.set_caption("Alien Invasion")

        # Создание экземпляра для хранения игровой статистики #
        # И панели результатов #
        self.stats = GameStats(self)
        self.sb = ScoreBoard(self)
        
        self.ship = Ship(self)     # Передаем текущий эземпляр класса ai, в качестве аргумента #
        self.bg_color = (230,230,230)         # Цвет фона #
        self.bullets = pygame.sprite.Group()  # Группа для хранения всех летящих снарядов #
        self.aliens = pygame.sprite.Group()   # Группа для хранения флота вторжения #

        # Добавление метода _create_fleet #
        self._create_fleet()

        # создание кнопки play #
        self.play_button = Button(self, "Play")

    def run_game(self):    # Запуск основного цикла игры #
        while True:
            self._check_events()    # Точечный синтаксис для вызова внутри класса #
        # Части игры которые выполняются при активной игре #
            if self.stats.game_active:
                self.ship.update()      # При каждом проходе цикла вызывается метод для корабля #
                self._update_bullets()  # Обновление позиций снарядов #
                self._update_aliens()   # Обновление позиций каждого прищельца #
            self._update_screen()   # Прорисовка фона и переключение экрана #
  
    def _update_bullets(self):
        # Обновляет позиции снарядов и уничтожает старые снаряды#
        self.bullets.update()    # Позиция снаряда обновляется при каждом проходе цикла #
        # Удаление снарядов вышедших за край экрана #
        for bullet in self.bullets.copy():    # copy() для запуска цикла #
            if bullet.rect.bottom <= 0:       # Проверка вышел ли снаряд за край экрана #
                self.bullets.remove(bullet)   # Удаление снаряда #

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        # Обработка коллизий снарядов с прищельцами #
        # При обнаружении попадания, удалить снаряд и прищельца #
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens ,True, True)

        if collisions:
            for aliens in collisions.values():    # Цикл перебирает все значения в словаре #
                self.stats.score += self.settings.alien_points * len(aliens)
            self.stats.score += self.settings.alien_points    # Проверка попадания, начисление очков #
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # Уничтожение существующих снарядов, повышение скорости, создание нового флота #
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Увеличение уровня #
            self.stats.level += 1    # Если прищельцы уничтожены, то прибавать уровень #
            self.sb.prep_level()     # Вызов функции для прибавления уровня #

    def _check_events(self):
            # Отслеживание событий клавиатуры и мыши #
        for event in pygame.event.get():            # Получение доступа к событиям #
            if event.type == pygame.QUIT:         # при событии закрытия игрового экрана, срабатывает метод #
                sys.exit()                      # Выход из игры #
            elif event.type == pygame.KEYDOWN:    # Выполнение кода при обнаружении события KEYDOWN # 
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:        
                self._check_keyup_events(event) 
            elif event.type == pygame.MOUSEBUTTONDOWN:   # Нажатие на мышь в любой части экрана #
                mouse_pos = pygame.mouse.get_pos()       # Кортеж с координатами точки щелчка #
                self._check_play_button(mouse_pos)       # Передача данных кортежа #

    def _check_keydown_events(self, event):
            # Реагирует на нажатие клавиш #
        if event.key == pygame.K_RIGHT:    
            self.ship.moving_right = True   # Вместо изменений позиции корабля, присваивается True #
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_front = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_back = True
        elif event.key == pygame.K_q:       # Завершение игры на кнопку q #
            sys.exit()
        elif event.key == pygame.K_SPACE:   # Выстрел на пробел #
            self._fire_bullet() 

    def _check_keyup_events(self, event):
           # Реагирует на отпускание клавиш #
        if event.key == pygame.K_RIGHT:      # Проверка на клавишу, которую отпустили #
            self.ship.moving_right = False  # Присваивается значение false #
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:  
            self.ship.moving_front = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_back = False

    def _check_play_button(self, mouse_pos):
        # Запуск новой игры при нажатии на play #  
        # Находится ли точка щелчка в предеалх определенной области #
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)  # Содержит значение True или False #
        if button_clicked and not self.stats.game_active:  # Перезапуск если пользователь нажал на кнопку и игра не активна в данный момент #
                # Сброс игровых настроек #  
            self.settings.initialize_dynamic_settings()

            # сборс игровой статистики #
            self.stats.reset_stats()         # Обновление игровой статистики #
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()    # Кол-во пройденных уровней отображается на экране #
            self.sb.prep_ships()    # Кол-во попыток  #

            # очистка списка прищельцев и снарядов #
            self.aliens.empty()
            self.bullets.empty()

            # создание нового флота и размещение корабля в центре #
            self._create_fleet()      # Содание нового флота #
            self.ship.center_ship()   # Размещение корабля по центру #

            # Указатель мыши скрывается #
            pygame.mouse.set_visible(False)

        
    def _update_screen(self):
            # код обновления экрана в отдельном методе  #
        self.screen.fill(self.settings.bg_color)    # При каждом проходе цикла перерисовывается экран #
        self.ship.blitme()     # Корабль рисуется на экране, поверх цветого фона #
        # Отобрражение последнего прорисованного экрана #
        for bullet in self.bullets.sprites():  # Возвращает список всех спрайтов в группе Bullets, #
            bullet.draw_bullet()               # Чтобы нарисовать все выпущенные снаряды на экране #
        self.aliens.draw(self.screen)          # Чтобы пришелец появился на экране #

        # Вывод информации о счете  #
        self.sb.show_score()

        # Вызов метода для вывода кнопки на экран #
        # Кнопка play отображается в том случае, если игра не активна #
        if not self.stats.game_active:
            self.play_button.draw_button()
        

        pygame.display.flip()          # Так же создание иллюзии плавного движения #


    def _fire_bullet(self):
        # Создание нового снаряда и включение его в группу bullets #
        if len(self.bullets) < self.settings.bullets_allowed:      # Возможность выпускать снаряды группами по 5 #
            new_bullet = Bullet(self)     # Создаем экземпляр bullet которому присваивается имя new_bullet #
            self.bullets.add(new_bullet)  # включается в группу bullets методом add, а не append #

    def _create_fleet(self):
        # Создание флота вторжения #
        # создание пришельца и вычисление количества пришельцев в ряду #
        # Интервал между соседними пришельцами равен ширине пришельца #
        alien = Alien(self)                          # Создание экземпляра Alien #
        alien_width, alien_height = alien.rect.size  # Использование size, со значениями ширины прищельца #
        alien_width = alien.rect.width  # Определение ширины пришельца по атрибуту rect, сохранение в alien_width #       
        available_space_x = self.settings.screen_width - (2 * alien_width)  # Вычисление доступного горизонтального пространства и кол-во пришельцев в нем #
        number_aliens_x = available_space_x // (2 * alien_width)            

        # Определяет количество рядов, помещающихся на экране #
        ship_height = self.ship.rect.height
        avaibale_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)  # Доступное вертикальное пространство #
        number_rows = avaibale_space_y // (2 * alien_height)    # Количество создаваемых рядов #

        # Создание флота вторжения #
        for row_number in range(number_rows):            # Создает ряды пришельцев #
            for alien_number in range(number_aliens_x):  # Создает 1 ряд пришельцев #
                self._create_alien(alien_number, row_number)
            
    def _create_alien(self, alien_number,row_number):
        # Создание пришельца и размещение его в ряду #
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien_width = alien.rect.width
        alien.x = alien_width + 2 * alien_width * alien_number # Новый пришелец и занимаемое им пространство #
        alien.rect.x = alien.x  # Размещение прищельца в ряду  #
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number  # Изменяем координату прищельца, если он не в 1 ряду #
        self.aliens.add(alien)  # Добавление в группу для хранения флота #

    def _ship_hit(self):
        if self.stats.ships_left > 0:
            # Обрабатывает столкновение корабля с пришельцами #
            # Уменьшение ships_left и  обновление панели счета #
            self.stats.ships_left -= 1
            self.sb.prep_ships()     # Вывод попыток при столкновении прищельца с кораблем #

            # Очистка списков пришельцев и снарядов #
            self.aliens.empty() 
            self.bullets.empty()

            # Создание нового флота и размещение корабля в центре #
            self._create_fleet()
            self.ship.center_ship()

            # Пауза #
            sleep(0.2)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

        
    def _update_aliens(self):
        # Обновляет позиции всех прищельцев #
        self._check_fleet_edges()   # Перед обновлением позиций, вызывается метод  #
        self.aliens.update()

        # Проверка коллизий "Корабль прищелец" #
        if pygame.sprite.spritecollideany(self.ship, self.aliens):  # Функция ищет элемнт группы встпувщий в коллизию #
            self._ship_hit()                                       # При обнаружении столкновении с пришельцем #


    def _change_fleet_direction(self):
        # опускает весь флот и меняет направление флота #
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed  # Уменьшает высоту каждого пришельца, используя fleen_direction #
        self.settings.fleet_direction *= -1                 # направление меняется в противоположную сторону #
                

    def _check_fleet_edges(self):
        # Реагирует на достижением прищельца края экрана #
        for alien in self.aliens.sprites():    # Вызов метода для каждого пришельца #
            if alien.check_edges():            # если True то прищелец находится у края и флот меняет направление #
                self._change_fleet_direction()  # Вызывается функция и происходит выход из цикла #
                break


if __name__ == '__main__':
    # Создание экземпляра и запуск игры #
    ai = AlienInvasion()     # Метод выполняется при прямом вызове функции #
    ai.run_game() 

