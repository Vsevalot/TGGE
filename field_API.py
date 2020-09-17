from random import random
from typing import Dict

field_name = "test_field.field"

wall_chance = 0.05
box_chance = 0.01
foe_chance = 0.02

wall_char = 'w'
box_char = 'b'
foe_char = 'f'
empty_char = ' '


def normalize_dict(object_dict: Dict[str, float]) -> Dict[str, float]:
    total_probability = 0
    for obj in object_dict:
        total_probability += object_dict[obj]

    if total_probability > 1:
        return {obj: object_dict[obj] / total_probability for obj in object_dict}
    else:
        if ' ' not in object_dict:
            object_dict[' '] = 1 - total_probability
    return object_dict


def generate_field(field_name: str, field_width_cells: int = 40,
                   field_height_cells: int = 30, object_chances = None):

    # object_dict = {}
    # if object_chances is None:
    #     object_dict[' '] = 1.0
    # else:
    #     object_dict = normalize_dict(object_chances)
    #
    # spawn_borders = {}
    # object_list = list(object_dict.keys())
    # for i in range(len(object_list)):
    #     spawn_borders[object_list[i]] = sum([object_dict[object_list[o]] for o in range(i)])

    with open(field_name, 'w', encoding="utf-8") as file:
        empty_chance = 1 - wall_chance - box_chance - foe_chance
        for i in range(field_height_cells):
            for k in range(field_width_cells):
                rand = random()
                if rand < empty_chance:
                    file.write(empty_char)
                elif rand < empty_chance + wall_chance:
                    file.write(wall_char)
                elif rand < empty_chance + wall_chance + box_chance:
                    file.write(box_char)
                else:
                    file.write(foe_char)
            file.write('\n')
        file.close()

def read_field(path_to_field: str):
    char_field = []
    with open(field_name, 'w', encoding="utf-8") as file:
        lines = file.readlines()
        char_field = []


if __name__ == "__main__":
    field_name = "test_field.field"
    generate_field(field_name, object_chances={wall_char: wall_chance, box_char: box_chance, foe_char: foe_chance})