import json
import os
import logging
from dataclasses import dataclass, fields
from typing import Dict, Any, Optional, Tuple
import bpy

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ShaderConfig:
    name: str
    shader_type: str = "principled"
    noise_scale: float = 10.0
    noise_detail: float = 15.0
    noise_roughness: float = 0.5
    noise_distortion: float = 0.0
    color_mix_factor: float = 0.5
    color_primary: Tuple[float, float, float, float] = (0.8, 0.8, 0.8, 1.0)
    color_secondary: Tuple[float, float, float, float] = (0.5, 0.5, 0.5, 1.0)
    roughness: float = 0.5
    metallic: float = 0.5
    emission_strength: float = 1.0
    subsurface: float = 0.0
    clearcoat: float = 0.0
    sheen: float = 0.0
    description: str = "Default shader configuration"

    def to_property_group(self, property_group: bpy.types.PropertyGroup):
        for field in fields(self):
            if hasattr(property_group, field.name):
                setattr(property_group, field.name, getattr(self, field.name))

class DynamicShaderProperties(bpy.types.PropertyGroup):
    noise_scale: bpy.props.FloatProperty(
        name="Noise Scale",
        default=10.0,
        min=0.0,
        max=100.0
    )
    noise_detail: bpy.props.FloatProperty(
        name="Noise Detail",
        default=15.0,
        min=0.0,
        max=50.0
    )
    noise_roughness: bpy.props.FloatProperty(
        name="Noise Roughness",
        default=0.5,
        min=0.0,
        max=1.0
    )
    metallic: bpy.props.FloatProperty(
        name="Metallic",
        default=0.5,
        min=0.0,
        max=1.0
    )
    roughness: bpy.props.FloatProperty(
        name="Roughness",
        default=0.5,
        min=0.0,
        max=1.0
    )
    color_primary: bpy.props.FloatVectorProperty(
        name="Primary Color",
        subtype='COLOR',
        size=4,
        default=(0.1, 0.3, 0.7, 1.0),
        min=0.0,
        max=1.0
    )
    color_secondary: bpy.props.FloatVectorProperty(
        name="Secondary Color",
        subtype='COLOR',
        size=4,
        default=(0.3, 0.6, 0.8, 1.0),
        min=0.0,
        max=1.0
    )

class ShaderConfigLoader:
    DEFAULT_CONFIG = {
        'noise_scale': 10.0,
        'noise_detail': 15.0,
        'noise_roughness': 0.5,
        'noise_distortion': 0.0,
        'color_mix_factor': 0.5,
        'color_primary': [0.1, 0.3, 0.7, 1.0],
        'color_secondary': [0.3, 0.6, 0.8, 1.0],
        'roughness': 0.5,
        'metallic': 0.5,
        'emission_strength': 1.0,
        'shader_type': 'principled',
        'subsurface': 0.0,
        'clearcoat': 0.0,
        'sheen': 0.0,
        'description': 'Default configuration'
    }

    @classmethod
    def load_config(cls, config_path: Optional[str] = None) -> Dict[str, ShaderConfig]:
        try:
            if config_path is None:
                config_path = os.path.join(os.path.dirname(__file__), 'shader_planet_config.json')

            with open(config_path, 'r') as file:
                configs = json.load(file)

            shader_configs = {}
            for name, config in configs.items():
                full_config = cls.DEFAULT_CONFIG.copy()
                full_config.update(config)
                full_config['name'] = name
                shader_configs[name] = ShaderConfig(**full_config)

            return shader_configs

        except FileNotFoundError:
            logger.warning(f"Configuration file not found: {config_path}")
            return {'default': ShaderConfig(**cls.DEFAULT_CONFIG)}
        except json.JSONDecodeError:
            logger.warning(f"Invalid JSON in configuration file: {config_path}")
            return {'default': ShaderConfig(**cls.DEFAULT_CONFIG)}
        except Exception as e:
            logger.warning(f"Error loading configuration: {e}")
            return {'default': ShaderConfig(**cls.DEFAULT_CONFIG)}

    @classmethod
    def register_properties(cls):
        bpy.utils.register_class(DynamicShaderProperties)
        bpy.types.Material.dynamic_shader = bpy.props.PointerProperty(type=DynamicShaderProperties)

    @classmethod
    def unregister_properties(cls):
        bpy.utils.unregister_class(DynamicShaderProperties)
        del bpy.types.Material.dynamic_shader
