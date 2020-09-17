import pygame
from typing import Tuple, NewType


class Model():
    def __init__(self, path_to_img: str, x: int = 0, y: int = 0):
        self.idle_img = pygame.image.load(path_to_img)
        self.width, self.height = self.idle_img.get_size()
        self.frames = {"current": self.idle_img, "IDLE": self.idle_img}
        self.current_frame = 0
        self.x = x
        self.y = y
        self.layer = 0  # objects intersect/get collision only if they are one the same layer
        self.x_velocity = 0
        self.y_velocity = 0
        self.type = ''
        self.movable = True

    def set_x_coordinate(self, x: int):
        self.x = x

    def set_y_coordinate(self, y: int):
        self.y = y

    def get_coordinates(self) -> Tuple[int, int]:
        return self.x, self.y

    def add_frame(self, path_to_frame, frame_name) -> bool:
        """
        Adds frames to the model.
        :param path_to_frame: path to jpg, png, bmp file with a frame
        :param frame_name: name of the frame in frame dictionary
        :return: Return True if frame was added and False if there is a frame with given name
        """
        if frame_name in self.frames:
            return False
        else:
            frame = pygame.image.load(path_to_frame)
            if frame.get_size() != (self.width, self.height):
                print(f"Warning! The frame {frame_name} size is {frame.get_size()} "
                      f"while model size is ({self.width}, {self.height})")
            self.frames[frame_name] = frame
            return True

    def set_current_frame(self, frame_name: str) -> bool:
        """
        Tries to set frame with given name as current frame
        :param frame_name: Name of the frame in self.frames dictionary
        :return: True if frame is set False else
        """
        if frame_name in self.frames:
            self.frames["current"] = self.frames[frame_name]
            return True
        return False

    def get_current_frame(self) -> str:
        """
        Goes through the frame dict and find the name of current frame
        :return: name of the current frame
        """
        for f in self.frames:
            if self.frames[f] is self.frames["current"]:
                return f

    def is_movable(self) -> bool:
        return self.movable

class Player(Model):
    def __init__(self, path_to_img: str, x: int = 0, y: int = 0):
        super().__init__(path_to_img, x, y)
        self.idle_delay = 60
        self.idle_time = 0
        self.type = "player"

    def set_idle_delay(self, delay: int):
        self.idle_delay = delay
