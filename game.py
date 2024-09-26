import pygame

from direction import Direction
from food import Food
from snake import Snake


class Game:
    def __init__(self) -> None:
        pygame.init()
        # Create a game window
        self.screen = pygame.display.set_mode((800, 800))  # e.g. (800, 600)
        pygame.display.set_caption("Snake Game 🐍")

        # game objects
        self.snake = Snake()
        self.food = Food()

    def run(self):
        running = True
        clock = pygame.time.Clock()

        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and not pause:
                        self.snake.direction = Direction.UP
                    elif event.key == pygame.K_DOWN and not pause:
                        self.snake.direction = Direction.DOWN
                    elif event.key == pygame.K_LEFT and not pause:
                        self.snake.direction = Direction.LEFT
                    elif event.key == pygame.K_RIGHT and not pause:
                        self.snake.direction = Direction.RIGHT
                    elif event.key == pygame.K_SPACE:
                        pause = False
                        self.snake = Snake()

            try:
                if not pause:
                    self.snake.update(self.food)
                    self.draw()
            except Exception:
                self.display_game_over()
                pause = True

            # Inside the game loop
            clock.tick(10)  # Limit to 60 FPS

    def draw(self):
        # Game Logic Here
        self.screen.fill((255, 255, 255))
        self.food.draw(self.screen)
        self.snake.draw(self.screen)
        pygame.display.flip()

    def display_game_over(self):
        self.screen.fill((255, 255, 255))
        font = pygame.font.SysFont("Arial", 36)  # (None, font size)
        text = font.render(
            "Game Over. Hit Space to restart!", True, (0, 0, 0)
        )  # text, antialias, color
        self.screen.blit(
            text, (400 - text.get_width() / 2, 400 - text.get_height() / 2)
        )
        pygame.display.flip()
