        # Файл для добавления и изменений настроек  #

    # Класс для хранения всех настроек игры Alien Invasion #
class Settings():
        def __init__(self):
            # Инициализирует настройки игры #          
                # Параметры экрана: #
                self.screen_width = 1250       # Высота экрана #
                self.screen_height = 715       # ширина экрана #
                self.bg_color = (230, 230, 230)   # Цвет на фоне #
                self.ship_speed = 1.5      # Скорость корабля #
                self.ship_limit = 3  

                        # Параметры снаряда  #
                self.bullet_speed = 2
                self.bullet_width = 4      # Ширина 3 пикселя #
                self.bullet_height = 17   # Высота 15 пикселя #
                self.bullet_color = (255,0,0)

                self.bullets_allowed = 5   # Ограничение снарядов #
                # Настройки пришельцев #
                self.alien_speed = 1.0      # Скорость каждого прищельца #
                self.fleet_drop_speed = 10  # Величина снижения флота, при достижении им края #

                # Темп ускорения игры #
                self.speedup_scale = 1.1

                # Темп роста стоимости прищельцев #
                self.score_scale = 1.5

                self.initialize_dynamic_settings()      # инициализирует значения атрибутов, которые должны изменятся #
                
        def initialize_dynamic_settings(self): 
        # Инициализирует настройки изменяющиеся в ходе игры #
                self.ship_speed_factor = 1.5
                self.bullet_speed_factor = 3.0
                self.alien_speed_factor = 1.0

                # fleet_direction = 1 <- Обозначает движение в право, = -1 <- Движение в лево #
                self.fleet_direction = 1    

                # Подсчет очков #
                self.alien_points = 50   # Сбрасывается в начале каждой новой игры #
        
        def increase_speed(self):
        # увеличивает настройки скорости и стоимость прищельцев #
                self.ship_speed_factor *= self.speedup_scale 
                self.bullet_speed_factor *= self.speedup_scale
                self.alien_speed_factor *= self.speedup_scale 

                self.aliens_points = int(self.alien_points * self.score_scale) # Int для прибавления целого кол-ва очков #
            



    

 