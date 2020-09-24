import pygame
from typing import Tuple
from pathlib import Path

path_to_img_folder = Path(__file__).parent.parent.joinpath("images")

PATH_TO_WALL = path_to_img_folder.joinpath("wall.jpg")
PATH_TO_BOX = path_to_img_folder.joinpath("rock.bmp")
PATH_TO_FOE = path_to_img_folder.joinpath("wall.bmp")
PATH_TO_EMPTY = path_to_img_folder.joinpath("grass.png")
PATH_TO_PLAYER = path_to_img_folder.joinpath("frames/ErWiNom_1x1.png")

wall_char = 'w'
box_char = 'b'
foe_char = 'f'
empty_char = ' '

class Model():
    def __init__(self, field_x: int = -1, field_y: int = -1, model_type: str = ''):
        if model_type == '':
            self.idle_img = pygame.image.load(str(PATH_TO_EMPTY))
        elif model_type == 'w':
            self.idle_img = pygame.image.load(str(PATH_TO_WALL))
        elif model_type == 'b':
            self.idle_img = pygame.image.load(str(PATH_TO_BOX))
        elif model_type == 'f':
            self.idle_img = pygame.image.load(str(PATH_TO_FOE))
        elif model_type == "player":
            self.idle_img = pygame.image.load(str(PATH_TO_PLAYER))

        self.frames = {"current": self.idle_img, "IDLE": self.idle_img}
        self.width, self.height = self.idle_img.get_size()
        self.current_frame = 0
        self.x = -1
        self.y = -1
        self.field_x = field_x
        self.field_y = field_y
        self.layer = 0  # objects intersect/get collision only if they are one the same layer
        self.x_velocity = 0
        self.y_velocity = 0
        self.type = model_type
        self.movable = True
        self.field = None

    def set_x_coordinate(self, x: int):
        self.x = x

    def set_y_coordinate(self, y: int):
        self.y = y

    def get_coordinates(self) -> Tuple[int, int]:
        return self.x, self.y

    def add_frame(self, path_to_frame, frame_name) -> bool:
        """
        Adds a frame to the model.
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

    def set_field(self, field):
        self.field = field

    def move(self, direction: str):
        next_object: Model = Model()
        if direction == "up":
            if self.field_y <= 0:  # if model is on the first cell of the field
                return
            next_object = self.field[self.field_y - 1][self.field_x]
            if next_object is None:  # empty space - move up
                self.field_y -= 1
                self.field[self.field_y][self.field_x] = self
                self.field[self.field_y + 1][self.field_x] = None
                return
        elif direction == "right":
            if self.field_x >= self.field.width - 1:  # if model is on the rightest cell of the field
                return
            next_object = self.field[self.field_y][self.field_x + 1]
            if next_object is None:  # empty space - move right
                self.field_x += 1
                self.field[self.field_y][self.field_x] = self
                self.field[self.field_y][self.field_x - 1] = None
                return
        elif direction == "down":
            if self.field_y >= self.field.height - 1:  # if model is on the last cell of the field
                return
            next_object = self.field[self.field_y + 1][self.field_x]
            if next_object is None:  # empty space - move down
                self.field_y += 1
                self.field[self.field_y][self.field_x] = self
                self.field[self.field_y - 1][self.field_x] = None
                return
        elif direction == "left":
            if self.field_x <= 0:  # if model is on the leftest cell of the field
                return
            next_object = self.field[self.field_y][self.field_x - 1]
            if next_object is None:  # empty space - move left
                self.field_x -= 1
                self.field[self.field_y][self.field_x] = self
                self.field[self.field_y][self.field_x + 1] = None
                return

        if not next_object.is_movable():
            return
        elif next_object.type == foe_char:
            print(f"{self.type} foe interaction")
        elif next_object.type == box_char:
            if self.type == "player":  # only player can move boxes, not other boxes or foes
                next_object.move(direction)

    def get_screen_position(self):
        if self.field is None:
            print(f"You must specify the field for the model at {self.field_x}, {self.field_y}!\nUse set_field method.")
            return 0, 0
        return self.field.shift_x + self.field_x * self.field.cell_size, \
               self.field.shift_y + self.field_y * self.field.cell_size


class Player(Model):
    def __init__(self, field_x: int = 0, field_y: int = 0):
        super().__init__(field_x, field_y, model_type="player")
        self.idle_delay = 60
        self.idle_time = 0

    def set_idle_delay(self, delay: int):
        self.idle_delay = delay
