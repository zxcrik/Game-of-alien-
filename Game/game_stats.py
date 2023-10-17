class GameStats():
    # Отслеживание статистики для игры #
    def __init__(self, ai_game):
        # Инициализирует статистику #
        self.settings = ai_game.settings
        self.reset_stats()   # Создается 1 экземпляр на игру #
            # Игра запускается в неактивном состоянии #
        self.game_active = False    # завершить игру после потери последнего корабля #

        # Рекорд не дожен сбрасыватся #
        self.high_score = 0
        self.level = 1

    def reset_stats(self):   # Вызывается в начале каждой новой игры # 
        # Инициализирует статистику, изменяющуюся в ходе игры #
        self.ships_left = self.settings.ship_limit
        self.score = 0  