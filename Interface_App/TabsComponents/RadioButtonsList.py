import pygame

# Цвета
WHITE = (255, 255, 255)
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (0, 102, 204)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
TAB_ACTIVE_COLOR = (102, 178, 255)


# Шрифт (по умолчанию)
DEFAULT_FONT_SIZE = 25


class RadioButtonsList:
    def __init__(self, projects, content_rect, font=None, font_size=DEFAULT_FONT_SIZE,
                 x_offset=50, y_offset_start=50, spacing=50, multiple_choice=False, default_state=False):
        """
        Инициализация модуля RadioProjectSelector.

        :param projects: Список строк с названиями проектов.
        :param content_rect: pygame.Rect, определяющий область отрисовки.
        :param font: pygame.font.Font (передайте нужный шрифт или используйте шрифт по умолчанию).
        :param font_size: Размер шрифта, если font не передан.
        :param x_offset: Смещение по X (для текста и кружков радио-кнопок).
        :param y_offset_start: Начальное смещение по Y, с которого начинаются элементы.
        :param spacing: Расстояние между элементами по вертикали.
        :param multiple_choice: Флаг, если в списке возможен выбор сразу нескольких элементов
        :param: default_state: Изначальное состояние элементов списка с множественным выбором (True - все закрашены, False - все пустые)
        """
        self.projects = projects
        self.selected_project = None
        self.x_offset = x_offset
        self.y_offset_start = y_offset_start
        self.spacing = spacing
        self.scroll_offset = 0  # Сдвиг прокрутки
        self.content_rect = content_rect  # Ограничение области рисования
        self.multiple_choice = multiple_choice
        self.default_state = default_state
        self.selected_projects = [default_state] * len(projects)

        if font:
            self.font = font
        else:
            # Задаем стандартный шрифт, чтобы избежать проблем со шрифтом
            self.font = pygame.font.Font(pygame.font.match_font('arial'), font_size)

    def draw(self, surface):
        if self.multiple_choice:
            self.draw_multiple(surface)
        else:
            self.draw_single(surface)

    def draw_multiple(self, surface):
        """
        Рисует список с радиокнопками в окно (surface).
        :param surface: Экземпляр pygame.Surface.
        """
        pygame.draw.rect(surface, TAB_ACTIVE_COLOR, self.content_rect, border_radius=15, width=2)  # Границы области
        original_clip = surface.get_clip()
        surface.set_clip(self.content_rect)

        y_offset = self.y_offset_start + self.scroll_offset

        for i, project in enumerate(self.projects):
            project_text = str(project)
            if y_offset > self.content_rect.bottom:
                break

            if y_offset + self.spacing > self.content_rect.top:
                # Рисуем радиокнопку
                circle_x = self.x_offset
                circle_y = y_offset + 15

                # Если данный проект выбран, заполняем круг
                if self.selected_projects[i]:
                    pygame.draw.circle(surface, BLACK, (circle_x, circle_y), 10, 2)
                    pygame.draw.circle(surface, LIGHT_BLUE, (circle_x, circle_y), 9)
                else:
                    pygame.draw.circle(surface, BLACK, (circle_x, circle_y), 10, 2)  # Контур радиокнопки

                # Рисуем текст рядом с радиокнопкой
                text_surface = self.font.render(project_text, True, BLACK)
                surface.blit(text_surface, (circle_x + 30, y_offset))

            y_offset += self.spacing

        surface.set_clip(original_clip)

    def draw_single(self, surface):
        """
        Рисует список проектов в переданное окно (surface).
        :param surface: Экземпляр pygame.Surface.
        """
        # Ограничим область списка "рамкой"
        pygame.draw.rect(surface, TAB_ACTIVE_COLOR, self.content_rect, border_radius=15, width=2)

        # Сохраняем текущую область обрезки и устанавливаем новую
        original_clip = surface.get_clip()
        surface.set_clip(self.content_rect)

        y_offset = self.y_offset_start + self.scroll_offset
        for i, project in enumerate(self.projects):
            project_text = str(project)
            # Проверяем, входит ли элемент в видимую область
            if y_offset > self.content_rect.bottom:
                break  # Выходим, как только выходим за нижнюю границу

            if y_offset + self.spacing > self.content_rect.top:
                # Отрисовка радиокнопки
                btn_x = self.x_offset
                btn_y = y_offset + 15
                if self.selected_project == i:  # Закрашиваем выбранное
                    pygame.draw.circle(surface, BLACK, (btn_x, btn_y), 10, 2)
                    pygame.draw.circle(surface, LIGHT_BLUE, (btn_x, btn_y), 9)
                else:
                    pygame.draw.circle(surface, BLACK, (btn_x, btn_y), 10, 2)

                # Отрисовка текста
                text_surface = self.font.render(project_text, True, BLACK)
                surface.blit(text_surface, (btn_x + 30, y_offset))

            y_offset += self.spacing

        # Восстанавливаем исходную область обрезки
        surface.set_clip(original_clip)

    def handle_event(self, event):
        """
        Обработка событий, например, мыши и скроллинга.
        :param event: pygame.event.Event.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if self.content_rect.collidepoint(mouse_x, mouse_y):
                if event.button == 4:  # Скролл вверх
                    self.scroll_offset = min(self.scroll_offset + 20, 0)  # Ограничиваем сверху
                elif event.button == 5:  # Скролл вниз
                    max_scroll = -(len(self.projects) * self.spacing - (self.content_rect.height - self.y_offset_start))
                    self.scroll_offset = max(self.scroll_offset - 20, max_scroll)

    def handle_click(self, pos):
        """
        Обработка кликов мыши. Проверяет, попали ли в радиокнопку.

        :param pos: Кортеж (x, y) из event.pos — координаты клика мыши.
        :return: bool — True, если выбран проект, иначе False.
        """
        y_offset = self.y_offset_start + self.scroll_offset
        for i in range(len(self.projects)):
            btn_x, btn_y = self.x_offset, y_offset + 15
            if (pos[0] - btn_x) ** 2 + (pos[1] - btn_y) ** 2 <= 10 ** 2:  # Клик в радиокнопку
                if self.multiple_choice:
                    self.selected_projects[i] = not (self.selected_projects[i])
                else:
                    self.selected_project = i
                return True
            y_offset += self.spacing
        return False



    def set_projects(self, projects):
        self.projects = projects
        self.selected_projects = [self.default_state] * len(projects)

    @staticmethod
    def save_selected_project(project):
        """
        Сохраняет выбранный проект в файл `selected_project.txt`.
        """
        with open("selected_project.txt", "w", encoding="utf-8") as file:
            file.write(f"Выбранный проект: {project}")

