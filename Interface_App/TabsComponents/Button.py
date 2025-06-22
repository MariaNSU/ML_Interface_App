import pygame

# Цвета
WHITE = (255, 255, 255)
LIGHT_BLUE = (173, 216, 230)
GRAY = (200, 200, 200)

# Шрифт (по умолчанию)
DEFAULT_FONT_SIZE = 36


class Button:
    def __init__(
        self, text, font_size, x_offset, y_offset, width, height, color=GRAY, pressed_color=LIGHT_BLUE, text_color=WHITE
    ):
        """
        Инициализация кнопки.

        :param text: Текст кнопки.
        :param font_size: Размер шрифта.
        :param x_offset: Положение по X.
        :param y_offset: Положение по Y.
        :param width: Ширина кнопки.
        :param height: Высота кнопки.
        :param color: Цвет кнопки (обычное состояние).
        :param pressed_color: Цвет кнопки при нажатии.
        :param text_color: Цвет текста.
        """
        self.text = text
        #self.font = pygame.font.Font(pygame.font.match_font('arial'), font_size)
        self.font = pygame.font.Font(None, font_size)
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.width = width
        self.height = height
        self.color = color
        self.pressed_color = pressed_color
        self.text_color = text_color
        self.is_pressed = False  # Состояние кнопки (нажата или нет)

    def draw(self, surface):
        """
        Рисует кнопку на указанной поверхности.
        :param surface: Экземпляр pygame.Surface.
        """
        # Выбираем цвет в зависимости от состояния
        current_color = self.pressed_color if self.is_pressed else self.color

        pygame.draw.rect(surface, current_color, (self.x_offset, self.y_offset, self.width, self.height),
                         border_radius=15)
        text_surface = self.font.render(self.text, True, self.text_color)
        surface.blit(
            text_surface,
            (
                self.x_offset + (self.width - text_surface.get_width()) // 2,
                self.y_offset + (self.height - text_surface.get_height()) // 2,
            ),
        )

    def draw2(self, surface):
        """
        Рисует кнопку с длинным текстом на указанной поверхности по словам
        :param surface: Экземпляр pygame.Surface.
        """
        # Выбираем цвет в зависимости от состояния
        current_color = self.pressed_color if self.is_pressed else self.color

        # Рисуем кнопку
        pygame.draw.rect(surface, current_color, (self.x_offset, self.y_offset, self.width, self.height), border_radius=15)

        # Разбиваем текст на строки
        words = self.text.split(' ')
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            if self.font.size(test_line)[0] > self.width - 10:  # Учитываем внутренний отступ
                lines.append(current_line.strip())
                current_line = word + " "
            else:
                current_line = test_line
        lines.append(current_line.strip())  # Не забываем добавить последнюю строчку

        # Рисуем текст построчно
        line_height = self.font.get_height()
        total_text_height = len(lines) * line_height
        start_y = self.y_offset + (self.height - total_text_height) // 2  # Центрируем текст по вертикали

        for i, line in enumerate(lines):
            text_surface = self.font.render(line, True, self.text_color)
            text_x = self.x_offset + (self.width - text_surface.get_width()) // 2  # Центрируем по горизонтали
            text_y = start_y + i * line_height
            surface.blit(text_surface, (text_x, text_y))

    def is_clicked(self, pos):
        """
        Проверяет, была ли нажата кнопка.
        :param pos: Кортеж (x, y).
        :return: bool
        """
        x_condition = self.x_offset <= pos[0] <= self.x_offset + self.width
        y_condition = self.y_offset <= pos[1] <= self.y_offset + self.height
        return x_condition and y_condition

    def set_pressed(self, pressed):
        """
        Устанавливает состояние кнопки.
        """
        self.is_pressed = pressed

