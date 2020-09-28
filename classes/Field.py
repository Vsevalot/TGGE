from random import random
from typing import Dict
from classes.models import Model

field_name = "test_field.field"

wall_chance = 0.05
box_chance = 0.01
foe_chance = 0.02

wall_char = 'w'
box_char = 'b'
foe_char = 'f'
empty_char = ' '

class PlayerNotFound(Exception):
   pass


class Field(object):
    def __init__(self, path_to_field: str, cell_size: int = 40):
        self.player_x = -1
        self.player_y = -1
        self.field = Field.read_field(self, path_to_field, cell_size)
        self.cell_size = cell_size
        self.width = len(self.field)
        self.height = len(self.field[0])
        self.shift_x = 0
        self.shift_y = 0
        self.background = None
        self.floor = None

    def __getitem__(self, item):
        return self.field[item]

    def swap(self, element1: Model, element2: Model) -> None:
        """
        Swaps two elements in the field
        :param element1: first element
        :param element2: second element
        :return: None
        """
        self[element1.field_x][element1.field_y] = element2
        self[element2.field_x][element2.field_y] = element1

        first_x, first_y = element1.field_x, element1.field_y
        element1.field_x = element2.field_x
        element1.field_y = element2.field_y
        element2.field_x = first_x
        element2.field_y = first_y

    def set_background(self, background_surface):
        self.background = background_surface

    def set_floor(self, floor_surface):
        self.floor = floor_surface

    def set_shift(self, x: int, y: int):
        """

        :param x:
        :param y:
        :return:
        """
        self.shift_x = x
        self.shift_y = y

    def add_player(self, player_model, x: int = -1, y:int = -1):
        """
        X and Y would be reversed cos field is a filed of rows => the first index is row and the second is column
        :param player_model:
        :param x:
        :param y:
        :return:
        """
        if x == -1 or y == -1:  # if no coordinates given - place at the first empty cell
            for i in range(len(self.field)):
                for k in range(len(self.field[0])):
                    if self[i][k] is None:
                        player_model.field_x = k
                        player_model.field_y = i
                        self.player_x = k
                        self.player_y = i
                        self[i][k] = player_model
                        return
        else:
            self[y][x] = player_model
            self.player_x = y
            self.player_y = x
            player_model.field_x = x
            player_model.field_y = y

    def get_player(self):
        if self.player_x == -1 or self.player_y == -1:
            raise PlayerNotFound("You must specify player's position on the field. Make sure the field has 'p' char")
        return self[self.player_x][self.player_y]

    def read_field(self, path_to_field: str, cell_size: int = 40) -> list:
        """
        Reads a field from a file in the given path and generates a field of game models.
        If a field char is not in the models dictionary from models.py everything breaks
        :param path_to_field:
        :param cell_size:
        :return:
        """
        field = []
        with open(path_to_field, 'r', encoding="utf-8") as file:
            lines = file.readlines()
            for y, line in enumerate(lines):
                field_row = []
                for x, char in enumerate(line[:-1]):  # drop \n
                    if char == 'p':
                        self.player_x = x
                        self.player_y = y
                    model = Model(model_type=char, field_x=x, field_y=y)
                    if (char == 'p') or (char == 'b'):
                        model.movable = True
                    field_row.append(model)
                    field_row[-1].set_field(self)
                field.append(field_row)

        field = [[row[i] for row in field] for i in range(len(field[0]))]
        return field

    @staticmethod
    def generate_random_field(spawn_ratio: Dict[str, float], field_width_cells: int = 10,
                              field_height_cells: int = 8, walls_around: bool  = False) -> list:
        """
        Generates a random .field file. Chars and spawn ratio should be described in the spawn_ratio parameter
        :param spawn_ratio: dictionary with objects spawn ratio
        :param field_width_cells: desired width of the field
        :param field_height_cells: desired height of the field
        :param walls_around: if set to True all fields will have walls on the perimeter
        :return: None
        """
        if walls_around:
            if (field_width_cells <= 2 or field_height_cells <= 2):
                print(f"Can't generate {field_width_cells}x{field_height_cells} field")
                return []
            inner_filed = Field.generate_random_field(spawn_ratio, field_width_cells - 2, field_height_cells - 2)
            filed = [[wall_char for i in range(field_width_cells)]]
            for i in range(field_height_cells - 2):
                filed.append([wall_char] + inner_filed[i] + [wall_char])
            filed.append([wall_char for i in range(field_width_cells)])
            return filed
        else:
            object_dict = Field.__normalize_spawning_dict(spawn_ratio)
            spawning_intervals = {}  # Dict of intervals for random spawning generation
            cumulative_chance = 0
            for obj in object_dict:
                cumulative_chance += object_dict[obj]
                spawning_intervals[obj] = cumulative_chance

            field = []
            for i in range(field_height_cells):
                field_row = []
                for k in range(field_width_cells):
                    rand = random()
                    for char in spawning_intervals:
                        if rand < spawning_intervals[char]:
                            field_row.append(char)
                            break
                field.append(field_row)
            return field

    @staticmethod
    def __normalize_spawning_dict(object_dict: Dict[str, float]) -> Dict[str, float]:
        """
        Normalizes probabilities of each dictionary component
        :param object_dict: Dictionary with a cell char as key and probability of spawning as value
        :return: Dictionary with normalized values
        """
        total_probability = 0
        for obj in object_dict:
            total_probability += object_dict[obj]
        return {obj: object_dict[obj] / total_probability for obj in object_dict}

    @staticmethod
    def write_filed(path_to_field: str, field):
        """
        Writes given field to the .field file
        :param path_to_field: whole path with file name and extension .file
        :param field: list of list of characters
        :return:
        """
        with open(path_to_field, 'w') as file:
            for line in field:
                for char in line:
                    file.write(char)
                file.write('\n')
            file.close()


if __name__ == "__main__":
    spawn_ratio = {wall_char: 3, box_char: 1, foe_char: 1, empty_char: 10}
    Field.write_filed(field_name, Field.generate_random_field(spawn_ratio=spawn_ratio, walls_around=True))
