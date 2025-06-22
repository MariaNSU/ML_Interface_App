import pygame
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Constants.colors import *
from Constants.sizes import *
from Constants.figures import SELECT_PUMPING_RECT

from TabsDraw import draw_Choose_screen
from TabsComponents.Button import Button

from Screen import Screen
from NewProjectTabsScreen import NewProjectTabsScreen
from ExistingDataTabsScreen import ExistingDataTabsScreen



BASE_PATH = os.getcwd()

class ChooseScreen(Screen):
    def __init__(self):
        self.new_project_button = Button(text="Создать новый проект", font_size=46, x_offset=WIDTH // 2 - 900 - LISTS_OFFSET // 2, y_offset=HEIGHT // 2, width=600, height=60, color=ACTIVE_BUTTON, pressed_color=INACTIVE_BUTTON)
        self.existing_project_button = Button(text="Выбрать существующий проект", font_size=46, x_offset=WIDTH // 2 - 300, y_offset=HEIGHT // 2, width=600, height=60, color=ACTIVE_BUTTON, pressed_color=INACTIVE_BUTTON)
        self.own_data_button = Button(text="Работа со своими данными", font_size=46, x_offset=WIDTH // 2 + 300 + LISTS_OFFSET // 2, y_offset=HEIGHT // 2, width=600, height=60, color=ACTIVE_BUTTON, pressed_color=INACTIVE_BUTTON)
        self.back_button = Button(text="Назад", font_size=46, x_offset=10,
                                  y_offset=SELECT_PUMPING_RECT.y,  width=300, height=60, color=ACTIVE_BUTTON,
                                  pressed_color=INACTIVE_BUTTON)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.new_project_button.is_clicked(event.pos):
                    return NewProjectTabsScreen()

                elif self.own_data_button.is_clicked(event.pos):
                    pass
                    return ExistingDataTabsScreen()

                elif self.existing_project_button.is_clicked(event.pos):
                    pass
                    #return ExistingProjectsScreen()
                '''elif self.back_button.is_clicked(event.pos):
                    return EnterScreen()'''


    def render(self, screen):
        draw_Choose_screen(screen, self.new_project_button, self.existing_project_button, self.own_data_button, self.back_button)
