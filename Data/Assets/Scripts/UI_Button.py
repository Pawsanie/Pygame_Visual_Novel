from os import path

from pygame import Surface, SRCALPHA, transform, mouse

from .Assets_load import image_load, json_load
from .Render import surface_size, button_size
"""
Contents code for user interface buttons.
"""


class Button:
    """
    Generate interface button surface and coordinates for render.

    :param background_surface: pygame.Surface of background.
    :type background_surface: Surface
    :param button_name: String with button image file name.
    :type button_name: str
    :param button_text: String with text of button.
    :type button_text: str | None
    :param button_image_data: Nested dictionary with button name as key and dictionary with button type,
                              index order position and sprite name as values.
    :type button_image_data: dict[str, dict[str, int]]
    :param language_flag: String with language flag.
    :type language_flag: str
    :param button_text_localization_dict: Dictionary with language flags as keys and localization text as values.
    :type button_text_localization_dict: dict[str]
    """
    def __init__(self, *, background_surface: Surface, button_name: str,
                 button_text: str | None, button_image_data: dict[str, int],
                 language_flag: str, button_text_localization_dict: dict[str]):
        """
        :param background_surface: pygame.Surface of background.
        :type background_surface: Surface
        :param button_name: String with button image file name.
        :type button_name: str
        :param button_text: String with text of button.
        :type button_text: str | None
        :param button_image_data: Nested dictionary with button name as key and dictionary with button type,
                                  index order position and sprite name as values.
        :type button_image_data: dict[str, dict[str, int]]
        :param language_flag: String with language flag.
        :type language_flag: str
        :param button_text_localization_dict: Dictionary with language flags as keys and localization text as values.
        :type button_text_localization_dict: dict[str]
        """
        self.background_surface: Surface = background_surface
        self.button_name: str = button_name
        self.button_text: str | None = button_text
        self.language_flag = language_flag
        self.button_text_localization_dict = button_text_localization_dict
        self.localization_button_text(language_flag=self.language_flag)
        self.button_image_data: dict[str, int] = button_image_data

        # Generate button image:
        self.button_sprite_standard: Surface = image_load(
            art_name=str(self.button_image_data['sprite_name']),
            file_format='png',
            asset_type=path.join(*['UI', 'Buttons']))
        self.button_sprite: Surface = self.button_sprite_standard

        # Generate button surface:
        self.button_size: tuple[int, int] = button_size(
            place_flag=button_image_data['type'],
            background_surface=self.background_surface)
        self.button_surface: Surface = Surface(self.button_size, SRCALPHA)

        # Generate button coordinates:
        self.button_coordinates: tuple[int, int] = (0, 0)
        self.coordinates(background_surface=self.background_surface)

        # Button image render:
        self.button_sprite = transform.scale(self.button_sprite, self.button_size)
        self.button_surface.blit(self.button_sprite, (0, 0))

    def generator(self):
        """
        Generate button surface and coordinates for render.
        """
        return self.button_surface, self.button_coordinates

    def scale(self, *, background_surface):
        """
        Scale button surface, with background context.

        :param background_surface: pygame.Surface of background.
        :type background_surface: Surface.
        """
        # Arg parse:
        self.background_surface = background_surface

        # Button size scale:
        self.button_sprite: Surface = self.button_sprite_standard
        self.button_size: tuple[int, int] = button_size(
            place_flag=self.button_image_data['type'],
            background_surface=self.background_surface)
        self.button_sprite = transform.scale(self.button_sprite, self.button_size)
        self.button_surface: Surface = transform.scale(self.button_surface, self.button_size)

        # Scale coordinates:
        self.coordinates(background_surface=self.background_surface)

        # Default button render:
        if self.button_cursor_position_status() is False:
            self.button_surface.blit(self.button_sprite, (0, 0))

        # Button ready to be pressed:
        else:
            # self.button_surface.blit(self.button_sprite, (0, 0))
            self.button_surface.fill((0, 0, 0))  # <---------------- Remake after tests

    def reflect(self):
        """
        Reflect button sprite surface.
        Reflect methode must be after scale methode in prerender loop.
        """
        self.button_surface: Surface = transform.flip(
            self.button_surface,
            flip_x=True,
            flip_y=False)

    def coordinates(self, *, background_surface: Surface):
        """
        Generate coordinates.

        :param background_surface: pygame.Surface of background.
        :type background_surface: Surface.
        """
        self.background_surface: Surface = background_surface
        place_flag: dict[str, int] = self.button_image_data
        button_coordinates_x, button_coordinates_y = (0, 0)
        background_surface_size: list[int, int] = surface_size(interested_surface=self.background_surface)
        background_surface_size_x_middle: int = background_surface_size[0]//2
        background_surface_size_y_middle: int = background_surface_size[1]//2

        if place_flag['type'] == 'gameplay_ui':
            # X:
            button_coordinates_x: int = \
                (background_surface_size_x_middle - (self.button_size[0]//2)) + \
                (self.button_size[0] * place_flag['index_number'])
            # Y:
            button_coordinates_y: int = background_surface_size[1] - self.button_size[1]

        if place_flag['type'] == 'game_menu':
            # X:
            # Y:
            ...

        if place_flag['type'] == 'start_menu':
            # X:
            # Y:
            ...

        if place_flag['type'] == 'save_menu':
            # X:
            # Y:
            ...

        if place_flag['type'] == 'load_menu':
            # X:
            # Y:
            ...

        if place_flag['type'] == 'exit_menu':
            # X:
            # Y:
            ...

        if place_flag['type'] == 'settings_menu':
            # X:
            # Y:
            ...

        self.button_coordinates: tuple[int, int] = (button_coordinates_x, button_coordinates_y)

    def localization_button_text(self, *, language_flag):
        """
        Generate text on button if it's necessary.

        :param language_flag: String with language flag.
        :type language_flag: str
        """
        if self.button_text is not None:
            self.language_flag: str = language_flag
            self.button_text: str = self.button_text_localization_dict[self.language_flag]

    def button_cursor_position_status(self) -> bool:
        """
        Checking the cursor position above the button.

        :return: True | False
        """
        # Mouse processing:
        cursor_position: tuple[int, int] = mouse.get_pos()
        # Button processing:
        button_x_size, button_y_size = surface_size(self.button_surface)
        button_coordinates_x, button_coordinates_y = self.button_coordinates
        # Drawing a button while hovering over:
        if button_coordinates_x < cursor_position[0] < button_coordinates_x + button_x_size and \
                button_coordinates_y < cursor_position[1] < button_coordinates_y + button_y_size:
            return True
        # Default Button Rendering:
        else:
            return False

    def button_clicked_status(self) -> bool:
        """
        Check left click of mouse to button status.

        :return: True | False
        """
        if self.button_cursor_position_status() is True:
            button_clicked: tuple[bool, bool, bool] = mouse.get_pressed()
            if button_clicked[0] is True:
                return True


def button_generator(language_flag: str, background_surface: Surface) -> dict[str, dict[str, Button]]:
    """
    Generate dict with buttons for user interface.

    :return: A nested dictionary of buttons group and an instance of the Button class.
    """
    result, ui_buttons_json = {}, {}
    # localizations instructions from 'ui_localizations_data.json': UI files and languages for UI.
    localizations_data: dict = json_load(['Scripts', 'Json_data', 'UI', 'Localization', 'ui_localizations_data'])
    # localizations data:
    ui_buttons_files: tuple[str] = (localizations_data['ui_buttons_files'])
    localizations: tuple[str] = (localizations_data['localizations'])

    # All buttons text localizations:
    all_buttons_text_localizations_dict: dict = {}
    for language in localizations:
        all_buttons_text_localizations_dict.update(
            {language: json_load(['Scripts', 'Json_data', 'UI', 'Localization', language])})

    # User Interface buttons:
    for file_name in ui_buttons_files:
        ui_buttons_json: dict = json_load(['Scripts', 'Json_data', 'UI', file_name])
        ui_buttons: dict = {}
        for key in ui_buttons_json:

            # Generate text localizations for button:
            button_text_localization: dict = {}
            button_text: str | None = None
            try:
                for language in all_buttons_text_localizations_dict:
                    button_text_localization.update({language: all_buttons_text_localizations_dict[language][key]})
                button_text = all_buttons_text_localizations_dict[language_flag][key]
            except KeyError:
                button_text = None

            # Generate button:
            ui_buttons.update(
                {key: Button(
                    background_surface=background_surface,
                    button_name=key,
                    button_text=button_text,
                    button_image_data=ui_buttons_json[key],
                    language_flag=language_flag,
                    button_text_localization_dict=button_text_localization
                )})

        result.update({file_name: ui_buttons})
    return result
