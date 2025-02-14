import bpy
from typing import Any, Tuple
from bpy.types import NodeSocketColor, Node

class ShaderBase:
    VALID_SHADER_TYPES = {
        "principled", "glass", "emission", "nebula",
        "crystal", "holographic", "solar_fire",
        "inferno", "crystal_emission", "plasma",
        "rocky_planet", "gas_planet", "ice_planet",
        "lava_planet", "earth_like", "alien_planet"
    }

    DEFAULT_SHADER_PARAMS = {
        "principled": {
            "metallic": 0.5,
            "roughness": 0.5,
            "clearcoat": 0.0,
            "sheen": 0.0,
            "color_primary": (0.8, 0.8, 0.8, 1.0),
            "color_secondary": (0.5, 0.5, 0.5, 1.0)
        },
        "glass": {
            "ior": 1.45,
            "roughness": 0.0,
            "color_primary": (0.9, 0.9, 1.0, 1.0),
            "color_secondary": (0.8, 0.8, 0.9, 1.0)
        },
        "emission": {
            "emission_strength": 1.0,
            "color_primary": (1.0, 0.8, 0.2, 1.0),
            "color_secondary": (1.0, 0.4, 0.1, 1.0)
        }
    }

    @staticmethod
    def convert_to_tuple(color: Any) -> Tuple[float, float, float, float]:
        if isinstance(color, (tuple, list)):
            return tuple(color) if len(color) == 4 else tuple(color) + (1.0,)
        if isinstance(color, NodeSocketColor):
            return tuple(color.default_value)
        if hasattr(color, '__len__') and len(color) == 4:
            return tuple(float(c) for c in color)
        if hasattr(color, 'to_tuple'):
            return color.to_tuple()
        return (0.8, 0.8, 0.8, 1.0)

    @staticmethod
    def create_color_mix_node(nodes: Any, color_primary: Any, color_secondary: Any) -> Node:
        mix = nodes.new('ShaderNodeMixRGB')
        mix.inputs[0].default_value = 0.5
        mix.inputs[1].default_value = ShaderBase.convert_to_tuple(color_primary)
        mix.inputs[2].default_value = ShaderBase.convert_to_tuple(color_secondary)
        return mix

    @staticmethod
    def create_principled_shader(nodes: Any, node_links: Any, config) -> Node:
        shader = nodes.new("ShaderNodeBsdfPrincipled")
        mix_node = ShaderBase.create_color_mix_node(nodes, config.color_primary, config.color_secondary)
        node_links.new(mix_node.outputs[0], shader.inputs['Base Color'])
        shader.inputs['Metallic'].default_value = config.metallic
        shader.inputs['Roughness'].default_value = config.roughness
        return shader
