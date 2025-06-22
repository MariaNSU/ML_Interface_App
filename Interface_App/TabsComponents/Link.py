import pygame
import webbrowser

class Link:
    def __init__(self, text, font, color, hover_color, position, underline_offset, tooltip_text):
        """
        Конструктор класса
        :param text: Текст ссылки
        :param font: Объект шрифта pygame.font.Font
        :param color: Цвет текста в обычном состоянии
        :param hover_color: Цвет текста при наведении мыши
        :param position: Координаты центра текста (x, y)
        :param underline_offset: Смещение подчеркивания от нижней границы текста
        :param tooltip_text: Текст всплывающей подсказки
        :param url: URL-адрес для открытия в браузере
        """
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.position = position
        self.underline_offset = underline_offset
        self.tooltip_text = tooltip_text
        self.url = "https://wwwsnd.inp.nsk.su/trac/wiki/SND2K/Data/"

        self.is_hovered = False
        self.render_text()
        self.render_tooltip()

    def render_text(self):
        """
        Отрисовывает текст ссылки.
        """
        color = self.hover_color if self.is_hovered else self.color
        self.text_surface = self.font.render(self.text, True, color)
        self.text_rect = self.text_surface.get_rect(center=self.position)

    def render_tooltip(self):
        """
        Отрисовывает всплывающую подсказку.
        """
        self.tooltip_surface = self.font.render(self.tooltip_text, True, self.hover_color)
        self.tooltip_rect = self.tooltip_surface.get_rect(midtop=(self.text_rect.centerx, self.text_rect.bottom))

    def update(self, mouse_pos):
        """
        Обновляет состояние ссылки (работа с наведением мыши).
        :param mouse_pos: Позиция мыши
        """
        self.is_hovered = self.text_rect.collidepoint(mouse_pos)
        self.render_text()  # Обновляем текст в зависимости от состояния

    def draw(self, screen):
        """
        Рисует текст и подсказку при необходимости.
        :param screen: Экран pygame
        """
        # Отрисовка текста
        screen.blit(self.text_surface, self.text_rect)

        # Подчеркивание
        pygame.draw.line(
            screen,
            self.hover_color if self.is_hovered else self.color,
            (self.text_rect.left, self.text_rect.bottom + self.underline_offset),
            (self.text_rect.right, self.text_rect.bottom + self.underline_offset),
            2
        )

        # Всплывающая подсказка
        if self.is_hovered:
            screen.blit(self.tooltip_surface, self.tooltip_rect)

    def handle_event(self, event):
        """
        Обрабатывает события (например, клик мыши).
        :param event: Событие Pygame
        """
        if event.type == pygame.MOUSEBUTTONDOWN and self.is_hovered:
            webbrowser.open(self.url, 1)  # Открыть URL

    def set_url(self, url):
        """
        Устанавливаем ссылки именно на страницы вики с перекачками
        :param url: обязательно через тире должна быть версия перекачки!!! (напр., MHAD2012-6)
        :return:
        """
        #"https://wwwsnd.inp.nsk.su/trac/wiki/SND2K/Data/" + pumping_name
        self.url = url


# Пример использования класса
def main():
    # Инициализация Pygame
    pygame.init()
    width, height = 600, 400
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Класс ссылки")
    clock = pygame.time.Clock()

    # Цвета
    white = (255, 255, 255)
    black = (0, 0, 0)
    blue = (100, 149, 237)

    # Шрифт
    font = pygame.font.Font(None, 36)

    # Создание объекта ссылки
    link = Link(
        "Подробнее",
        font,
        black,
        blue,
        (width // 2, height // 2),
        underline_offset=6,
        tooltip_text="Сейчас откроется браузер",
        url="D:\PycharmProjects\PyGameExample\ExperimentsData\MHAD2010-4\index.html"
    )

    running = True
    while running:
        screen.fill(white)  # Заливка фона

        # Получаем позицию мыши
        mouse_pos = pygame.mouse.get_pos()

        # Обновление состояния ссылки
        link.update(mouse_pos)

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            link.handle_event(event)  # Передаем события объекту

        # Отрисовка ссылки
        link.draw(screen)

        pygame.display.flip()  # Обновляем экран
        clock.tick(60)  # Максимум 60 FPS

    pygame.quit()

