import pygame
font = pygame.font.Font(None, 46)


class Tab:
    def __init__(self, title, content_color):
        self.title = title
        self.width = max(180, font.size(title)[0] + 20)  # Автоматическая ширина
        self.content_color = content_color





