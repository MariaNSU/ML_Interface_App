import pygame
import os
import sys
import pyperclip

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Constants.colors import GRAY, BLUE, BLACK
from Constants.figures import FONT
# Шрифт
pygame.font.init()
class InputBox:
    def __init__(self, x, y, w, h, placeholder="", password=False, need_to_validate=False):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = GRAY
        self.text = ""
        self.masked_text = ""
        self.placeholder = placeholder  # Текст-подсказка внутри поля
        self.active = False
        self.password = password # Является ли окно полем для пароля, если да, то маскируем текст звездочкой
        self.valid = True  # Добавляем флаг для проверки валидности состояния
        self.need_to_validate = need_to_validate  # Флаг о необходимости проверки

    def draw(self, screen):
        outline_color = self.color if self.valid else (255, 0, 0)
        pygame.draw.rect(screen, outline_color, self.rect, 2)
        text_to_display = (self.masked_text if self.password else self.text) if self.text else self.placeholder
        text_surface = FONT.render(text_to_display, True, GRAY)
        text_width, text_height = text_surface.get_size()
        screen.blit(text_surface, (self.rect.x + (self.rect.w - text_width) // 2,
                                   self.rect.y + (self.rect.h - text_height) // 2))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.color = BLUE if self.active else GRAY

        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
                self.masked_text = self.masked_text[:-1]
            elif event.key == pygame.K_v and pygame.key.get_mods() & pygame.KMOD_CTRL:
                clipboard_text = pyperclip.paste()
                self.text += clipboard_text
                self.masked_text += "*" * len(clipboard_text)
            else:
                self.text += event.unicode
                self.masked_text += "*"

            if self.need_to_validate:
                self.validate_input()
    def validate_input(self):
        try:
            value = int(self.text)
            if 0 <= value < 10:
                self.valid = True  # Корректное значение
            else:
                self.valid = False  # Ошибка (вне диапазона)
        except ValueError:
            self.valid = False  # Ошибка (введено не число)
