import bpy

from .shaderConfigLoader import ShaderConfigLoader
from .shaderPlanetFactory import PlanetShaderFactory


class PlanetShaders:
    configs = ShaderConfigLoader.load_config()  # Load config once as a class-level variable

    @staticmethod
    def update_shader_settings(context):
        """Update material settings when a new shader is selected."""
        obj = context.active_object
        if not obj or not obj.active_material:
            return  # No object or material selected

        material = obj.active_material
        shader_name = context.scene.selected_planet_name

        if shader_name in PlanetShaders.configs:
            shader = PlanetShaders.configs[shader_name]

            # Update the material properties instead of just scene settings
            material["noise_scale"] = shader.noise_scale
            material["noise_detail"] = shader.noise_detail
            material["noise_roughness"] = shader.noise_roughness
            material["noise_distortion"] = shader.noise_distortion
            material["color_primary"] = shader.color_primary
            material["color_secondary"] = shader.color_secondary
            material["color_mix_factor"] = 0.5  # Default mixing factor

            # Rename the material to match the selected shader
            material.name = shader_name

    @staticmethod
    def create_shader_collection():
        """Create and return a collection of shaders."""
        return {
            name: PlanetShaderFactory.create_shader(config) for name, config in PlanetShaders.configs.items()
        }

    @staticmethod
    def apply_shader(obj, shader_name):
        """Apply the selected shader to a specific object."""
        if not obj or not obj.data:
            bpy.context.scene["shader_log"] = "ERROR: No valid object provided for shader application."
            return

        # Ensure shader exists
        if shader_name not in PlanetShaders.configs:
            bpy.context.scene["shader_log"] = f"WARNING: Shader '{shader_name}' not found in config. Using default."
            shader_name = "Ultra_Gas_Giant"  # Fallback shader

        shader_config = PlanetShaders.configs[shader_name]  # Get shader settings

        # Ensure the object has material slots
        obj.data.materials.clear()  # Remove existing materials
        material = PlanetShaderFactory.create_shader(shader_config)

        obj.data.materials.append(material)  # Assign new shader

        bpy.context.scene["shader_log"] = f"Shader '{shader_name}' applied to {obj.name} successfully."


def update_shader_property(self, context):
    """Called when the planet_shader property is updated."""
    PlanetShaders.apply_shader(context.active_object, self.planet_shader)


def register():
    """Register properties and types with Blender."""
    # Extract shader names for the EnumProperty items
    shader_types = list(PlanetShaders.configs.keys()) or ['Ultra_Gas_Giant']

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
    if hasattr(bpy.types.Scene, 'planet_shader'):
        del bpy.types.Scene.planet_shader
    if hasattr(bpy.types.Object, 'noise_scale'):
        del bpy.types.Object.noise_scale
    if hasattr(bpy.types.Object, 'noise_detail'):
        del bpy.types.Object.noise_detail
    if hasattr(bpy.types.Object, 'color_primary'):
        del bpy.types.Object.color_primary
    if hasattr(bpy.types.Object, 'color_secondary'):
        del bpy.types.Object.color_secondary


def main():
    register()


if __name__ == "__main__":
    main()
