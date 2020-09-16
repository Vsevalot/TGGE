import pygame
from random import randint
from classes import models


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
PLAYER_STEP = 40


def draw_grid(surface: pygame.Surface, surface_x: int, surface_y: int, cell_size: int) -> None:
    """
    Draws grid to make positioning easier
    :param surface: game display
    :param surface_x: x coordinate size of the display (px)
    :param surface_y: y coordinate size of the display (px)
    :param cell_size: size of a cell on the grid (px)
    :return: None
    """
    for i in range(surface_x // cell_size):
        pygame.draw.line(surface, BLACK_RGB, (i * cell_size, 0), (i * cell_size, surface_y))
    for k in range(surface_y // cell_size):
        pygame.draw.line(surface, BLACK_RGB, (0, k * cell_size), (surface_x, k * cell_size))


if __name__ == "__main__":
    """
    INITIALIZING  
    """
    pygame.init()
    display: pygame.Surface = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    pygame.display.set_caption("TheGreatestGameEver")
    clock = pygame.time.Clock()
    clock.tick(FPS)  # setting FPS
    running = True


    path_to_player_img = "images/definitely_an_imperial_trooper.png"
    player = models.model(path_to_player_img, x=1, y=1)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == ESCAPE_KEY:
                    running = False

                if event.key == W_KEY:  # Move up key
                    if player.y > 1:
                        player.y -= PLAYER_STEP
                elif event.key == D_KEY:  # Move right key
                    pass
                elif event.key == S_KEY:  # Move down key
                    if player.y < SCREEN_HEIGHT - PLAYER_STEP:
                        player.y += PLAYER_STEP
                elif event.key == A_KEY:  # Move left key
                    pass

            display.fill(WHITE_RGB)
            draw_grid(display, SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE)
            display.blit(player.img, player.get_coordinates())
            pygame.display.update()  # This line redraw the scene / object same as pygame.display.flip()
            print(f"DEBUG --- {event}")

    pygame.quit()
    quit(0)