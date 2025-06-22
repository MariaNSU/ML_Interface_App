import pygame
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Constants.figures import *
from Constants.colors import *
from Helpers.draw_params import update_limits, execute_root_script
from Helpers.processUserDataFiles import get_picture_path




pygame.init()

# Вспомогательные функции

def draw_rounded_rect(surface, color, rect, radius, width=0):
    pygame.draw.rect(surface, color, rect, border_radius=radius, width=width)


def draw_text(screen, text, rect, font=FONT, color=TEXT_COLOR):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=rect.center)

    screen.blit(text_surface, text_rect)


def draw_long_text_in_lines(screen, text, rect, font=FONT, color=TEXT_COLOR, center=True):
    """
        Функция для отрисовки текста внутри заданного прямоугольника.
        Текст разбивается по переносам строки \n.

        :param screen: Поверхность, на которой будет отрисован текст.
        :param text: Текст, который нужно отобразить.
        :param font: Объект шрифта Pygame.
        :param rect: Объект pygame.Rect, определяющий область для текста.
        :param color: Цвет текста в формате RGB (по умолчанию белый).
        :param center: Центрирование текста по вертикали
        """
    # Разбиваем текст по переносам строки
    lines = text.split('\n')

    # Рисуем текст построчно
    line_height = font.get_height()
    total_text_height = len(lines) * line_height
    if center:
        start_y = rect.y + (rect.height - total_text_height) // 2  # Центрируем текст по вертикали
    else:
        start_y = rect.y + 15  # Текст по ферхнему краю прямоугольника с небольшим отступом

    for i, line in enumerate(lines):
        text_surface = font.render(line, True, color)
        text_x = rect.x + (rect.width - text_surface.get_width()) // 2  # Центрируем по горизонтали
        text_y = start_y + i * (line_height + 5)
        screen.blit(text_surface, (text_x, text_y))


def draw_long_text_in_words(screen, text, rect, font=FONT, color=TEXT_COLOR, horizontal_center=True, vertical_center=True):
    # Разбиваем текст на строки
    words = text.split(' ')
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] > rect.width - 10:  # Учитываем внутренний отступ
            lines.append(current_line.strip())
            current_line = word + " "
        else:
            current_line = test_line
    lines.append(current_line.strip())  # Не забываем добавить последнюю строчку

    # Рисуем текст построчно
    line_height = font.get_height()
    total_text_height = len(lines) * line_height
    if vertical_center:
        start_y = rect.y + (rect.height - total_text_height) // 2  # Центрируем текст по вертикали
    else:
        start_y = rect.y + 15

    for i, line in enumerate(lines):
        text_surface = font.render(line, True, color)
        if horizontal_center:
            text_x = rect.x + (rect.width - text_surface.get_width()) // 2  # Центрируем по горизонтали
        else:
            text_x = rect.x + 15
        text_y = start_y + i * line_height
        screen.blit(text_surface, (text_x, text_y))




# for ReDrawing pictures
def handle_redrawing_of_param(screen, param , left, right):
    image_paths = get_picture_path(param)
    if image_paths:
        original_image_C = image_paths['.C'][0]
        if original_image_C:
            new_path = os.path.dirname(original_image_C)
            dir_name = new_path + "/New_Pics/"

            if not os.path.exists(dir_name):
                # Create the directory
                os.makedirs(dir_name)

            path_to_new_file = dir_name + param + left + "_" + right + ".C"

            path_to_new_image = path_to_new_file.split(".C")[0] + ".png"

            update_limits(original_image_C, path_to_new_file, int(left), int(right), output_image=path_to_new_image)
            execute_root_script(path_to_new_file)

            image = pygame.image.load(path_to_new_image)

            image_resized = pygame.transform.scale(image, (HIST_RECT.width, HIST_RECT.height))
            screen.blit(image_resized, HIST_RECT.topleft)
