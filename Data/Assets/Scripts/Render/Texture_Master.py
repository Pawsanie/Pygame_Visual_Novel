from pygame import Surface, SRCALPHA, transform

from ..Universal_computing.Pattern_Singleton import SingletonPattern
from ..Universal_computing.Assets_load import AssetLoader
"""
Contains code responsible for collecting and storing textures.
"""


class TexturesMaster(SingletonPattern):
    """
    Storing textures data for image calculation.
    """
    def __init__(self):
        # Program layers settings:
        self._asset_loader: AssetLoader = AssetLoader()

        # TexturesMaster attributes:
        self._texture_sources: dict = {
            "Characters": "characters_sprites",
            "Backgrounds": "backgrounds_sprites"
        }
        self._texture_configs_catalog: dict = {}
        self._raw_images_catalog: dict = {}
        self._raw_textures_catalog: dict = {}
        self._texture_catalog: dict = {}
        self._image_memory_pool_bytes: int = 262144000  # 250mb as default

        # TexturesMaster settings:
        self.__initialisation()

    def get_texture_configs_data(self, *, texture_name: str, texture_type: str) -> dict:
        """
        Get texture configuration data.
        Use in Sprites.
        :param texture_name: Name of texture which data you want to get.
        :type texture_name: str
        :param texture_type: Type of texture which data you want to get.
        :type texture_type: str
        :return: Texture data dictionary.
        """
        return self._texture_configs_catalog[texture_type][texture_name]

    def __initialisation(self):
        """
        Collect raw texture data and create sprite sheets.
        """
        self._collect_texture_configurations()
        self._collect_raw_images()
        self._create_raw_sprite_sheet_frames()
        self._raw_images_catalog.clear()
        self._create_void_background()

        self._create_texture_catalog()

    def _create_void_background(self):
        void_surface: Surface = Surface((720, 480))
        void_surface.fill((0, 0, 0))
        self._raw_textures_catalog["Backgrounds"].update(
            {
                None: {
                    "frames": {
                        None: void_surface
                    }
                }
            }
        )

    def _create_texture_catalog(self):
        # TODO: optimisation_scale
        self._texture_catalog: dict = self._raw_textures_catalog.copy()

    def get_texture(self, *, texture_type: str, texture_name: str,
                    animation: str | None = None, frame: int | str) -> Surface:
        """
        Get texture Surface from TexturesMaster storage.
        :param texture_type: Characters|Backgrounds
        :type texture_type: str
        :param texture_name: Name of texture.
        :type texture_name: str
        :param animation: Animation name of sprite sheet. For statick images is None as default.
        :type animation: str | None
        :param frame: Animation frame number, or frame name for statick images.
        :type frame: int | str
        :return: Texture frame Surface
        """
        if animation is not None:
            return self._texture_catalog[texture_type][texture_name][animation][str(frame)]
        else:
            return self._texture_catalog[texture_type][texture_name][str(frame)]

    def _collect_texture_configurations(self):
        """
        Get texture configurations for Sprites creation.
        """
        for texture_source_folder, game_play_texture_config_file in self._texture_sources.items():
            if texture_source_folder not in self._texture_configs_catalog:
                self._texture_configs_catalog.update(
                    {
                        texture_source_folder: {}
                    }
                )

            # Get texture configs names:
            sprite_configs_names_collection: list = []
            sprites_raw_data: dict = self._asset_loader.json_load(
                [
                    "Scripts", "Json_data", game_play_texture_config_file,
                ]
            )

            for sprite_type_name_key, sprite_data_value in sprites_raw_data.items():
                sprite_config_name: str = sprite_data_value["texture"]
                if sprite_config_name not in sprite_configs_names_collection:
                    sprite_configs_names_collection.append(sprite_config_name)

            # Get texture configs data:
            for config_name in sprite_configs_names_collection:
                config_data: dict = self._asset_loader.json_load(
                    [
                        "Scripts", "Json_data", "Texture_data", texture_source_folder, config_name
                    ]
                )
                self._texture_configs_catalog[texture_source_folder].update(
                    {
                        config_name: config_data
                    }
                )

    def _collect_raw_images(self):
        """
        Collect row texture images for scale.
        """
        for texture_type, texture_collection in self._texture_configs_catalog.items():
            if texture_type not in self._raw_images_catalog:
                self._raw_images_catalog.update(
                    {
                        texture_type: {}
                    }
                )

            for texture_name in texture_collection:
                texture_image: Surface = self._asset_loader.image_load(
                    art_name=texture_name,
                    asset_type=texture_type,
                )
                self._raw_images_catalog[texture_type].update(
                    {
                        texture_name: texture_image
                    }
                )

    def _create_raw_sprite_sheet_frames(self):
        """
        Create raw sprite sheet.
        Frames of this sprite sheet are not scale from raw state.
        They will be scale when loading a game map or video clip into a separate collection.
        """
        def __get_frames(*, texture_type_name: str, frames: dict) -> dict:
            """
            Get sprite sheet frame from texture image.
            :param texture_type_name: Asset type for raw image getting.
            :type texture_type_name: str
            :param frames: Dictionary with frame coordinates data.
            :type frames: dict
            """
            result: dict = {}
            for frame in frames:
                top_left_corner: dict = frames[frame]["top_left_corner"]
                bottom_right_corner: dict = frames[frame]["bottom_right_corner"]

                bounding_box: tuple[int, int] = (
                    bottom_right_corner["x"] - top_left_corner["x"],
                    bottom_right_corner["y"] - top_left_corner["y"]
                )

                frame_surface: Surface = Surface(
                    bounding_box,
                    SRCALPHA
                )

                frame_blit_coordinates: tuple[int, int] = (
                    - top_left_corner["x"],
                    - top_left_corner["y"]
                )

                texture: Surface = self._raw_images_catalog[texture_type_name][texture_name]
                frame_surface.blit(
                    texture, frame_blit_coordinates
                )

                result.update(
                    {
                        frame: frame_surface
                    }
                )
            return result

        # Create sprites:
        for texture_type, texture_catalog in self._texture_configs_catalog.items():
            if texture_type not in self._raw_textures_catalog:
                self._raw_textures_catalog.update(
                    {
                        texture_type: {}
                    }
                )

            for texture_name, texture_data in texture_catalog.items():
                self._raw_textures_catalog[texture_type].update(
                    {
                        texture_name: {}
                    }
                )

                # Animation sprites:
                if texture_data["sprite_sheet"]:
                    for animation in texture_data["animations"]:
                        self._raw_textures_catalog[texture_type][texture_name].update(
                            {
                                animation: __get_frames(
                                    texture_type_name=texture_type,
                                    frames=texture_data["animations"][animation]["frames"]
                                )
                            }
                        )

                # Statick sprites:
                else:
                    self._raw_textures_catalog[texture_type][texture_name].update(
                        {
                            "frames": __get_frames(
                                texture_type_name=texture_type,
                                frames=texture_data["statick_frames"]
                            )
                        }
                    )

    def set_new_scale_frame(self, *, texture_name: str, texture_type: str, frame: int,
                            image_size: tuple[int, int], animation_name: str = "statick_frames"):
        """
        Cash new frame size.
        :param texture_name: Name of texture image frame.
        :type texture_type: str
        :param texture_type: Type of texture image.
        :type texture_type: str
        :param frame: Number of frame or statick frame name.
        :type frame: int | str
        :param image_size: Frame image surface.
        :type image_size: tuple[int, int]
        :param animation_name: Name of animation for non statick textures.
        :type animation_name: str
        """
        image_surface: Surface = transform.scale(
            self._texture_catalog[
                texture_type
            ][
                texture_name
            ][
                animation_name
            ][
                str(frame)
            ],
            image_size
        )

        self._texture_catalog[
            texture_type
        ][
            texture_name
        ][
            animation_name
        ][
            str(frame)
        ]: Surface = image_surface

    def get_texture_size(self, *, texture_name: str, texture_type: str,
                         frame: int, animation_name: str = "statick_frames") -> tuple[int, int]:
        """
        Get texture size from catalog.
        :param texture_name: Name of texture image frame.
        :type texture_type: str
        :param texture_type: Type of texture image.
        :type texture_type: str
        :param frame: Number of frame or statick frame name.
        :type frame: int | str
        :param animation_name: Name of animation for non statick textures.
        :type animation_name: str
        """
        return self._texture_catalog[texture_type][texture_name][animation_name][str(frame)].get_width(), \
            self._texture_catalog[texture_type][texture_name][animation_name][str(frame)].get_height()
