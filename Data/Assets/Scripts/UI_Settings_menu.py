# from pygame import KEYDOWN

from .Settings_Keeper import SettingsKeeper
from .UI_Base_menu import BaseMenu
"""
Contains settings menu code.
"""


class SettingsMenu(BaseMenu):
    """
    Controls reactions to user input commands from mouse or key bord in Settings Menu.

    :param interface_controller: InterfaceController exemplar.
                                 Responsible for user interface status and buttons.
    :type interface_controller: InterfaceController
    :param scene_validator: SceneValidator exemplar.
                        Responsible for scene order and scene construction.
    :type scene_validator: SceneValidator
    :param settings_keeper: Settings controller class.
    :type settings_keeper: SettingsKeeper
    """
    def __init__(self, *, interface_controller, settings_keeper, scene_validator):
        """
        :param interface_controller: InterfaceController exemplar.
                                     Responsible for user interface status and buttons.
        :type interface_controller: InterfaceController
        :param scene_validator: SceneValidator exemplar.
                            Responsible for scene order and scene construction.
        :type scene_validator: SceneValidator
        :param settings_keeper: Settings controller class.
        :type settings_keeper: SettingsKeeper
        """
        super(SettingsMenu, self).__init__(
            interface_controller=interface_controller,
            scene_validator=scene_validator)
        self.settings_keeper: SettingsKeeper = settings_keeper

    def settings_menu_ui_mouse(self):
        """
        Interface interaction in in-game exit menu.
        From GAME menu!
        """
        gameplay_ui_buttons: tuple[str, bool] = self.interface_controller.button_clicked_status()
        # Clicking a button with a mouse:
        if gameplay_ui_buttons[1] is True:
            command = gameplay_ui_buttons[0]
            if command == 'settings_menu_video':
                ...
            if command == 'settings_menu_audio':
                ...
            if command == 'settings_menu_localization':
                ...
            if command == 'settings_menu_back':
                if self.interface_controller.settings_from_start_menu_flag is True:
                    self.interface_controller.settings_menu_status = False
                    self.interface_controller.start_menu_status = True
                if self.interface_controller.settings_from_game_menu_flag is True:
                    self.interface_controller.settings_menu_status = False
                    self.interface_controller.game_menu_status = True

    def key_bord_setting_menu_ui_key_down(self, event):
        """
        :param event: pygame.event from main_loop.
        """
        ...
        # if event.type == KEYDOWN:
        #     if event.key == ...:

    def setting_menu_input(self, event):
        """
        Setting menu conveyor:
        :param event: pygame.event from main_loop.
        """
        self.settings_menu_ui_mouse()
        self.key_bord_setting_menu_ui_key_down(event)
        self.input_wait_ready()
