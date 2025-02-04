import sys

try:
    import bpy
except ImportError:
    print("Error: 'bpy' module not found. Make sure you are running this script inside Blender.")
    sys.exit(1)

# Import custom modules
from ShadersPlanets.shaderConfigLoader import ShaderConfigLoader


# Define Shader Operators (Fixes 'unknown operator' issue)
class OBJECT_OT_UpdateShader(bpy.types.Operator):
    bl_idname = "object.update_shader"
    bl_label = "Update Shader"
    bl_description = "Applies the selected planet shader"

    def execute(self, context):
        print("Applying shader...")
        # Implement your shader application logic here
        return {'FINISHED'}


class OBJECT_OT_ResetShader(bpy.types.Operator):
    bl_idname = "object.reset_shader"
    bl_label = "Reset Shader"
    bl_description = "Resets shader settings to default"

    def execute(self, context):
        print("Resetting shader settings...")
        # Implement shader reset logic here
        return {'FINISHED'}


# UI Panel
class ShaderPanel(bpy.types.Panel):
    bl_label = "Planet Shader Creator"
    bl_idname = "VIEW3D_PT_shader_creator"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Create'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Ensure properties exist to avoid errors
        required_props = ["planet_name", "color_primary", "color_secondary", "noise_scale", "noise_detail"]
        for prop in required_props:
            if not hasattr(scene, prop):
                layout.label(text=f"Error: Missing property '{prop}'", icon='ERROR')
                return

        # Material Preview
        box = layout.box()
        box.label(text="Material Preview", icon='MATERIAL')
        row = box.row()
        row.template_ID_preview(context.active_object, "active_material", new="material.new")

        # Planet Type Selection
        box = layout.box()
        box.label(text="Planet Type", icon='WORLD_DATA')
        box.prop(scene, "planet_name", text="")

        # Load Shader Configurations
        try:
            shader_configs = ShaderConfigLoader.load_config()
        except Exception as e:
            layout.label(text=f"Error loading shader config: {e}", icon='ERROR')
            return

        planet_name = scene.planet_name

        if planet_name in shader_configs:
            planet_config = shader_configs[planet_name]

            # Noise Parameters
            noise_box = layout.box()
            noise_box.label(text="Noise Settings", icon='TEXTURE')
            col = noise_box.column(align=True)
            col.prop(scene, "noise_scale", slider=True)
            col.prop(scene, "noise_detail", slider=True)
            col.prop(scene, "noise_roughness", slider=True)
            col.prop(scene, "noise_distortion", slider=True)

            # Color Settings
            color_box = layout.box()
            color_box.label(text="Color Settings", icon='COLOR')
            col = color_box.column(align=True)
            col.prop(scene, "color_primary", text="Primary")
            col.prop(scene, "color_secondary", text="Secondary")
            col.prop(scene, "color_mix_factor", slider=True)

            # Surface Properties
            surface_box = layout.box()
            surface_box.label(text="Surface Properties", icon='SURFACE_DATA')
            col = surface_box.column(align=True)
            col.prop(scene, "roughness", slider=True)
            col.prop(scene, "metallic", slider=True)
            col.prop(scene, "emission_strength", slider=True)

        # Action Buttons
        row = layout.row(align=True)
        row.operator("object.update_shader", text="Apply", icon='CHECKMARK')
        row.operator("object.reset_shader", text="Reset", icon='LOOP_BACK')


# Register Properties
def register():
    bpy.utils.register_class(ShaderPanel)
    bpy.utils.register_class(OBJECT_OT_UpdateShader)
    bpy.utils.register_class(OBJECT_OT_ResetShader)

    bpy.types.Scene.planet_name = bpy.props.StringProperty(
        name="Planet Name",
        default="Ultra_Gas_Giant",
        description="Name of the selected planet type"
    )

    bpy.types.Scene.noise_scale = bpy.props.FloatProperty(
        name="Noise Scale",
        default=1.0,
        min=0.0,
        max=10.0
    )
    bpy.types.Scene.noise_detail = bpy.props.FloatProperty(
        name="Noise Detail",
        default=2.0,
        min=0.0,
        max=10.0
    )
    bpy.types.Scene.noise_roughness = bpy.props.FloatProperty(
        name="Roughness",
        default=0.5,
        min=0.0,
        max=1.0
    )
    bpy.types.Scene.noise_distortion = bpy.props.FloatProperty(
        name="Distortion",
        default=0.0,
        min=0.0,
        max=1.0
    )
    bpy.types.Scene.color_primary = bpy.props.FloatVectorProperty(
        name="Primary Color",
        subtype='COLOR',
        default=(1.0, 1.0, 1.0),
        min=0.0,
        max=1.0
    )
    bpy.types.Scene.color_secondary = bpy.props.FloatVectorProperty(
        name="Secondary Color",
        subtype='COLOR',
        default=(0.0, 0.0, 0.0),
        min=0.0,
        max=1.0
    )
    bpy.types.Scene.color_mix_factor = bpy.props.FloatProperty(
        name="Color Mix",
        default=0.5,
        min=0.0,
        max=1.0
    )
    bpy.types.Scene.roughness = bpy.props.FloatProperty(
        name="Surface Roughness",
        default=0.5,
        min=0.0,
        max=1.0
    )
    bpy.types.Scene.metallic = bpy.props.FloatProperty(
        name="Metallic",
        default=0.0,
        min=0.0,
        max=1.0
    )
    bpy.types.Scene.emission_strength = bpy.props.FloatProperty(
        name="Emission",
        default=0.0,
        min=0.0,
        max=10.0
    )

    print("Shader Panel and properties successfully registered!")


# Unregister Properties
def unregister():
    bpy.utils.unregister_class(ShaderPanel)
    bpy.utils.unregister_class(OBJECT_OT_UpdateShader)
    bpy.utils.unregister_class(OBJECT_OT_ResetShader)

    del bpy.types.Scene.planet_name
    del bpy.types.Scene.noise_scale
    del bpy.types.Scene.noise_detail
    del bpy.types.Scene.noise_roughness
    del bpy.types.Scene.noise_distortion
    del bpy.types.Scene.color_primary
    del bpy.types.Scene.color_secondary
    del bpy.types.Scene.color_mix_factor
    del bpy.types.Scene.roughness
    del bpy.types.Scene.metallic
    del bpy.types.Scene.emission_strength

    print("Shader Panel and properties successfully unregistered!")


# Main Function
def main():
    register()


if __name__ == "__main__":
    main()
