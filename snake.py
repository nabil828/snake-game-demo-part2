from dataclasses import dataclass
import random
import pygame

from direction import Direction


@dataclass
class Segment:
    x: int
    y: int


class Snake:
    def __init__(self) -> None:
        # self.x = 120
        # self.y = 120
        self.direction = Direction.RIGHT
        self.segments = [
            Segment(40, 120),
            Segment(80, 120),
            Segment(120, 120),
        ]  # the last element is the head

    def draw(self, screen):
        for segment in self.segments:
            pygame.draw.rect(screen, (0, 0, 0), (segment.x, segment.y, 40, 40))

    def set_head(self, segment):
        self.segments[-1] = segment

    def get_head(self):
        return self.segments[-1]

    head = property(get_head, set_head)

    def update(self, food):
        # - update all the segments except the head
        for i in range(0, len(self.segments) - 1):  # 0 1
            self.segments[i].x = self.segments[i + 1].x
            self.segments[i].y = self.segments[i + 1].y

        # - update the head
        if self.direction == Direction.RIGHT:
            self.head.x += 40
        elif self.direction == Direction.LEFT:
            self.head.x -= 40
        elif self.direction == Direction.UP:
            self.head.y -= 40
        elif self.direction == Direction.DOWN:
            self.head.y += 40

        def game_over():
            if (
                self.head.x > 800
                or self.head.x < 0
                or self.head.y < 0
                or self.head.y > 800
                or self.head in self.segments[:-1]
            ):
                return True
            return False

        if game_over():
            raise Exception("Game Over!")

        def detect_collision_with_food():
            if self.head.x == food.x and self.head.y == food.y:
                return True
            return False

        def increase_the_size_of_snake_by_one():
            self.segments.append(Segment(food.x, food.y))

        def change_the_location_of_the_food():
            food.x = random.randint(0, 19) * 40  # 0, 40, 80, 120, ..., 760
            food.y = random.randint(0, 19) * 40  # 0, 40, 80, 120, ..., 760

        if detect_collision_with_food():
            increase_the_size_of_snake_by_one()
            change_the_location_of_the_food()
