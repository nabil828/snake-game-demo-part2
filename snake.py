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
        self.auto_pilot = False
        self.auto_pilot_path = []
        self.auto_pilot_visited = []
        self.strategy = "bfs"

    def draw(self, screen):
        # the visited nodes
        for segment in self.auto_pilot_visited:
            pygame.draw.rect(screen, (66, 135, 245), (segment.x, segment.y, 40, 40))

        # path
        for segment in self.auto_pilot_path:
            pygame.draw.rect(screen, (252, 186, 3), (segment.x, segment.y, 40, 40))

        for segment in self.segments:
            pygame.draw.rect(screen, (0, 0, 0), (segment.x, segment.y, 40, 40))

    def set_head(self, segment):
        self.segments[-1] = segment

    def get_head(self):
        return self.segments[-1]

    head = property(get_head, set_head)

    def update(self, food, wall):
        # - update all the segments except the head
        for i in range(0, len(self.segments) - 1):  # 0 1
            self.segments[i].x = self.segments[i + 1].x
            self.segments[i].y = self.segments[i + 1].y

        class NoFoodFoundException(Exception):
            pass

        def find_path_bfs():
            visited = []
            queue = []
            visited.append(self.head)
            queue.append((self.head, [self.head]))

            #! this can be refactored
            def find_valid_neighbors(a_segment):
                valid_neigbors = []
                if a_segment.x > 0:
                    valid_neigbors.append(Segment(a_segment.x - 40, a_segment.y))
                if a_segment.x < 760:
                    valid_neigbors.append(Segment(a_segment.x + 40, a_segment.y))
                if a_segment.y < 760:
                    valid_neigbors.append(Segment(y=a_segment.y + 40, x=a_segment.x))
                if a_segment.y > 0:
                    valid_neigbors.append(Segment(y=a_segment.y - 40, x=a_segment.x))

                for a_neighbor in valid_neigbors:
                    if a_neighbor in self.segments:
                        valid_neigbors.remove(a_neighbor)

                for a_neighbor in valid_neigbors:
                    if a_neighbor in wall.segments:
                        valid_neigbors.remove(a_neighbor)

                return valid_neigbors

            while queue:
                a_segment, path = queue.pop(0)

                if a_segment.x == food.x and a_segment.y == food.y:
                    self.auto_pilot_visited = visited
                    self.auto_pilot_path = path
                    return path

                valid_neighbors = find_valid_neighbors(a_segment)

                for a_valid_neighbor in valid_neighbors:
                    if a_valid_neighbor not in visited:
                        visited.append(a_valid_neighbor)
                        queue.append((a_valid_neighbor, path + [a_valid_neighbor]))
            raise NoFoodFoundException("")

        def find_path_dfs():
            visited = []
            stack = []
            visited.append(self.head)
            stack.append((self.head, [self.head]))

            def find_valid_neighbors(a_segment):
                valid_neigbors = []
                if a_segment.x > 0:
                    valid_neigbors.append(Segment(a_segment.x - 40, a_segment.y))
                if a_segment.x < 760:
                    valid_neigbors.append(Segment(a_segment.x + 40, a_segment.y))
                if a_segment.y < 760:
                    valid_neigbors.append(Segment(y=a_segment.y + 40, x=a_segment.x))
                if a_segment.y > 0:
                    valid_neigbors.append(Segment(y=a_segment.y - 40, x=a_segment.x))

                for a_neighbor in valid_neigbors:
                    if a_neighbor in self.segments:
                        valid_neigbors.remove(a_neighbor)

                return valid_neigbors

            while stack:
                a_segment, path = stack.pop()

                if a_segment.x == food.x and a_segment.y == food.y:
                    self.auto_pilot_visited = visited
                    self.auto_pilot_path = path
                    return path

                valid_neighbors = find_valid_neighbors(a_segment)

                for a_valid_neighbor in valid_neighbors:
                    if a_valid_neighbor not in visited:
                        visited.append(a_valid_neighbor)
                        stack.append((a_valid_neighbor, path + [a_valid_neighbor]))
            raise NoFoodFoundException("")

        if self.auto_pilot == True:
            if len(self.auto_pilot_path) == 0:
                # ❗can be refactored using DIP
                if self.strategy == "bfs":
                    find_path_bfs()
                elif self.strategy == "dfs":
                    find_path_dfs()
                else:
                    pass

            # path[1] is the first element of the path to the food
            if self.auto_pilot_path[1].y > self.head.y:
                self.direction = Direction.DOWN
            elif self.auto_pilot_path[1].y < self.head.y:
                self.direction = Direction.UP
            elif self.auto_pilot_path[1].x > self.head.x:
                self.direction = Direction.RIGHT
            elif self.auto_pilot_path[1].x < self.head.x:
                self.direction = Direction.LEFT
            self.auto_pilot_path.pop(0)

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
                or self.head in wall.segments
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

            if Segment(food.x, food.y) in self.segments:
                change_the_location_of_the_food()
            self.auto_pilot_path = []
            self.auto_pilot_visited = []

        if detect_collision_with_food():
            increase_the_size_of_snake_by_one()
            change_the_location_of_the_food()
