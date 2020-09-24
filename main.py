import pygame
from classes.models import Player
from classes.Field import Field
from PIL import Image


SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
CELL_SIZE = 40
FPS = 30
WHITE_RGB = (255, 255, 255)
BLACK_RGB = (0, 0, 0)
ESCAPE_KEY = 27
D_KEY = 100
A_KEY = 97
W_KEY = 119
S_KEY = 115
UP_KEY = 273
DOWN_KEY = 274
RIGHT_KEY = 275
LEFT_KEY = 276
PLAYER_STEP = 40


def draw_grid(surface: pygame.Surface, surface_width: int, surface_height: int, cell_size: int) -> None:
    """
    Draws grid to make positioning easier
    :param surface: game display
    :param surface_width: max x coordinate size of the display - width (px)
    :param surface_height: max y coordinate size of the display - height (px)
    :param cell_size: size of a cell on the grid (px)
    :return: None
    """
    for i in range(surface_width // cell_size):
        pygame.draw.line(surface, BLACK_RGB, (i * cell_size, 0), (i * cell_size, surface_height))
    for k in range(surface_height // cell_size):
        pygame.draw.line(surface, BLACK_RGB, (0, k * cell_size), (surface_width, k * cell_size))


def get_player():
    player = Player(field_x=3, field_y=1)
    return player


def prepare_field(path_to_field: str, cell_size: int) -> Field:
    field = Field(path_to_field=path_to_field, cell_size=cell_size)
    path_to_background = "images/background.png"
    field.set_background(pygame.image.load(path_to_background))
    path_to_floor = "images/floor.png"
    floor = Image.open(path_to_floor)
    floor_x = field.width * field.cell_size
    floor_y = field.height * field.cell_size
    floor = floor.resize((floor_x, floor_y))
    path_to_new_floor = f"images/floor{floor_x}x{floor_y}.png"
    floor.save(path_to_new_floor)
    field.set_floor(pygame.image.load(path_to_new_floor))
    player = get_player()
    field.add_player(player, 3, 1)
    player.set_field(field)

    # Centre field
    if field.width * cell_size < SCREEN_WIDTH and field.height * cell_size < SCREEN_HEIGHT:
        x_shift = (SCREEN_WIDTH - field.width * cell_size) // 2
        y_shift = (SCREEN_HEIGHT - field.height * cell_size) // 2
        field.shift_field(x_shift, y_shift)
    return field


def run_game_loop(display: pygame.Surface) -> None:
    """
    The main game loop
    :param display: game display from pygame.display.set_mode
    :return: None
    """
    # Setup game loop
    clock = pygame.time.Clock()
    running = True

    path_to_field = "test_field.field"
    field = prepare_field(path_to_field=path_to_field, cell_size=CELL_SIZE)
    player = field.get_player()
    display.blit(field.background, (0, 0))
    # draw_grid(display, SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == ESCAPE_KEY:
                    running = False
                """
                Movement control
                """
                if (event.key == W_KEY) or (event.key == UP_KEY):  # Move up key
                    player.move("up")
                elif (event.key == D_KEY) or (event.key == RIGHT_KEY):  # Move right key
                    player.move("right")
                elif (event.key == S_KEY) or (event.key == DOWN_KEY):  # Move down key
                    player.move("down")
                elif (event.key == A_KEY) or (event.key == LEFT_KEY):  # Move right key
                    player.move("left")

        display.blit(field.floor, (0 + field.shift_x, 0 + field.shift_y))
        for i in range(field.height):
            for k in range(field.width):
                if field[i][k] is None:
                    continue
                display.blit(field[i][k].frames["current"], field[i][k].get_screen_position())
        pygame.display.update()
        clock.tick(FPS)  # Setting FPS. Don't really know how it works but I can't find any docs in the web


if __name__ == "__main__":
    # Setup display
    pygame.init()
    display = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    pygame.display.set_caption("TheGreatestGameEver")
    run_game_loop(display)
    pygame.quit()
    quit(0)
