"""
-*- coding: utf-8 -*-
Written by: sme30393
Date: 17/10/2021
"""
from src.game.object_builder import Snake, Apple


class InputVector:

    def __init__(self, snake: Snake, apple: Apple):

        self.snake = snake
        self.apple = apple
        self.width = self.snake.width
        self.height = self.snake.height
        self.step_size = self.snake.step_size
        self.boundary = self.snake.boundary
        self.snake_coordinates = self.list_snake_coordinates()

    def compute(self) -> list:

        vector_apple = self.respect_to_apple()
        vector_collision_object = self.check_sides()
        return vector_apple + vector_collision_object

    def respect_to_apple(self) -> list:
        return [
            self.apple.x < self.snake.x[0],
            self.apple.x > self.snake.x[0],
            self.apple.y < self.snake.y[0],
            self.apple.y > self.snake.y[0]
        ]

    def check_sides(self) -> list:
        return [self.side_clear(side=side) for side in ["right", "left", "bottom", "top"]]

    def side_clear(self, side: str) -> bool:

        if side == "right":
            return self.right_side_clear()
        elif side == "left":
            return self.left_side_clear()
        elif side == "top":
            return self.top_side_clear()
        return self.bottom_side_clear()

    def list_snake_coordinates(self):
        return [(x, y) for x, y in zip(self.snake.x[:self.snake.length], self.snake.y[:self.snake.length])]

    def right_side_clear(self) -> bool:
        if self.boundary and self.snake.x[0] == self.width:
            return False
        if self.periodic_obstruction_horizontal(edge=self.width - self.step_size, x_obstruction=0):
            return False
        if self.snake_obstruction_horizontal(x_obstruction=self.snake.x[0] + self.step_size):
            return False
        return True

    def left_side_clear(self) -> bool:
        if self.boundary and self.snake.x[0] == 0:
            return False
        if self.periodic_obstruction_horizontal(edge=0, x_obstruction=self.width):
            return False
        if self.snake_obstruction_horizontal(x_obstruction=self.snake.x[0] - self.step_size):
            return False
        return True

    def bottom_side_clear(self):
        if self.boundary and self.snake.y[0] == self.height:
            return False
        if self.periodic_obstruction_vertical(edge=0, y_obstruction=self.height - self.step_size):
            return False
        if self.snake_obstruction_vertical(y_obstruction=self.snake.y[0] + self.step_size):
            return False
        return True

    def top_side_clear(self):
        if self.boundary and self.snake.y[0] == 0:
            return False
        if self.periodic_obstruction_vertical(edge=self.height - self.step_size, y_obstruction=0):
            return False
        if self.snake_obstruction_vertical(y_obstruction=self.snake.y[0] - self.step_size):
            return False
        return True

    def periodic_obstruction_horizontal(self, edge: int, x_obstruction: int) -> bool:
        return self.snake.x[0] == edge and any(
            [x == x_obstruction and y == self.snake.y[0] for x, y in self.snake_coordinates[1:]]
        )

    def periodic_obstruction_vertical(self, edge: int, y_obstruction: int) -> bool:
        return self.snake.y[0] == edge and any(
            [x == self.snake.x[0] and y == y_obstruction for x, y in self.snake_coordinates[1:]]
        )

    def snake_obstruction_horizontal(self, x_obstruction: int) -> bool:
        return any([a == (x_obstruction, self.snake.y[0]) for a in self.snake_coordinates])

    def snake_obstruction_vertical(self, y_obstruction: int) -> bool:
        return any([a == (self.snake.x[0], y_obstruction) for a in self.snake_coordinates])


def main():
    pass


if __name__ == "__main__":
    main()
