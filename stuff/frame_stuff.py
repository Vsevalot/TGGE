from PIL import Image
from pathlib import Path
from typing import Tuple


def crop_frames(path_to_frames: str, frames_in_row: int, frames_in_column: int,
                path_to_save: str = '', extension: str = "png", frame_size: Tuple[int, int] = (-1, -1)) -> bool:
    """
    Crop single frames file to individual frames
    :param path_to_frames: path to frames file
    :param frames_in_row: number of frames per row, used to calculate crop borders
    :param frames_in_column: number of frames per column, used to calculate crop borders
    :param path_to_save: OPTIONAL. Path to the save folder.
    If not specified, folder "frames" created at the location of the frames file.
    :param extension: OPTIONAL. Extension of the cropped frames. Default value is png
    :param frame_size: OPTIONAL. Forces to resize each frame to the given size
    :return: True if everything is fine False otherwise
    """
    frames_path = Path(path_to_frames)
    if not frames_path.exists():
        print(f"Error: {frames_path} does not exist!")
        return False
    if not frames_path.is_file():
        print(f"Error: {frames_path} must be a file!")
        return False
    frames = Image.open(frames_path)
    frame_sheet_size = frames.size
    frame_width = frame_sheet_size[0] // frames_in_row
    frame_height = frame_sheet_size[1] // frames_in_column

    folder_to_save = Path(path_to_save)
    if not folder_to_save.exists():
        print(f"Error: {folder_to_save} does not exist!")
        return False
    if not folder_to_save.is_dir():
        print(f"Error: path to save must be a folder!\nGiven: {folder_to_save}")
        return False
    if path_to_save == '':
        folder_to_save = frames_path.parent.joinpath("frames")
        if not folder_to_save.exists():
            folder_to_save.mkdir()

    if frames_in_row < 1 or frames_in_column < 1:
        print("Number of frames per row and frames per column must be greater than 0!")
        return False

    for i in range(frames_in_row):
        for k in range(frames_in_column):
            crop_coordinates = (i * frame_width, k * frame_height, (i + 1) * frame_width, (k + 1) * frame_height)
            frame = frames.crop(crop_coordinates)
            if frame_size != (-1, -1):  # If frame size were given
                frame = frame.resize(frame_size)
            frame.save(f"{folder_to_save}/{frames_path.stem}_{i + 1}x{k + 1}.{extension}")
    return True


if __name__ == "__main__":
    path_to_frames = "C:/Users/sevamunger/PycharmProjects/TGGE/images/ErWiNom.png"
    frames_per_row = 4
    frames_per_column = 4
    crop_frames(path_to_frames, frames_per_row, frames_per_column, frame_size=(40, 40))
