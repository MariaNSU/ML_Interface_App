import pygame
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from TabsComponents.RadioButtonsList import RadioButtonsList
from TabsComponents.Button import Button
from TabsComponents.InputBox import InputBox
from TabsComponents.Tab import Tab
from TabsComponents.TabManager import TabManager

from TabsDraw import draw_Existing_Data_tab, draw_Selections_tab, draw_TMVA_tab
from TabsEventHandlers import handle_events_Existing_Data

from Constants.colors import *
from Constants.lists import EXTENDED_PUMPINGS_RELEASE, DISCRIMINATORS
from Constants.sizes import *
from Constants.figures import (PUMPING_INFO_RECT, INPUT_LIMITS_RECT, INPUT_SELECTION_CONDITIONS_RECT,
                               DISCRIMINATORS_RECT, SELECT_PUMPING_RECT)

pygame.init()
from Screen import Screen


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class ExistingDataTabsScreen(Screen):

    def __init__(self):
        self.tab_manager = TabManager()
        self.tab_manager.add_tab(Tab("Данные и МС", CONTENT_COLOR))
        self.tab_manager.add_tab(Tab("Отбор", CONTENT_COLOR))
        self.tab_manager.add_tab(Tab("TMVA", CONTENT_COLOR))
        self.tab_manager.add_tab(Tab("Новые переменные", (255, 204, 204)))

        # Data
        self.data_var_input = InputBox(START_INPUT_X, START_INPUT_Y, VAR_INPUT_WIDTH, INPUT_HEIGHT, "exnn22")
        self.data_filename_input = InputBox(START_INPUT_X + VAR_INPUT_WIDTH + DISTANCE_BETWEEN_X, START_INPUT_Y,
                                      FILENAME_INPUT_WIDTH, INPUT_HEIGHT, "listNN22.txt")
        self.data_path_input = InputBox(START_INPUT_X + VAR_INPUT_WIDTH + 2 * DISTANCE_BETWEEN_X + FILENAME_INPUT_WIDTH,
                                   START_INPUT_Y,
                                   PATH_INPUT_WIDTH, INPUT_HEIGHT, "/online/users2/username/release/output/")
        # Signal
        self.signal_var_input = InputBox(START_INPUT_X, SIGNAL_INPUT_START_Y, VAR_INPUT_WIDTH, INPUT_HEIGHT, "mc22")
        self.signal_filename_input = InputBox(START_INPUT_X + VAR_INPUT_WIDTH + DISTANCE_BETWEEN_X, SIGNAL_INPUT_START_Y,
                                    FILENAME_INPUT_WIDTH, 50, "listMC22.txt")
        self.signal_path_input = InputBox(START_INPUT_X + VAR_INPUT_WIDTH + 2 * DISTANCE_BETWEEN_Y + FILENAME_INPUT_WIDTH,
                             SIGNAL_INPUT_START_Y, PATH_INPUT_WIDTH, 50,
                                    "/online/users2/username/release/output/")

        # Background
        self.background_var_input = InputBox(START_INPUT_X, BACKGROUND_INPUT_START_Y, VAR_INPUT_WIDTH, INPUT_HEIGHT, "hd22")
        self.background_filename_input = InputBox(START_INPUT_X + VAR_INPUT_WIDTH + DISTANCE_BETWEEN_X,
                                             BACKGROUND_INPUT_START_Y,
                                             FILENAME_INPUT_WIDTH, 50, "listHD22.txt")
        self.background_path_input = InputBox(
            START_INPUT_X + VAR_INPUT_WIDTH + 2 * DISTANCE_BETWEEN_X + FILENAME_INPUT_WIDTH,
            BACKGROUND_INPUT_START_Y, PATH_INPUT_WIDTH, INPUT_HEIGHT, "/online/users2/username/release/output/")

        # for choosing pumping
        self.pumping_list = RadioButtonsList(EXTENDED_PUMPINGS_RELEASE, y_offset_start=PUMPINGS_LIST_START_Y, spacing=50,
                                        x_offset=WIDTH // 2 - LISTS_WIDTH // 2 + TEXT_OFFSET_INSIDE_LIST,
                                        content_rect=pygame.Rect(WIDTH // 2 - LISTS_WIDTH // 2, PUMPINGS_LIST_START_Y,
                                                                 LISTS_WIDTH, LISTS_HEIGHT // 2.5))

        self.go_to_draw_button = Button(text="перейти к рисованию", font_size=46,
                                   x_offset=WIDTH // 2 - 400 - DISTANCE_BETWEEN_X // 2,
                                   y_offset=PUMPING_INFO_RECT.bottom + LISTS_OFFSET, width=400,
                                   height=50, color=ACTIVE_BUTTON, pressed_color=INACTIVE_BUTTON)

        self.add_background_button = Button(text="добавить фон", font_size=46, x_offset=WIDTH // 2 + DISTANCE_BETWEEN_X // 2,
                               y_offset=PUMPING_INFO_RECT.bottom + LISTS_OFFSET, width=400,
                                       height=50, color=ACTIVE_BUTTON, pressed_color=INACTIVE_BUTTON)

        # Dictionary mapping variable names to their corresponding InputBox instances
        self.input_boxes = {
            "data_var_input": self.data_var_input,
            "data_filename_input": self.data_filename_input,
            "data_path_input": self.data_path_input,
            "signal_var_input": self.signal_var_input,
            "signal_filename_input": self.signal_filename_input,
            "signal_path_input": self.signal_path_input,
            "background_var_input": self.background_var_input,
            "background_filename_input": self.background_filename_input,
            "background_path_input": self.background_path_input,
        }

        self.back_button = Button(text="Назад к выбору", font_size=46, x_offset=10,
                                  y_offset=SELECT_PUMPING_RECT.y,  width=300, height=60, color=ACTIVE_BUTTON,
                                  pressed_color=INACTIVE_BUTTON)

        # Selections tab
        self.ntuples_vars_selected_list = RadioButtonsList([], y_offset_start=LISTS_START_Y_OFFSET + 5, spacing=50,
                                                           x_offset=PUMPING_LIST_POSITION + TEXT_OFFSET_INSIDE_LIST,
                                                           content_rect=pygame.Rect(PUMPING_LIST_POSITION,
                                                                                    LISTS_START_Y_OFFSET, LISTS_WIDTH,
                                                                                    LISTS_HEIGHT))

        self.beam_points_list = RadioButtonsList([],
                                                 y_offset_start=LISTS_START_Y_OFFSET + LISTS_HEIGHT + LISTS_OFFSET + 5,
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
        self.right_border_input = InputBox(INPUT_LIMITS_RECT.x + INPUT_LIMITS_RECT.w + 80 + 10,
                                           INPUT_LIMITS_RECT.y + 10, 80,
                                           INPUT_HEIGHT, placeholder="1")
        self.selections_input = InputBox(INPUT_SELECTION_CONDITIONS_RECT.x + INPUT_SELECTION_CONDITIONS_RECT.w,
                                         INPUT_SELECTION_CONDITIONS_RECT.y + 10, w=LISTS_WIDTH + LISTS_OFFSET,
                                         h=INPUT_HEIGHT, placeholder="CutV25==1")

        # TMVA tab
        self.backgrounds_list = RadioButtonsList([], y_offset_start=LISTS_START_Y_OFFSET + 5, spacing=50,
                                                x_offset=MODELING_LIST_POSITION + TEXT_OFFSET_INSIDE_LIST,
                                                content_rect=pygame.Rect(MODELING_LIST_POSITION, LISTS_START_Y_OFFSET,
                                                                         LISTS_WIDTH, LISTS_HEIGHT // 2),
                                                multiple_choice=True, default_state=True)

        self.signal_selection_input = InputBox(INPUT_LIMITS_RECT.x + INPUT_LIMITS_RECT.w, INPUT_LIMITS_RECT.y + 10, 390,
                                               INPUT_HEIGHT, placeholder="CutV25==1")

        self.backgrounds_selection_input = InputBox(
            INPUT_SELECTION_CONDITIONS_RECT.x + INPUT_SELECTION_CONDITIONS_RECT.w,
            INPUT_SELECTION_CONDITIONS_RECT.y + 10, 390, INPUT_HEIGHT,
            placeholder="CutV25==1")

        self.discriminators_list = RadioButtonsList(DISCRIMINATORS, y_offset_start=LISTS_START_Y_OFFSET + 5, spacing=50,
                                             x_offset=NTIPLE_VARS_LIST_POSITION + TEXT_OFFSET_INSIDE_LIST,
                                             content_rect=pygame.Rect(NTIPLE_VARS_LIST_POSITION, LISTS_START_Y_OFFSET,
                                                                      LISTS_WIDTH, LISTS_HEIGHT),
                                             multiple_choice=True, default_state=True)

        self.launch_train_button = Button(text="Запустить обучение", font_size=46,
                                          x_offset=WIDTH // 2 - 400 - DISTANCE_BETWEEN_X // 2,
                                          y_offset=PUMPING_INFO_RECT.bottom + LISTS_OFFSET, width=400,
                                          height=60, color=ACTIVE_BUTTON, pressed_color=INACTIVE_BUTTON)

        self.show_results_button = Button(text="Показать результаты", font_size=46,
                                          x_offset=WIDTH // 2 + DISTANCE_BETWEEN_X // 2,
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
                handle_events_Existing_Data(event, self.input_boxes, self.pumping_list,
                                            self.go_to_draw_button, self.add_background_button)

            if active_tab.title == "Отбор":
                pass

    def render(self, screen):
        # Отрисовка вкладок
        self.tab_manager.draw(screen)

        active_tab = self.tab_manager.tabs[self.tab_manager.active_tab]

        if active_tab.title == "Данные и МС":
            # TODO
            # add warnings if there is no data in input boxes
            draw_Existing_Data_tab(screen, self.data_var_input, self.data_filename_input, self.data_path_input, self.signal_var_input,
                                    self.signal_filename_input, self.signal_path_input, self.background_var_input,
                                    self.background_filename_input,
                                    self.background_path_input, self.pumping_list, self.go_to_draw_button, self.add_background_button)

        if active_tab.title == "Отбор":
            draw_Selections_tab(screen, self.ntuples_vars_selected_list, self.beam_points_list,
                                 self.left_border_input,
                                 self.right_border_input, self.selections_input,
                                 self.optimize_selections_button, self.renew_hist_button)
        if active_tab.title == "Новые переменные":
            pass
        if active_tab.title == "TMVA":
            draw_TMVA_tab(screen, self.ntuples_vars_selected_list, self.discriminators_list, self.backgrounds_list,
                              self.backgrounds_selection_input, self.signal_selection_input,
                              self.launch_train_button)
