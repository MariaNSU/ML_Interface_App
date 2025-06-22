import pygame
from Constants.colors import *
from Constants.sizes import *
from Constants.figures import FONT

pygame.init()

# Шрифт


def draw_rounded_rect(surface, color, rect, radius):
    pygame.draw.rect(surface, color, rect, border_radius=radius)


def draw_text(screen, text, rect, font, color):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)


class TabManager:
    def __init__(self):
        self.tabs = []
        self.active_tab = None

    def add_tab(self, tab):
        self.tabs.append(tab)
        if not self.active_tab:
            self.active_tab = 0

    def change_tab(self, index):
        if index < len(self.tabs):
            self.active_tab = index

    def update(self, mouse_pos):
        """Обновляет состояние вкладок (например, при наведении мыши)."""
        pass  # Можно реализовать эффекты наведения

    def handle_click(self, event):
        """Обрабатывает клик по вкладкам."""
        x, y = event.pos
        if y < 60:  # Высота области вкладок
            current_x = 10
            for i, tab in enumerate(self.tabs):
                tab_rect = pygame.Rect(current_x, 10, tab.width, 40)
                if tab_rect.collidepoint(event.pos):
                    self.change_tab(i)
                current_x += tab.width + 10

    def draw(self, screen):
        """Отрисовка вкладок."""
        # Отрисовка фона
        screen.fill(BACKGROUND_COLOR)
        # Отрисовка самих вкладок
        current_x = 10
        for i, tab in enumerate(self.tabs):
            tab_rect = pygame.Rect(current_x, 5, tab.width, 40)
            color = TAB_ACTIVE_COLOR if i == self.active_tab else TAB_INACTIVE_COLOR
            text_color = TEXT_COLOR_ACTIVE if i == self.active_tab else TEXT_COLOR_INACTIVE
            draw_rounded_rect(screen, color, tab_rect, radius=15)
            draw_text(screen, tab.title, tab_rect, FONT, text_color)
            current_x += tab.width + 10
        # Отрисовка содержимого активной вкладки
        if self.active_tab is not None:
            active_tab = self.tabs[self.active_tab]
            content_rect = pygame.Rect(5, 50, WIDTH - 10, HEIGHT - 40)
            pygame.draw.rect(screen, active_tab.content_color, content_rect)