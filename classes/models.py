import pygame
from typing import Tuple


class model():
    def __init__(self, path_to_img: str, x:int = 0, y:int = 0):
        self.img = pygame.image.load(path_to_img)
        self.x = x
        self.y = y
        self.x_velocity = 0
        self.y_velocity = 0

    def set_x_velocity(self, velocity: int = 1) -> None:
        self.x_velocity = 1

    def set_y_velocity(self, velocity: int = 1) -> None:
        self.y_velocity = 1

    def get_coordinates(self) -> Tuple[int, int]:
        return self.x, self.y

    def update_coordinates(self) -> None:
        self.x += self.x_velocity
        self.y += self.y_velocity
