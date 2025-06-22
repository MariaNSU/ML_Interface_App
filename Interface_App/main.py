import pygame
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Constants.colors import *
from Constants.sizes import *
from Screens.EnterScreen import EnterScreen
from Helpers.execute_local_commands import remove_key_and_enc_files

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
BASE_PATH = os.getcwd()

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Enter")


class ScreenManager:
    def __init__(self):
        self.current_screen = EnterScreen()

    def handle_events(self, events):
        next_screen = self.current_screen.handle_events(events)
        if next_screen:
            self.current_screen = next_screen

    def render(self, screen):
        self.current_screen.render(screen)

def main():
    screen_manager = ScreenManager()
    running = True
    clock = pygame.time.Clock()

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        screen.fill(CONTENT_COLOR)
        screen_manager.handle_events(events)
        screen_manager.render(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    remove_key_and_enc_files() # чистим пароли и ключи после закрытия программы


main()
