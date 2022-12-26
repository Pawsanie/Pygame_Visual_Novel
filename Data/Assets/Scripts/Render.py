from pygame import display, Surface
"""
Contains code for display image render.
"""


def render(func):
    """
    Decorator with the main render process.
    """
    def base_render(*args, **kwargs):
        self = args[0]  # class method`s 'self.' for in class decorator.
        # Clear old screen for not 16x9 display render:
        self.screen_clear()
        # Function render:
        func(*args, **kwargs)
        # Flip all surfaces:
        display.update()
    return base_render


class Render:
    """
    Render image on display.
    """
    def __init__(self, *, screen: Surface, interface_controller, stage_director):
        """
        :param screen: Display surface for image render.
        :type screen: pygame.Surface
        :param interface_controller: InterfaceController for access to user interface.
        :type interface_controller: InterfaceController
        :param stage_director: StageDirector for access to scenes data.
        :type stage_director: StageDirector
        """
        self.screen: Surface = screen
        self.stage_director = stage_director
        self.interface_controller = interface_controller

    def screen_clear(self):
        """
        Clear scene before scene render.
        """
        self.screen.fill((0, 0, 0))

    def gameplay_text_render(self):
        # Get data from StageDirector:
        background: Surface = self.stage_director.get_background()[0]
        text_canvas: tuple[Surface, tuple[int, int]] = self.stage_director.text_canvas.get()  # Remake
        speaker: tuple[Surface, tuple[int, int]] = self.stage_director.speaker
        speech: tuple[Surface, tuple[int, int]] = self.stage_director.speech
        # Render:
        if self.interface_controller.gameplay_interface_hidden_status is False:
            text_canvas[0].blit(speaker[0], speaker[1])
            text_canvas[0].blit(speech[0], speech[1])
            background.blit(text_canvas[0], text_canvas[1])

    def ui_buttons_render(self):
        """
        User interface render.
        """
        # Get data from StageDirector and InterfaceController:
        background: Surface = self.stage_director.get_background()[0]
        get_ui_buttons_dict = self.interface_controller.get_ui_buttons_dict()
        # Render:
        if self.interface_controller.gameplay_interface_status is True:
            if self.interface_controller.gameplay_interface_hidden_status is False:
                for button_key in get_ui_buttons_dict:
                    button = get_ui_buttons_dict[button_key]
                    button_surface, button_coordinates = button.generator()
                    background.blit(button_surface, button_coordinates)
        else:
            for button_key in get_ui_buttons_dict:
                button = get_ui_buttons_dict[button_key]
                button_surface, button_coordinates = button.generator()
                self.screen.blit(button_surface, button_coordinates)

    def characters_render(self):
        """
        Scene characters render.
        """
        # Get data from StageDirector:
        background = self.stage_director.get_background()[0]
        characters_dict = self.stage_director.characters_dict
        # Render:
        for character in characters_dict.values():
            background.blit(character.surface,
                            character.coordinates_pixels)

    def background_render(self):
        """
        Background render.
        """
        # Get data from StageDirector:
        get_background_data: tuple[Surface, tuple[int, int]] = self.stage_director.get_background()
        background, background_coordinates = get_background_data
        # Render:
        self.screen.blit(background, background_coordinates)

    def standard_menu_render(self, background_name):
        # Background render:
        self.stage_director.set_scene(location=background_name)
        self.background_render()
        # Exit menu ui render:
        self.ui_buttons_render()

    @render
    def gameplay_read_scene(self):
        """
        Render reading scene.
        """
        # Characters render:
        self.characters_render()
        # Text render:
        self.gameplay_text_render()
        # Gameplay ui render:
        self.ui_buttons_render()
        # Background render:
        self.background_render()

    @render
    def game_menu(self):
        """
        Render game menu scene.
        """
        # Mask settings:
        screen_mask: Surface = Surface([self.screen.get_width(), self.screen.get_height()])
        screen_mask.fill((0, 0, 0))
        screen_mask.set_alpha(210)
        # Characters render:
        self.characters_render()
        # Background render:
        self.background_render()
        # Menu mask render:
        self.screen.blit(screen_mask, (0, 0))
        # Game menu ui render:
        self.ui_buttons_render()

    @render
    def exit_menu(self):
        self.standard_menu_render('exit_menu')

    @render
    def settings_menu(self):
        self.standard_menu_render('settings_menu')

    @render
    def load_menu(self):
        self.standard_menu_render('load_menu')

    @render
    def save_menu(self):
        self.standard_menu_render('save_menu')

    @render
    def settings_status_menu(self):
        self.standard_menu_render('settings_status_menu')

    @render
    def start_menu(self):
        self.standard_menu_render('start_menu')

    def image_render(self):
        """
        Display image render.
        """
        if self.interface_controller.gameplay_interface_status is True:
            self.gameplay_read_scene()
        if self.interface_controller.game_menu_status is True:
            self.game_menu()
        if self.interface_controller.settings_menu_status is True:
            self.settings_menu()
        if self.interface_controller.exit_menu_status is True:
            self.exit_menu()
        if self.interface_controller.load_menu_status is True:
            self.load_menu()
        if self.interface_controller.save_menu_status is True:
            self.save_menu()
        if self.interface_controller.settings_status_menu_status is True:
            self.settings_status_menu()
        if self.interface_controller.start_menu_status is True:
            self.start_menu()
