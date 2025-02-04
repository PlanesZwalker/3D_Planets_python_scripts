import bpy


class ShaderProperties:

    @staticmethod
    def draw_shader_params(layout, scene, planet_config):
        """Dynamically generate shader parameters based on the selected shader type."""
        shader_type = planet_config.shader_type

        # Get corresponding method for the selected shader type
        shader_type_methods = {
            'PRINCIPLED': ShaderProperties.draw_principled_shader_params,
            'GLASS': ShaderProperties.draw_glass_shader_params,
            'EMISSION': ShaderProperties.draw_emission_shader_params
        }

        # Call the corresponding shader parameter method
        if shader_type in shader_type_methods:
            shader_type_methods[shader_type](layout, scene, planet_config)
        else:
            layout.label(text="No specific parameters for this shader type.")

    @staticmethod
    def draw_shader_common_params(layout, scene):
        """Draw common shader parameters."""
        layout.prop(scene, "noise_scale", text="Noise Scale")
        layout.prop(scene, "noise_detail", text="Noise Detail")
        layout.prop(scene, "color_primary", text="Primary Color")
        layout.prop(scene, "color_secondary", text="Secondary Color")

    @staticmethod
    def draw_principled_shader_params(layout, scene, planet_config):
        """Draw UI elements for the Principled shader."""
        layout.label(text="Principled Shader Settings:")
        ShaderProperties.draw_shader_common_params(layout, scene)

        # Example: Add properties from the planet_config, like metallic, roughness
        layout.prop(scene, "metallic", text="Metallic")
        layout.prop(scene, "roughness", text="Roughness")

    @staticmethod
    def draw_glass_shader_params(layout, scene, planet_config):
        """Draw UI elements for the Glass shader."""
        layout.label(text="Glass Shader Settings:")
        ShaderProperties.draw_shader_common_params(layout, scene)

        # Glass-specific properties
        layout.prop(scene, "glass_refraction", text="Refraction Index")

    @staticmethod
    def draw_emission_shader_params(layout, scene, planet_config):
        """Draw UI elements for the Emission shader."""
        layout.label(text="Emission Shader Settings:")
        ShaderProperties.draw_shader_common_params(layout, scene)

        # Emission-specific properties
        layout.prop(scene, "emission_strength", text="Emission Strength")


# Register properties to be used in the scene
def register():
    bpy.types.Scene.noise_scale = bpy.props.FloatProperty(
        name="Noise Scale",
        default=10.0,
        min=0.1,
        max=100.0
    )

    bpy.types.Scene.noise_detail = bpy.props.FloatProperty(
        name="Noise Detail",
        default=15.0,
        min=1.0,
        max=30.0
    )

    bpy.types.Scene.color_primary = bpy.props.FloatVectorProperty(
        name="Primary Color",
        subtype='COLOR',
        size=4,
        default=(0.1, 0.3, 0.7, 1),  # RGBA default
        min=0.0,
        max=1.0
    )

    bpy.types.Scene.color_secondary = bpy.props.FloatVectorProperty(
        name="Secondary Color",
        subtype='COLOR',
        size=4,
        default=(0.3, 0.6, 0.8, 1),  # RGBA default
        min=0.0,
        max=1.0
    )

    bpy.types.Scene.metallic = bpy.props.FloatProperty(
        name="Metallic",
        default=0.5,
        min=0.0,
        max=1.0
    )

    bpy.types.Scene.roughness = bpy.props.FloatProperty(
        name="Roughness",
        default=0.5,
        min=0.0,
        max=1.0
    )

    bpy.types.Scene.glass_refraction = bpy.props.FloatProperty(
        name="Glass Refraction",
        default=1.5,
        min=1.0,
        max=2.0
    )

    bpy.types.Scene.emission_strength = bpy.props.FloatProperty(
        name="Emission Strength",
        default=1.0,
        min=0.0,
        max=10.0
    )


def unregister():
    del bpy.types.Scene.noise_scale
    del bpy.types.Scene.noise_detail
    del bpy.types.Scene.color_primary
    del bpy.types.Scene.color_secondary
    del bpy.types.Scene.metallic
    del bpy.types.Scene.roughness
    del bpy.types.Scene.glass_refraction
    del bpy.types.Scene.emission_strength


if __name__ == "__main__":
    register()
