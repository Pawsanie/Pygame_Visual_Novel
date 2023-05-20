from ..User_Interface.UI_Button import button_generator
from ..Universal_computing import SingletonPattern
from ..User_Interface.UI_Menu_Text import menus_text_generator, MenuText
from ..User_Interface.UI_Button import Button
from ..Stage_Director import StageDirector
from ..Settings_Keeper import SettingsKeeper
"""
Contents code for user interface controller.
"""


class InterfaceController(SingletonPattern):
    """
    Generate user interface: buttons, menu and control it.
    InterfaceController used in "GamePlay_Administrator.py" for gameplay programming.
    Created in GameMaster class in Game_Master.py.
    """
    menu_settings: dict[str] = {
        'exit_menu': 'ui_setting_menu_buttons',
        'settings_menu': 'ui_exit_menu_buttons',
        'load_menu': 'ui_load_menu_buttons',
        'save_menu': 'ui_save_menu_buttons',
        'settings_status_menu': 'ui_settings_status_buttons',
        'start_menu': 'ui_start_menu_buttons',
        'back_to_start_menu_status_menu': 'ui_back_to_start_menu_status_menu_buttons',
        'creators_menu': 'ui_creators_menu_buttons'
    }

    def __init__(self):
        # Arguments processing:
        self.stage_director: StageDirector = StageDirector()
        self.settings_keeper: SettingsKeeper = SettingsKeeper()

        # Generate buttons:
        self.buttons_dict: dict = button_generator()
        self.gameplay_choice_buttons: dict = {}
        # Generate menus text:
        self.menus_text_dict: dict = menus_text_generator()

        # In game user interface:
        # "True/False" and "False" as default.
        self.gameplay_interface_hidden_status: bool = False
        self.gameplay_interface_status: bool = False
        # Menu interface:
        # "True/False" and "False" as default.
        self.game_menu_status: bool = False
        self.settings_menu_status: bool = False
        self.exit_menu_status: bool = False
        self.load_menu_status: bool = False
        self.save_menu_status: bool = False
        self.settings_status_menu_status: bool = False
        self.back_to_start_menu_status: bool = False
        self.creators_menu_status: bool = False
        # Start Menu:
        # "True/False" and "True" as default.
        self.start_menu_status: bool = True
        # Exit menu "from called" flag:
        # "True/False" and "start_menu_flag - True" as default.
        self.exit_from_start_menu_flag: bool = True
        self.exit_from_game_menu_flag: bool = False
        # Setting menu "from called" flag:
        # "True/False" and "start_menu_flag - True" as default.
        self.settings_from_start_menu_flag: bool = True
        self.settings_from_game_menu_flag: bool = False
        # Load menu "from called" flag:
        # "True/False" and "start_menu_flag - True" as default.
        self.load_from_start_menu_flag: bool = True
        self.load_from_game_menu_flag: bool = False
        # GamePlay type:
        # "True/False" and "False" as default.
        self.gameplay_type_reading: bool = False
        self.gameplay_type_choice: bool = False

        # Tag for menu background render:
        self.menu_name: str | None = None

    def get_ui_buttons_dict(self) -> dict[str, Button]:
        """
        Generate user interface buttons.

        :return: Dict with buttons names strings as values.
        """
        if self.gameplay_interface_status is True:
            self.menu_name: None = None
            if self.gameplay_type_reading is True:
                return self.buttons_dict['ui_gameplay_buttons']
            if self.gameplay_type_choice is True:
                return self.gameplay_choice_buttons
        if self.game_menu_status is True:
            self.menu_name: None = None
            return self.buttons_dict['ui_game_menu_buttons']

        if self.settings_menu_status is True:
            self.menu_name: str = "exit_menu"
            return self.buttons_dict['ui_setting_menu_buttons']
        if self.exit_menu_status is True:
            self.menu_name: str = "settings_menu"
            return self.buttons_dict['ui_exit_menu_buttons']
        if self.load_menu_status is True:
            self.menu_name: str = "load_menu"
            return self.buttons_dict['ui_load_menu_buttons']
        if self.save_menu_status is True:
            self.menu_name: str = "save_menu"
            return self.buttons_dict['ui_save_menu_buttons']
        if self.settings_status_menu_status is True:
            self.menu_name: str = "settings_status_menu"
            return self.buttons_dict['ui_settings_status_buttons']
        if self.start_menu_status is True:
            self.menu_name: str = "start_menu"
            return self.buttons_dict['ui_start_menu_buttons']
        if self.back_to_start_menu_status is True:
            self.menu_name: str = "back_to_start_menu_status_menu"
            return self.buttons_dict['ui_back_to_start_menu_status_menu_buttons']
        if self.creators_menu_status is True:
            self.menu_name: str = "creators_menu"
            return self.buttons_dict['ui_creators_menu_buttons']

    def get_menus_text_dict(self) -> dict[str, MenuText]:
        """
        Generate text for same menu.

        :return: Dict with menu text.
        """
        if self.exit_menu_status is True:
            return self.menus_text_dict['ui_exit_menu_text']
        if self.settings_status_menu_status is True:
            return self.menus_text_dict['ui_settings_status_text']
        if self.back_to_start_menu_status is True:
            return self.menus_text_dict['ui_back_to_start_menu_status_menu_text']
        if self.creators_menu_status is True:
            return self.menus_text_dict['ui_creators_menu_text']

    def scale(self):
        ui_buttons_dict: dict[str, Button] = self.get_ui_buttons_dict()
        for key in ui_buttons_dict:
            button: Button = ui_buttons_dict[key]
            button.scale()

    def button_clicked_status(self, event) -> tuple[str | None, bool]:
        """
        Check left click of mouse to button status.

        :param event: pygame.event from main_loop.
        :return: tuple[str | None, True | False]
        """
        if self.gameplay_interface_hidden_status is False:
            gameplay_ui_dict: dict = self.get_ui_buttons_dict()
            for button in gameplay_ui_dict:
                click_status = gameplay_ui_dict[button].button_clicked_status(event)
                if click_status is True:
                    return button, True
        return None, False

    def button_push_status(self) -> tuple[str | None, bool]:
        """
        Check left click of mouse to button status.

        :return: tuple[str | None, True | False]
        """
        if self.gameplay_interface_hidden_status is False:
            gameplay_ui_dict: dict[str, Button] = self.get_ui_buttons_dict()
            for button in gameplay_ui_dict:
                click_status = gameplay_ui_dict[button].button_click_hold()
                if click_status is True:
                    return button, True
        return None, False

    def button_cursor_position_status(self) -> bool:
        """
        Checking the cursor position above the button.

        :return: True | False
        """
        gameplay_ui_dict: dict = self.get_ui_buttons_dict()
        for button in gameplay_ui_dict:
            cursor_position_status = gameplay_ui_dict[button].button_cursor_position_status()
            if cursor_position_status is True:
                return True
            else:
                return False
