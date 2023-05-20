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
        # GamePlay type:
        # "True/False" and "False" as default.
        self.gameplay_type_reading: bool = False
        self.gameplay_type_choice: bool = False

        # Tag for menu background render:
        self.menu_name: str | None = None
        # Menu interface:
        self.menus_collection: dict | None = None
        self.game_menu_status: bool = False

    def get_ui_buttons_dict(self) -> dict[str, Button]:
        """
        Generate user interface buttons.

        :return: Dict with buttons names strings as values.
        """
        # In game user interface:
        if self.gameplay_interface_status is True:
            self.menu_name: None = None
            if self.gameplay_type_reading is True:
                return self.buttons_dict['ui_gameplay_buttons']
            if self.gameplay_type_choice is True:
                return self.gameplay_choice_buttons
        # Menu interface:
        for menu_key in self.menus_collection:
            menu: dict = self.menus_collection[menu_key]
            if menu['object'].status is True:
                self.menu_name: str | None = menu_key
                return self.buttons_dict[menu['tag']]

    def get_menus_text_dict(self) -> dict[str, MenuText]:
        """
        Generate text for same menu.

        :return: Dict with menu text.
        """
        for menu_key in self.menus_collection:
            menu: dict = self.menus_collection[menu_key]
            if menu['object'].status is True:
                if menu['text'] is not None:
                    return self.menus_text_dict[menu['text']]

    def scale(self):
        """
        Scale interface buttons.
        """
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
