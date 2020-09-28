import pygame

wall_char = 'w'
box_char = 'b'
foe_char = 'f'
empty_char = ' '
WHITE_RGB = (255, 255, 255)
BLACK_RGB = (0, 0, 0)

EMPTY_MODEL_TYPE = ' '


class Model():
    def __init__(self, field_x: int = -1, field_y: int = -1, model_type: str = ''):
        self.field_x = field_x
        self.field_y = field_y
        self.type = model_type
        self.surface_size = (40, 40)

        self.default_surface = pygame.Surface(self.surface_size)
        self.default_surface.fill(WHITE_RGB)
        self.default_surface.blit(pygame.font.Font(None, 44).render(model_type, 1, BLACK_RGB), (6, 6))

        self.frames = {"current": self.default_surface, "default": self.default_surface}
        self.movable = False
        self.field = None

    def add_frame(self, path_to_frame, frame_name) -> bool:
        """
        Adds a frame to the model.
        :param path_to_frame: path to jpg/ png/ bmp file with a frame
        :param frame_name: name of the frame in frame dictionary
        :return: Return True if frame was added and False if there is a frame with given name
        """
        if frame_name in self.frames:
            return False
        else:
            frame = pygame.image.load(path_to_frame)
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
            next_object = self.field[self.field_x][self.field_y - 1]
        elif direction == "right":
            if self.field_x >= self.field.width - 1:  # if model is on the rightest cell of the field
                return
            next_object = self.field[self.field_x + 1][self.field_y]
        elif direction == "down":
            if self.field_y >= self.field.height - 1:  # if model is on the last cell of the field
                return
            next_object = self.field[self.field_x][self.field_y + 1]
        elif direction == "left":
            if self.field_x <= 0:  # if model is on the leftest cell of the field
                return
            next_object = self.field[self.field_x - 1][self.field_y]
        if next_object.type == ' ':  # empty space - move up
            self.field.swap(self, next_object)
            return

        if next_object.type == foe_char:
            print(f"{self.type} foe interaction")
        elif not next_object.is_movable():
            pass
        elif next_object.type == box_char:
            if self.type == "p":  # only player can move boxes, not other boxes or foes
                next_object.move(direction)

    def get_screen_position(self):
        return self.field.shift_x + self.field_x * self.field.cell_size, \
               self.field.shift_y + self.field_y * self.field.cell_size
