import pygame
from typing import List
from random import randint
from classes.models import Model, Player
import os


SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
CELL_SIZE = 40
FPS = 60
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


def redraw_game_window(display: pygame.Surface, objects_to_draw: List[Model]):
    display.fill(WHITE_RGB)
    draw_grid(display, SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE)
    for model in objects_to_draw:
        display.blit(model.frames["current"], model.get_coordinates())  # Draw a surface
    pygame.display.update()  # This line redraw the scene / object. Same as pygame.display.flip()


def prepare_models() -> List[Model]:
    path_to_player_img = "images/definitely_an_imperial_trooper.png"
    player = Player(path_to_player_img, x=1, y=81)
    path_to_player_frames = "images/player_frames"
    player_frames = [os.path.join(path_to_player_frames, f) for f in os.listdir(path_to_player_frames)]
    for path_to_frame in player_frames:
        frame_name = os.path.basename(path_to_frame).split('.')[0]
        if not player.add_frame(path_to_frame, frame_name):
            print(f"{frame_name} cannot be added!")

    path_to_rock = "images/rock.bmp"
    rock = Model(path_to_rock, 1, 201)
    rock.type = "rock"

    path_to_wall = "images/wall.bmp"
    wall = Model(path_to_wall, 1, 41)
    wall.type = "wall"
    wall.movable = False

    walls = [Model(path_to_wall, 40 * randint(1, 10) + 1, 40 * randint(1, 10) + 1) for i in range(10)]
    walls = [w for w in walls if w.get_coordinates() not in [m.get_coordinates for m in walls]]  # remove dublicate
    
    return [player, rock, wall] + walls


def run_game_loop(display: pygame.Surface) -> None:
    """
    The main game loop
    :param display: game display from pygame.display.set_mode
    :return: None
    """
    # Setup game loop
    clock = pygame.time.Clock()
    running = True
    
    models = prepare_models()
    player: Player = [m for m in models if m.type == "player"][0]  # It's ok, pycharm goes little crazy about subclasses
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == ESCAPE_KEY:
                    running = False

                """
                Movement control
                """
                if (event.key == W_KEY) or (event.key == UP_KEY):  # Move up key
                    if player.y > 1:
                        player.set_y_coordinate(player.y - PLAYER_STEP)
                        player.set_current_frame("UP")
                        player.idle_time = 0
                        for m in models:  # Checking for collisions
                            if m is not player:
                                if player.get_coordinates() == m.get_coordinates():
                                    player.set_y_coordinate(player.y + PLAYER_STEP)
                                    if m.is_movable():
                                        if m.y > 1:
                                            m.set_y_coordinate(m.y - PLAYER_STEP)
                elif (event.key == D_KEY) or (event.key == RIGHT_KEY):  # Move right key
                    pass
                elif (event.key == S_KEY) or (event.key == DOWN_KEY):  # Move down key
                    if player.y < SCREEN_HEIGHT - PLAYER_STEP:
                        player.set_y_coordinate(player.y + PLAYER_STEP)
                        player.set_current_frame("DOWN")
                        player.idle_time = 0
                        for m in models:  # Checking for collisions
                            if m is not player:
                                if player.get_coordinates() == m.get_coordinates():
                                    player.set_y_coordinate(player.y - PLAYER_STEP)
                                    if m.is_movable():
                                        if m.y < SCREEN_HEIGHT - PLAYER_STEP:
                                            m.set_y_coordinate(m.y + PLAYER_STEP)

                elif (event.key == A_KEY) or (event.key == LEFT_KEY):  # Move left key
                    pass
            print(f"DEBUG --- {event}")

        player.idle_time += 1
        if player.idle_time > player.idle_delay:
            if player.get_current_frame() != "IDLE":
                player.set_current_frame("IDLE")
        redraw_game_window(display, models)

        clock.tick(FPS)  # Setting FPS. Don't really know how it works but I can't find any docs in the web


if __name__ == "__main__":
    # Setup display
    pygame.init()
    display = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    pygame.display.set_caption("TheGreatestGameEver")
    run_game_loop(display)
    pygame.quit()
    quit(0)