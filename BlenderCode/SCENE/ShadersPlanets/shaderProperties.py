import bpy
import logging
from typing import Optional, Dict, Any, List, Tuple
from .shaderPlanetFactory import PlanetShaderFactory

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ShaderProperties:
    SHADER_TYPES = [
        ('rocky_planet', "Rocky Planet", "Rocky planet surface shader"),
        ('gas_planet', "Gas Planet", "Gas giant atmosphere shader"),
        ('ice_planet', "Ice Planet", "Icy planet surface shader"),
        ('lava_planet', "Lava Planet", "Volcanic planet surface shader"),
        ('earth_like', "Earth-like", "Earth-like planet shader"),
        ('alien_planet', "Alien Planet", "Exotic alien planet shader")
    ]

    @staticmethod
    def update_shader(self, context):
        if context.active_object and context.active_object.active_material:
            mat = context.active_object.active_material
            if hasattr(mat, 'dynamic_shader'):
                PlanetShaderFactory.update_material_parameters(mat)

    @classmethod
    def register_properties(cls):
        props = {
            'shader_type': bpy.props.EnumProperty(
                name="Planet Type",
                items=cls.SHADER_TYPES,
                default='rocky_planet',
                update=cls.update_shader
            ),
            'noise_scale': bpy.props.FloatProperty(
                name="Surface Detail Scale",
                default=20.0,
                min=0.1,
                max=100.0,
                update=cls.update_shader
            ),
            'noise_detail': bpy.props.FloatProperty(
                name="Surface Detail Level",
                default=2.0,
                min=0.0,
                max=16.0,
                update=cls.update_shader
            ),
            'noise_roughness': bpy.props.FloatProperty(
                name="Surface Roughness",
                default=0.5,
                min=0.0,
                max=1.0,
                update=cls.update_shader
            ),
            'noise_distortion': bpy.props.FloatProperty(
                name="Surface Distortion",
                default=0.3,
                min=0.0,
                max=1.0,
                update=cls.update_shader
            ),
            'color_primary': bpy.props.FloatVectorProperty(
                name="Primary Color",
                subtype='COLOR',
                size=4,
                default=(0.8, 0.4, 0.1, 1.0),
                min=0.0,
                max=1.0,
                update=cls.update_shader
            ),
            'color_secondary': bpy.props.FloatVectorProperty(
                name="Secondary Color",
                subtype='COLOR',
                size=4,
                default=(0.2, 0.1, 0.05, 1.0),
                min=0.0,
                max=1.0,
                update=cls.update_shader
            ),
            'color_mix_factor': bpy.props.FloatProperty(
                name="Color Mix Factor",
                default=0.5,
                min=0.0,
                max=1.0,
                update=cls.update_shader
            ),
            'metallic': bpy.props.FloatProperty(
                name="Surface Metallic",
                default=0.0,
                min=0.0,
                max=1.0,
                update=cls.update_shader
            ),
            'roughness': bpy.props.FloatProperty(
                name="Surface Roughness",
                default=0.5,
                min=0.0,
                max=1.0,
                update=cls.update_shader
            ),
            'emission_strength': bpy.props.FloatProperty(
                name="Emission Strength",
                default=0.0,
                min=0.0,
                max=10.0,
                update=cls.update_shader
            ),
            'atmosphere_density': bpy.props.FloatProperty(
                name="Atmosphere Density",
                default=1.0,
                min=0.0,
                max=2.0,
                update=cls.update_shader
            ),
            'atmosphere_color': bpy.props.FloatVectorProperty(
                name="Atmosphere Color",
                subtype='COLOR',
                size=4,
                default=(0.5, 0.7, 1.0, 1.0),
                min=0.0,
                max=1.0,
                update=cls.update_shader
            ),
            'terrain_height': bpy.props.FloatProperty(
                name="Terrain Height",
                default=1.0,
                min=0.0,
                max=5.0,
                update=cls.update_shader
            ),
            'crater_density': bpy.props.FloatProperty(
                name="Crater Density",
                default=0.5,
                min=0.0,
                max=2.0,
                update=cls.update_shader
            ),
            'cloud_coverage': bpy.props.FloatProperty(
                name="Cloud Coverage",
                default=0.3,
                min=0.0,
                max=1.0,
                update=cls.update_shader
            ),
            'surface_temperature': bpy.props.FloatProperty(
                name="Surface Temperature",
                default=0.5,
                min=0.0,
                max=1.0,
                update=cls.update_shader
            ),
            'ring_system': bpy.props.BoolProperty(
                name="Enable Ring System",
                default=False,
                update=cls.update_shader
            )
        }

        for prop_name, prop in props.items():
            setattr(bpy.types.Scene, prop_name, prop)

    @classmethod
    def unregister_properties(cls):
        props = [
            'shader_type', 'noise_scale', 'noise_detail', 'noise_roughness',
            'noise_distortion', 'color_primary', 'color_secondary',
            'color_mix_factor', 'metallic', 'roughness', 'emission_strength',
            'atmosphere_density', 'atmosphere_color', 'terrain_height',
            'crater_density', 'cloud_coverage', 'surface_temperature',
            'ring_system'
        ]

        for prop in props:
            if hasattr(bpy.types.Scene, prop):
                delattr(bpy.types.Scene, prop)


def register():
    ShaderProperties.register_properties()


def unregister():
    ShaderProperties.unregister_properties()


if __name__ == "__main__":
    register()
