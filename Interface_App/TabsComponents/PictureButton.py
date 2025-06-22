import pygame
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Button import Button

from Constants.sizes import PUMPING_LIST_POSITION, LISTS_START_Y_OFFSET
from Constants.figures import FONT, PICTURE_RECT
from Constants.colors import GRAY, BLUE, BLACK, WHITE, LIGHT_BLUE, DARK_BLUE, ACTIVE_BUTTON, INACTIVE_BUTTON





class PictureButton(Button):
    def __init__(self, text, font_size, x_offset, y_offset, width, height,
                 image_path=None, color=ACTIVE_BUTTON, pressed_color=INACTIVE_BUTTON, text_color=WHITE):
        """
        Расширенная кнопка с функциональностью отображения картинки.

        :param image_path: Путь к изображению, которое будет отображаться при клике
        """
        super().__init__(text, font_size, x_offset, y_offset, width, height, color, pressed_color, text_color)
        self.image_path = image_path
        self.image = None
        self.image_rect = PICTURE_RECT
        if image_path and os.path.exists(image_path):
            self.load_image()

    def load_image(self):
        """Загружает изображение и масштабирует его под заданный прямоугольник"""
        try:
            self.image = pygame.image.load(self.image_path)
            # Масштабируем изображение с сохранением пропорций
            img_width, img_height = self.image.get_size()
            scale_ratio = min(self.image_rect.width / img_width,
                              self.image_rect.height / img_height)
            new_size = (int(img_width * scale_ratio), int(img_height * scale_ratio))
            self.image = pygame.transform.scale(self.image, new_size)
        except Exception as e:
            print(f"Error loading image {self.image_path}: {e}")
            self.image = None

    def draw_image(self, surface):
        """Рисует изображение, если оно загружено и кнопка нажата"""
        if self.is_pressed and self.image:
            # Очищаем область для изображения
            pygame.draw.rect(surface, WHITE, self.image_rect)

            # Центрируем изображение в отведенной области
            img_x = self.image_rect.x + (self.image_rect.width - self.image.get_width()) // 2
            img_y = self.image_rect.y + (self.image_rect.height - self.image.get_height()) // 2
            surface.blit(self.image, (img_x, img_y))

            # Рисуем рамку вокруг изображения
            pygame.draw.rect(surface, BLACK, self.image_rect, 2)

    def handle_event(self, event, buttons_group):
        """
        Обрабатывает события мыши.
        Возвращает True, если было нажатие на кнопку (для обработки в основном цикле)
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_clicked(event.pos):
                # Сбрасываем состояние всех кнопок в группе
                for btn in buttons_group:
                    btn.set_pressed(False)
                # Устанавливаем состояние текущей кнопки
                self.set_pressed(True)
                return True
        return False

    def update_image_path_with_background(self, background_name):
        """
        Обновляет путь к изображению, добавляя название фона в папку (images_НазваниеФона).
        Если изображение не найдено, оставляет self.image = None.
        """
        if not self.image_path:
            return  # Нет пути — ничего не делаем

        # Разделяем путь на папку и имя файла
        dir_name, file_name = os.path.split(self.image_path)
        dirs = self.image_path.split("/")[:-1]
        dir = "/".join(dirs)

        # Формируем новую папку: images_НазваниеФона
        new_dir = f"{dir}_{background_name}"
        new_image_path = os.path.join(new_dir, file_name)

        # Если новый путь существует — загружаем изображение
        if os.path.exists(new_image_path):
            self.image_path = new_image_path
            self.load_image()
        else:
            print(f"Image not found at {new_image_path}")
            self.image = None  # Сбрасываем изображение, если не найдено

    