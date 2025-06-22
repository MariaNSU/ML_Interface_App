import pygame
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from TabsComponents.RadioButtonsList import RadioButtonsList
from TabsComponents.Button import Button
from TabsComponents.InputBox import InputBox
from TabsComponents.Link import Link
from TabsComponents.Tab import Tab
from TabsComponents.PictureButton import PictureButton
from TabsComponents.TabManager import TabManager
from TabsDraw import draw_Data_and_MC_tab, draw_Project_tab, draw_Selections_tab, draw_TMVA_tab, draw_TMVA_results_tab, draw_TMVA_usage
from TabsEventHandlers import handle_events_Data_and_MC, handle_events_Project, handle_events_Selections, handle_events_TMVA, handle_events_TMVA_results

from Constants.colors import *
from Constants.lists import LABELS, EXTENDED_PUMPINGS_RELEASE, DISCRIMINATORS, TMVA_IMAGE_BUTTON
from Constants.sizes import *
from Constants.figures import (FONT, PUMPING_INFO_RECT, SELECT_BACKGROUND_RECT, INPUT_LIMITS_RECT,
                               INPUT_SELECTION_CONDITIONS_RECT, SELECTIONS_SIGNAL_INPUT, SELECT_PUMPING_RECT,
                               SELECTIONS_BACKGR_INPUT, PICTURE_RECT, )

from Screen import Screen

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class NewProjectTabsScreen(Screen):
    def __init__(self):

        self.tab_manager = TabManager()
        self.tab_manager.add_tab(Tab("Проект", CONTENT_COLOR))
        self.tab_manager.add_tab(Tab("Данные и МС", CONTENT_COLOR))
        self.tab_manager.add_tab(Tab("Отбор", CONTENT_COLOR))
        self.tab_manager.add_tab(Tab("TMVA", CONTENT_COLOR))
        self.tab_manager.add_tab(Tab("Результаты TMVA", CONTENT_COLOR))
        self.tab_manager.add_tab(Tab("Применение TMVA", CONTENT_COLOR))
        self.tab_manager.add_tab(Tab("Новые переменные", (255, 204, 204)))  # Длинное название

        # Поля ввода имеи для проекта
        self.proj_name_input = InputBox(WIDTH // 2 - 200, HEIGHT // 2 - 60, 400, 40, "проект 1")

        # Создаем InputBox для каждой частицы
        self.end_state_boxes = []
        spacing = 40  # Расстояние между полями ввода
        start_x = WIDTH // 5
        for i, label in enumerate(LABELS):
            input_box = InputBox(start_x + i * (80 + spacing), HEIGHT // 2 + 60, 80, 45, placeholder=label,
                                 need_to_validate=True)
            self.end_state_boxes.append(input_box)

        self.project_button = Button(text="Далее", font_size=46, x_offset=WIDTH // 2 - 150, y_offset=HEIGHT // 2 + 250,
                                width=300,
                                height=60, color=ACTIVE_BUTTON, pressed_color=INACTIVE_BUTTON)

        self.back_button = Button(text="Назад к выбору", font_size=46, x_offset=10,
                                  y_offset=SELECT_PUMPING_RECT.y,  width=300, height=60, color=ACTIVE_BUTTON,
                                  pressed_color=INACTIVE_BUTTON)

        # Data and MC tab


        self.pumping_list = RadioButtonsList(EXTENDED_PUMPINGS_RELEASE, y_offset_start=LISTS_START_Y_OFFSET + 5, spacing=50,
                                        x_offset=PUMPING_LIST_POSITION + TEXT_OFFSET_INSIDE_LIST,
                                        content_rect=pygame.Rect(PUMPING_LIST_POSITION, LISTS_START_Y_OFFSET,
                                                                 LISTS_WIDTH, LISTS_HEIGHT))

        self.modeling_signal_list = RadioButtonsList([], y_offset_start=LISTS_START_Y_OFFSET + 5, spacing=50,
                                                x_offset=MODELING_LIST_POSITION + TEXT_OFFSET_INSIDE_LIST,
                                                content_rect=pygame.Rect(MODELING_LIST_POSITION, LISTS_START_Y_OFFSET,
                                                                         LISTS_WIDTH, LISTS_HEIGHT // 2),
                                                multiple_choice=False)

        self.modeling_background_list = RadioButtonsList([], y_offset_start=SELECT_BACKGROUND_RECT.bottom + 15, spacing=50,
                                                    x_offset=MODELING_LIST_POSITION + TEXT_OFFSET_INSIDE_LIST,
                                                    content_rect=pygame.Rect(MODELING_LIST_POSITION,
                                                                             SELECT_BACKGROUND_RECT.bottom, LISTS_WIDTH,
                                                                             LISTS_HEIGHT // 2 - SELECT_BACKGROUND_RECT.height),
                                                    multiple_choice=True)

        self.ntuples_vars_list = RadioButtonsList([], y_offset_start=LISTS_START_Y_OFFSET + 5, spacing=50,
                                             x_offset=NTIPLE_VARS_LIST_POSITION + TEXT_OFFSET_INSIDE_LIST,
                                             content_rect=pygame.Rect(NTIPLE_VARS_LIST_POSITION, LISTS_START_Y_OFFSET,
                                                                      LISTS_WIDTH, LISTS_HEIGHT),
                                             multiple_choice=True, default_state=True)

        self.launch_task_button = Button(text="Запустить задание", font_size=46, x_offset=WIDTH // 2 - 200,
                                    y_offset=PUMPING_INFO_RECT.bottom + LISTS_OFFSET, width=400,
                                    height=60, color=ACTIVE_BUTTON, pressed_color=INACTIVE_BUTTON)

        self.link = Link("Подробнее",FONT,(0, 0, 0),TEXT_COLOR,
            (PUMPING_INFO_RECT.centerx, PUMPING_INFO_RECT.bottom - 2 * FONT.size("Подробнее")[1]),
            underline_offset=1,
            tooltip_text="Открыть в браузере")

        # Selections tab
        self.ntuples_vars_selected_list = RadioButtonsList([], y_offset_start=LISTS_START_Y_OFFSET + 5, spacing=50,
                                                      x_offset=PUMPING_LIST_POSITION + TEXT_OFFSET_INSIDE_LIST,
                                                      content_rect=pygame.Rect(PUMPING_LIST_POSITION,
                                                                               LISTS_START_Y_OFFSET, LISTS_WIDTH,
                                                                               LISTS_HEIGHT))

        self.beam_points_list = RadioButtonsList([], y_offset_start=LISTS_START_Y_OFFSET + LISTS_HEIGHT + LISTS_OFFSET + 5,
                                            spacing=50,
                                            x_offset=PUMPING_LIST_POSITION + TEXT_OFFSET_INSIDE_LIST,
                                            content_rect=pygame.Rect(PUMPING_LIST_POSITION,
                                                                     LISTS_START_Y_OFFSET + LISTS_HEIGHT + LISTS_OFFSET,
                                                                     LISTS_WIDTH, 250),
                                            multiple_choice=True, default_state=True)

        self.renew_hist_button = Button(text="перерисовать гистограммy", font_size=46,
                                   x_offset=WIDTH // 2 - 400 - DISTANCE_BETWEEN_X // 2,
                                   y_offset=PUMPING_INFO_RECT.bottom + LISTS_OFFSET, width=400,
                                   height=60, color=ACTIVE_BUTTON, pressed_color=INACTIVE_BUTTON)

        self.optimize_selections_button = Button(text="применить отбор ко всем", font_size=46,
                                            x_offset=WIDTH // 2 + DISTANCE_BETWEEN_X // 2,
                                            y_offset=PUMPING_INFO_RECT.bottom + LISTS_OFFSET, width=400,
                                            height=60, color=ACTIVE_BUTTON, pressed_color=INACTIVE_BUTTON)

        self.left_border_input = InputBox(INPUT_LIMITS_RECT.x + INPUT_LIMITS_RECT.w, INPUT_LIMITS_RECT.y + 10, 80,
                                     INPUT_HEIGHT, placeholder="0")
        self.right_border_input = InputBox(INPUT_LIMITS_RECT.x + INPUT_LIMITS_RECT.w + 80 + 10, INPUT_LIMITS_RECT.y + 10, 80,
                                      INPUT_HEIGHT, placeholder="1")
        self.selections_input = InputBox(INPUT_SELECTION_CONDITIONS_RECT.x + INPUT_SELECTION_CONDITIONS_RECT.w,
                                    INPUT_SELECTION_CONDITIONS_RECT.y + 10, w=LISTS_WIDTH + LISTS_OFFSET,
                                    h=INPUT_HEIGHT, placeholder="CutV25==1")

        # TMVA tab
        # this list almost the same as in Selections Tab, but it has multiple choice
        self.ntuples_vars_selected_list2 = RadioButtonsList([], y_offset_start=LISTS_START_Y_OFFSET + 5, spacing=50,
                                                           x_offset=PUMPING_LIST_POSITION + TEXT_OFFSET_INSIDE_LIST,
                                                           content_rect=pygame.Rect(PUMPING_LIST_POSITION,
                                                                                    LISTS_START_Y_OFFSET, LISTS_WIDTH,
                                                                                    LISTS_HEIGHT),
                                                           multiple_choice=True, default_state=True)

        self.backgrounds_list = RadioButtonsList([], y_offset_start=LISTS_START_Y_OFFSET + 5, spacing=50,
                                                x_offset=MODELING_LIST_POSITION + TEXT_OFFSET_INSIDE_LIST,
                                                content_rect=pygame.Rect(MODELING_LIST_POSITION, LISTS_START_Y_OFFSET,
                                                                         LISTS_WIDTH, LISTS_HEIGHT // 2),
                                                multiple_choice=True, default_state=True)

        self.signal_selection_input = InputBox(SELECTIONS_SIGNAL_INPUT.x + SELECTIONS_SIGNAL_INPUT.w,
                                               SELECTIONS_SIGNAL_INPUT.y + 10, LISTS_WIDTH*2 + 2*LISTS_OFFSET,
                                               INPUT_HEIGHT, placeholder="CutV25==1")

        self.backgrounds_selection_input = InputBox(SELECTIONS_BACKGR_INPUT.x + SELECTIONS_BACKGR_INPUT.w,
                                               SELECTIONS_BACKGR_INPUT.y + 10, LISTS_WIDTH*2 + 2*LISTS_OFFSET,
                                               INPUT_HEIGHT,
                                               placeholder="CutV25==1")

        self.discriminators_list = RadioButtonsList(DISCRIMINATORS, y_offset_start=LISTS_START_Y_OFFSET + 5, spacing=50,
                                             x_offset=NTIPLE_VARS_LIST_POSITION + TEXT_OFFSET_INSIDE_LIST,
                                             content_rect=pygame.Rect(NTIPLE_VARS_LIST_POSITION, LISTS_START_Y_OFFSET,
                                                                      LISTS_WIDTH, LISTS_HEIGHT),
                                             multiple_choice=True, default_state=True)

        self.launch_train_button = Button(text="Запустить обучение", font_size=46,
                                     x_offset=WIDTH // 2 - 200 - DISTANCE_BETWEEN_X // 2,
                                     y_offset=PUMPING_INFO_RECT.bottom + LISTS_OFFSET, width=400,
                                     height=60, color=ACTIVE_BUTTON, pressed_color=INACTIVE_BUTTON)


        # TMVA results Tab
        self.backgrounds_selected_list = RadioButtonsList([], y_offset_start=BKG_SELECTED_LIST_Y + 5, spacing=50,
                                                          x_offset=BKG_SELECTED_LIST_X + TEXT_OFFSET_INSIDE_LIST,
                                                          content_rect=pygame.Rect(BKG_SELECTED_LIST_X, BKG_SELECTED_LIST_Y,
                                                                     LISTS_WIDTH, 250),
                                                          multiple_choice=False, default_state=False)
        self.picture_buttons = []
        # Рассчитываем максимальное количество кнопок в одной колонке
        # Выравнивание по прямоугольнику с инфо о перекачке
        max_buttons_per_column = (LISTS_HEIGHT + LISTS_OFFSET) // (BUTTON_HEIGHT + SPACING)

        for i, (text, img) in enumerate(TMVA_IMAGE_BUTTON):
            # Определяем колонку (0 или 1)
            column = i // max_buttons_per_column
            row = i % max_buttons_per_column

            x_offset = BKG_SELECTED_LIST_X + column * (BUTTON_WIDTH + SPACING)
            y_offset = BKG_SELECTED_LIST_Y + 255 + row * (BUTTON_HEIGHT + SPACING)

            btn = PictureButton(
                text=text,
                font_size=30,
                x_offset=x_offset,
                y_offset=y_offset,
                width=BUTTON_WIDTH,
                height=BUTTON_HEIGHT,
                image_path=os.path.join("ML_APP/images", img) if img else None
            )
            self.picture_buttons.append(btn)

        # TMVA usage Tab
        self.discriminators_selected_list = RadioButtonsList([], y_offset_start=LISTS_START_Y_OFFSET + 5, spacing=50,
                                                      x_offset=PUMPING_LIST_POSITION + TEXT_OFFSET_INSIDE_LIST,
                                                      content_rect=pygame.Rect(PUMPING_LIST_POSITION,
                                                                               LISTS_START_Y_OFFSET, LISTS_WIDTH,
                                                                               LISTS_HEIGHT),
                                                      multiple_choice=True, default_state=True)

        self.generate_selector_button = Button(text="Применить", font_size=46, x_offset=WIDTH // 2 - 200,
                                    y_offset=PUMPING_INFO_RECT.bottom + LISTS_OFFSET, width=400,
                                    height=60, color=ACTIVE_BUTTON, pressed_color=INACTIVE_BUTTON)



    def handle_events(self, events):
        # Обработка событий
        for event in events:

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.tab_manager.handle_click(event)

            if self.tab_manager.active_tab is None:
                continue
            active_tab = self.tab_manager.tabs[self.tab_manager.active_tab]

            if active_tab.title == "Данные и МС":
                handle_events_Data_and_MC(event, self.pumping_list, self.modeling_signal_list,
                                          self.modeling_background_list,
                                          self.ntuples_vars_list, self.link, self.launch_task_button)

            if active_tab.title == "Проект":
                handle_events_Project(event, self.proj_name_input, self.project_button, self.tab_manager,
                                      self.end_state_boxes, self.back_button)

            if active_tab.title == "Отбор":
                handle_events_Selections(event, self.ntuples_vars_selected_list, self.beam_points_list,
                                         self.left_border_input,
                                         self.right_border_input, self.selections_input,
                                         self.optimize_selections_button, self.renew_hist_button)

            if active_tab.title == "TMVA":
                handle_events_TMVA(event, self.ntuples_vars_selected_list2, self.discriminators_list,
                                   self.backgrounds_list, self.backgrounds_selection_input, self.signal_selection_input,
                                   self.launch_train_button)

            if active_tab.title == "Новые переменные":
                pass

            if active_tab.title == "Результаты TMVA":
                handle_events_TMVA_results(event, self.picture_buttons, self.backgrounds_selected_list)
    def render(self, screen):
        # Отрисовка вкладок
        self.tab_manager.draw(screen)

        active_tab = self.tab_manager.tabs[self.tab_manager.active_tab]

        if active_tab.title == "Данные и МС":
            draw_Data_and_MC_tab(screen, self.pumping_list, self.modeling_signal_list,
                                 self.modeling_background_list,
                                 self.ntuples_vars_list, self.link, self.launch_task_button)

        if active_tab.title == "Проект":
            draw_Project_tab(screen, self.project_button, self.proj_name_input, self.end_state_boxes, self.back_button)

        if active_tab.title == "Отбор":
            draw_Selections_tab(screen, self.ntuples_vars_selected_list, self.beam_points_list,
                                self.left_border_input,
                                self.right_border_input, self.selections_input,
                                self.optimize_selections_button, self.renew_hist_button)
        if active_tab.title == "Новые переменные":
            pass
        if active_tab.title == "TMVA":
            draw_TMVA_tab(screen, self.ntuples_vars_selected_list2, self.discriminators_list, self.backgrounds_list,
                          self.backgrounds_selection_input, self.signal_selection_input,
                          self.launch_train_button)

        if active_tab.title == "Результаты TMVA":
            draw_TMVA_results_tab(screen, self.backgrounds_selected_list, self.picture_buttons)

        if active_tab.title == "Применение TMVA":
            draw_TMVA_usage(screen, self.discriminators_selected_list, self.generate_selector_button)