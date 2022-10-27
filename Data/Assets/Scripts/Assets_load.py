from os import path
import json

from pygame import image, font, mixer
"""
Contains code responsible for assets load.
"""
# ./Assets/. root path:
asset_root_path = f"{path.abspath(__file__).replace(path.join(*['Scripts', 'Assets_load.py']), '')}"


def image_load(*, art_name: str, file_format: str, asset_type: str) -> image.load:
    """
    Load image by name.
    :param asset_type: String: 'Characters' or 'Scenes'.
    :param art_name: must be string with file name in '*/Images/*' folder.
    :param file_format: Image file format: 'png' or 'jpg'.
    :return: Loaded image.
    """
    art_path = f"{asset_root_path}{path.join(*['Images', asset_type, art_name])}"
    scene_image_path = f"{art_path}.{file_format}"

    if file_format == 'png':
        return image.load(scene_image_path).convert_alpha()
    if file_format == 'jpg':
        return image.load(scene_image_path).convert()


def sound_load(*, asset_type: str, file_name: str) -> mixer.music.load:
    """
    Load sound by name.
    :param asset_type: String: 'Effects' or 'Music'.
    :param file_name: must be string with file name in '*/Sounds/*' folder.
    :return: Loaded sound.
    """
    sound_path = f"{asset_root_path}{path.join(*['Sounds', asset_type, file_name])}"
    return mixer.music.load(sound_path)


def font_load(*, font_name: str, font_size: int) -> font.Font:
    """
    Load font by name.
    :param font_name: Must be string with file name in '*/Fonts/*' folder.
    :param font_size: Must be int type.
    :return: Loaded font.
    """
    font_path = f"{asset_root_path}{path.join(*['Fonts', font_name])}"
    font_to_load = font.Font(font_path, font_size)
    return font_to_load


def json_load(path_list: list[str]) -> json.loads:
    """
    :param path_list: list with strings of folders names and file name.
    :return: Json dict.
    """
    scene_options_path = f"{asset_root_path}{path.join(*path_list)}.{'json'}"
    with open(scene_options_path, 'r', encoding='utf-8') as json_file:
        json_data = json_file.read()
        return json.loads(json_data)
