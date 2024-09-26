import pygame


class Food:
    def __init__(self) -> None:
        self.x = 200
        self.y = 200

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, 40, 40))
