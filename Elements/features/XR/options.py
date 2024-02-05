import xr
import enum

# required for openXR
class Form_factor(enum.Enum):
    #  configuration on the device
    HMD="Hmd"
    HANDHELD="Handheld"

class View_Configuration(enum.Enum):
    # required for VR: 2 views
    STEREO="Stereo"
    MONO="Mono"

class Blend_Mode(enum.Enum):
    # Default Draw mode
    OPAQUE="Opaque" # for VR
    ADDITIVE="Additive" # for AR
    ALPHABLEND="AlphaBlend" # for AR


class options:
    def __init__(self,graphics_plugin="OpenGL",form_factor="Hmd",View_config="Stereo",blend_mode="Opaque",space="Local"):
        "Initialize default options"
        self.graphics_plugin = graphics_plugin
        self.form_factor = form_factor
        self.view_configuration = View_config
        self.environment_blend_mode = blend_mode
        self.app_space = space
        self.parsed = {
            "form_factor": self.get_xr_form_factor(form_factor),
            "view_config_type": self.get_xr_view_configuration_type(View_config),
            "environment_blend_mode": self.get_xr_environment_blend_mode(blend_mode)
        }

    @property
    def background_clear_color(self) -> tuple:
        slate_grey = (0.184313729, 0.309803933, 0.309803933, 1.0)
        if self.parsed["environment_blend_mode"] == xr.EnvironmentBlendMode.OPAQUE:
            return slate_grey  # SlateGrey
        elif self.parsed["environment_blend_mode"] == xr.EnvironmentBlendMode.ADDITIVE:
            return 0, 0, 0, 1  # Black
        elif self.parsed["environment_blend_mode"] == xr.EnvironmentBlendMode.ALPHA_BLEND:
            return 0, 0, 0, 0  # TransparentBlack
        else:
            return slate_grey

    @staticmethod
    def get_xr_environment_blend_mode(environment_blend_mode_string: str) -> xr.EnvironmentBlendMode:
        return {
            "Opaque": xr.EnvironmentBlendMode.OPAQUE,
            "Additive": xr.EnvironmentBlendMode.ADDITIVE,
            "AlphaBlend": xr.EnvironmentBlendMode.ALPHA_BLEND,
        }[environment_blend_mode_string]

    @staticmethod
    def get_xr_environment_blend_mode_string(environment_blend_mode: xr.EnvironmentBlendMode) -> str:
        return {
            xr.EnvironmentBlendMode.OPAQUE: "Opaque",
            xr.EnvironmentBlendMode.ADDITIVE: "Additive",
            xr.EnvironmentBlendMode.ALPHA_BLEND: "AlphaBlend",
        }[environment_blend_mode]

    @staticmethod
    def get_xr_form_factor(form_factor_string: str) -> xr.FormFactor:
        if form_factor_string == "Hmd":
            return xr.FormFactor.HEAD_MOUNTED_DISPLAY
        elif form_factor_string == "Handheld":
            return xr.FormFactor.HANDHELD_DISPLAY
        raise ValueError(f"Unknown form factor '{form_factor_string}'")

    @staticmethod
    def get_xr_view_configuration_type(view_configuration_string: str) -> xr.ViewConfigurationType:
        if view_configuration_string == "Mono":
            return xr.ViewConfigurationType.PRIMARY_MONO
        elif view_configuration_string == "Stereo":
            return xr.ViewConfigurationType.PRIMARY_STEREO
        raise ValueError(f"Unknown view configuration '{view_configuration_string}'")
    
    def set_environment_blend_mode(self, environment_blend_mode: xr.EnvironmentBlendMode) -> None:
        self.environment_blend_mode = self.get_xr_environment_blend_mode_string(environment_blend_mode)
        self.parsed["environment_blend_mode"] = environment_blend_mode