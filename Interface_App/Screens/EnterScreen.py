import pygame
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from TabsComponents.InputBox import InputBox
from Constants.colors import *
from Constants.sizes import *
from TabsDraw import draw_Enter_screen
from TabsComponents.Button import Button
from Helpers.enterHelpers import encrypt_credentials
from Screen import Screen
from ChooseScreen import ChooseScreen


class EnterScreen(Screen):
    def __init__(self):
        self.username_input = InputBox(WIDTH // 2 - 200, HEIGHT // 2 - 60, 400, 40, "ivanov")
        self.password_input = InputBox(WIDTH // 2 - 200, HEIGHT // 2 + 60, 400, 40, "password123", password=True)
        self.next_button = Button(text="Далее", font_size=46, x_offset=WIDTH // 2 - 100, y_offset=HEIGHT // 2 + 250, width=200, height=60, color=ACTIVE_BUTTON, pressed_color=INACTIVE_BUTTON)

    def handle_events(self, events):
        for event in events:
            self.username_input.handle_event(event)
            self.password_input.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.next_button.is_clicked(event.pos):
                    if self.username_input.text and self.password_input.text:
                        encrypt_credentials(self.username_input.text, self.password_input.text)
                    return ChooseScreen()



    def render(self, screen):
        draw_Enter_screen(screen, self.username_input, self.password_input, self.next_button)