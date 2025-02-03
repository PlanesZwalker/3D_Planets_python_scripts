import os
import sys

import bpy

# Add parent directory to Python path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from ShadersPlanets.planetShaderFactory import PlanetShaderFactory
from ShadersPlanets.shaderConfigLoader import ShaderConfigLoader


class PlanetShaders:
    @staticmethod
    def create_shader_collection():
        config_path = os.path.join(os.path.dirname(__file__), 'planet_shader_config.json')
        configs = ShaderConfigLoader.load_config(config_path)
        return {name: PlanetShaderFactory.create_shader(
            config.name, config.noise_scale, config.noise_detail, config.color_primary, config.color_secondary,
            config.shader_type
        ) for name, config in configs.items()}

    @staticmethod
    def apply_shader(obj):
        config_path = os.path.join(os.path.dirname(__file__), 'planet_shader_config.json')
        configs = ShaderConfigLoader.load_config(config_path)
        shader_name = obj.get("planet_shader", "Ultra_Gas_Giant")
        if shader_name in configs:
            obj.data.materials.clear()
            obj.data.materials.append(PlanetShaderFactory.create_shader(
                configs[shader_name].name, configs[shader_name].noise_scale, configs[shader_name].noise_detail,
                configs[shader_name].color_primary, configs[shader_name].color_secondary,
                configs[shader_name].shader_type
            ))


def register():
    configs = ShaderConfigLoader.load_config()
    shader_types = list(configs.keys()) or ['Ultra_Gas_Giant']
    bpy.types.Object.planet_shader = bpy.props.EnumProperty(
        items=[(name, name, "") for name in shader_types],
        name="Planet Type",
        description="Select planet shader type",
        default=shader_types[0]
    )


def unregister():
    del bpy.types.Object.planet_shader


if __name__ == "__main__":
    register()
