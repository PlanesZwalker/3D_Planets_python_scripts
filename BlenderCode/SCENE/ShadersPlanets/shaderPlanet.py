import os
import bpy
from ShadersPlanets.shaderPlanetFactory import PlanetShaderFactory
from ShadersPlanets.shaderConfigLoader import ShaderConfigLoader


class PlanetShaders:
    @staticmethod
    def create_shader_collection():
        """Create and return a collection of shaders."""
        config_path = os.path.join(os.path.dirname(__file__), 'shader_planet_config.json')
        configs = ShaderConfigLoader.load_config(config_path)
        return {
            name: PlanetShaderFactory.create_shader(
                config.name, config.noise_scale, config.noise_detail,
                config.color_primary, config.color_secondary,
                config.shader_type, config.description, config.emission_strength
            ) for name, config in configs.items()
        }

    @staticmethod
    def apply_shader(obj, shader_name):
        """Apply the selected shader to a specific object."""

        if not obj or not obj.data:
            print("ERROR: No valid object provided for shader application.")
            return

        config_path = os.path.join(os.path.dirname(__file__), 'shader_planet_config.json')
        configs = ShaderConfigLoader.load_config(config_path)

        # Ensure shader exists
        if shader_name not in configs:
            print(f"WARNING: Shader '{shader_name}' not found in config. Using default.")
            shader_name = "Ultra_Gas_Giant"  # Fallback shader

        shader_config = configs[shader_name]  # Get shader settings

        # Ensure the object has material slots
        obj.data.materials.clear()  # Remove existing materials
        material = PlanetShaderFactory.create_shader(
            shader_config.name, shader_config.noise_scale,
            shader_config.noise_detail, shader_config.color_primary,
            shader_config.color_secondary, shader_config.shader_type,
            shader_config.description, shader_config.emission_strength
        )

        obj.data.materials.append(material)  # Assign new shader

        print(f"Shader '{shader_name}' applied to {obj.name} successfully.")


def update_shader_property(self, context):
    """Called when the planet_shader property is updated."""
    print(f"Shader updated to: {self.planet_shader}")
    PlanetShaders.apply_shader(context)


def register():
    """Register properties and types with Blender."""
    # Load the shader configuration
    config_path = os.path.join(os.path.dirname(__file__), 'shader_planet_config.json')
    configs = ShaderConfigLoader.load_config(config_path)

    # Extract shader names for the EnumProperty items
    shader_types = list(configs.keys()) or ['Ultra_Gas_Giant']

    # Register the EnumProperty to select the shader type in the Scene
    bpy.types.Scene.planet_shader = bpy.props.EnumProperty(
        items=[(name, name, "") for name in shader_types],
        name="Planet Shader",
        description="Select the type of planet shader",
        default=shader_types[0],
        update=update_shader_property  # Apply the shader when selection changes
    )

    # Register other shader-related properties
    bpy.types.Object.noise_scale = bpy.props.FloatProperty(
        name="Noise Scale",
        default=10.0,
        description="Adjust the scale of the noise used for planet texture"
    )
    bpy.types.Object.noise_detail = bpy.props.FloatProperty(
        name="Noise Detail",
        default=15.0,
        description="Adjust the detail of the noise used for planet texture"
    )
    bpy.types.Object.color_primary = bpy.props.FloatVectorProperty(
        name="Primary Color",
        subtype='COLOR',
        size=4,
        default=(0.8, 0.8, 1.0, 1.0),
        description="Set the primary color of the planet"
    )
    bpy.types.Object.color_secondary = bpy.props.FloatVectorProperty(
        name="Secondary Color",
        subtype='COLOR',
        size=4,
        default=(0.2, 0.2, 0.3, 1.0),
        description="Set the secondary color of the planet"
    )


def unregister():
    """Unregister properties and types from Blender."""
    del bpy.types.Scene.planet_shader  # Unregister planet_shader from Scene
    del bpy.types.Object.noise_scale
    del bpy.types.Object.noise_detail
    del bpy.types.Object.color_primary
    del bpy.types.Object.color_secondary


if __name__ == "__main__":
    register()
