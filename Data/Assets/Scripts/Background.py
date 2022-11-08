from pygame import display, image, transform, Surface

from .Assets_load import image_load, json_load
from .Render import background_sprite_data
"""
Contains code responsible for rendering scenes.
"""


class Background:
    """
    Load scene image by name and update the scene.
    Can scale scene size to display size.

    :param display_surface: Display surface object.
    :type display_surface: display.set_mode
    :param scene_image: Image for background.
    :type scene_image: pygame.image.load
    """
    def __init__(self, *, display_surface: display.set_mode, scene_image: image.load):
        """
        Set background image.
        Transform background to screen size.
        """
        self.display_surface: Surface = display_surface
        self.scene_image: Surface = scene_image
        self.scene_image_safe: Surface = scene_image  # hold standard image for rescale.
        self.background_coordinates = (0, 0)

    def scale(self):
        scene_image = self.scene_image_safe
        new_background_surface_size = background_sprite_data(display_surface=self.display_surface)
        self.scene_image = transform.scale(scene_image, new_background_surface_size[0])
        self.background_coordinates = new_background_surface_size[1]


def backgrounds_generator(*, display_surface: Surface) -> dict[str, Background]:
    """
    Generate dict with names of backgrounds and their sprites, for StageDirector.

    :param display_surface: pygame.Surface of pygame.display.set_mode.
    :return: Dict wth names of backgrounds and their sprites.
    """
    result = {}
    backgrounds_list: dict = json_load(['Scripts',
                                       'Json_data',
                                        'backgrounds_sprites'])
    for location in backgrounds_list:
        sprite: Surface = image_load(art_name=backgrounds_list[location],
                                     file_format='jpg',
                                     asset_type='Backgrounds')
        result.update({location: Background(display_surface=display_surface,
                                            scene_image=sprite)})
    return result

