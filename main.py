import pygame
from classes.models import Model
from classes.Field import Field


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

PATH_TO_WALL = "images/wall.jpg"
PATH_TO_BOX = "images/rock.bmp"
PATH_TO_FOE = "images/definitely_an_imperial_trooper.png"
PATH_TO_EMPTY = "images/grass.png"
PATH_TO_PLAYER = "images/frames/ErWiNom_1x1.png"
PATH_TO_BACKGROUND = "images/background.png"
PATH_TO_FLOOR = "images/floor.png"


def prepare_field(path_to_field: str, cell_size: int) -> Field:
    field = Field(path_to_field=path_to_field, cell_size=cell_size)
    field.set_background(pygame.image.load(PATH_TO_BACKGROUND))

    floor_surface = pygame.image.load(PATH_TO_FLOOR)
    floor_x = field.width * field.cell_size
    floor_y = field.height * field.cell_size
    field.set_floor(floor_surface.subsurface((0, 0, floor_x, floor_y)))

    field.get_player().set_field(field)

    for i in range(field.width):
        for k in range(field.height):
            path_to_frame = ''
            if field[i][k].type == 'w':
                path_to_frame = str(PATH_TO_WALL)
            elif field[i][k].type == 'b':
                path_to_frame = str(PATH_TO_BOX)
            elif field[i][k].type == 'f':
                path_to_frame = str(PATH_TO_FOE)
            elif field[i][k].type == "p":
                path_to_frame = str(PATH_TO_PLAYER)
            if path_to_frame != '':
                field[i][k].add_frame(path_to_frame, "idle")
                field[i][k].set_current_frame("idle")

    # Centre field
    if field.width * cell_size < SCREEN_WIDTH and field.height * cell_size < SCREEN_HEIGHT:
        x_shift = (SCREEN_WIDTH - field.width * cell_size) // 2
        y_shift = (SCREEN_HEIGHT - field.height * cell_size) // 2
        field.set_shift(x_shift, y_shift)
    return field


def run_game_loop(display: pygame.Surface) -> None:
    """
    The main game loop
    :param display: game display from pygame.display.set_mode
    :return: None
    """
    clock = pygame.time.Clock()
    running = True

    path_to_field = "test_field.field"
    field = prepare_field(path_to_field=path_to_field, cell_size=CELL_SIZE)
    player: Model = field.get_player()
    display.blit(field.background, (0, 0))

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
        for i in range(field.width):
            for k in range(field.height):
                if field[i][k].type == ' ':
                    continue
                display.blit(field[i][k].frames["current"], field[i][k].get_screen_position())
        pygame.display.update()
        clock.tick(FPS)  # Setting FPS. Don't really know how it works but I can't find any docs in the web


if __name__ == "__main__":
    pygame.init()
    display = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    pygame.display.set_caption("TheGreatestGameEver")
    run_game_loop(display)
    pygame.quit()
