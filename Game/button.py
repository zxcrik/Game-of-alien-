import pygame.font      # позволяет выводить текст на экран #

class Button():
    def __init__(self, ai_game, msg): 
        # инициализирует атрибуты кнопки #
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # назначение размера и свойств кнопки #
        self.width, self.height = 200, 50
        self.button_color = (0,255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)  # шрифт и размер #

        # Построение объекта rect кнопки и выравнивание по центру экрана #
        self.rect = pygame.Rect(0,0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # Сообщение кнопки создается только 1 раз #
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        # перобразует msg в прямоугольник и выравниет текст по центру #
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # отображение кнопки на экране и вывод сообщения #
        self.screen.fill(self.button_color, self.rect)          # рисует прямоугольную часть кнопки #
        self.screen.blit(self.msg_image, self.msg_image_rect)   # вывод изобрадения текста на экран #
