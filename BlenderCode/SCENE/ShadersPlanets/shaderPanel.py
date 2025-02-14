import bpy
from .shaderProperties import register as register_properties, unregister as unregister_properties
from .shaderOperators import SHADER_OT_CreatePlanetShader, SHADER_OT_UpdatePlanetShader

class SHADER_PT_PlanetPanel(bpy.types.Panel):
    bl_label = "Planet Shader Creator"
    bl_idname = "SHADER_PT_planet_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Shader'

    @classmethod
    def poll(cls, context):
        return context.active_object and context.active_object.type == 'MESH'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        obj = context.active_object

        # Material actions
        action_box = layout.box()
        action_box.label(text="Shader Actions")
        row = action_box.row(align=True)
        row.operator("shader.create_planet_shader", text="Create New Shader")
        row.operator("shader.update_planet_shader", text="Update Shader")

        # Material preview
        preview_box = layout.box()
        preview_box.label(text="Shader Preview")
        if obj and obj.active_material:
            row = preview_box.row()
            row.template_ID(obj, "active_material", new="material.new")
            row.template_preview(obj.active_material)

            # Dynamic parameters
            if hasattr(obj.active_material, 'dynamic_shader'):
                param_box = layout.box()
                param_box.label(text="Dynamic Parameters")
                col = param_box.column(align=True)
                col.prop(obj.active_material.dynamic_shader, "noise_scale")
                col.prop(obj.active_material.dynamic_shader, "noise_detail")
                col.prop(obj.active_material.dynamic_shader, "noise_roughness")
                col.prop(obj.active_material.dynamic_shader, "metallic")
                col.prop(obj.active_material.dynamic_shader, "roughness")
                col.prop(obj.active_material.dynamic_shader, "color_primary")
                col.prop(obj.active_material.dynamic_shader, "color_secondary")

            # Shader type selector
            shader_box = layout.box()
            shader_box.label(text="Planet Type")
            row = shader_box.row()
            row.prop(scene, "shader_type", text="")

            # Draw shader parameters based on type
            if scene.shader_type in ['rocky_planet', 'ice_planet', 'lava_planet', 'earth_like', 'alien_planet', 'gas_planet']:
                self.draw_planet_parameters(layout, scene, obj.active_material)
            else:
                self.draw_basic_parameters(layout, scene, obj.active_material)

    def draw_planet_parameters(self, layout, scene, material):
        # Surface Properties
        surface_box = layout.box()
        surface_box.label(text="Surface Properties")
        col = surface_box.column(align=True)
        col.prop(scene, "noise_scale", text="Surface Detail")
        col.prop(scene, "noise_detail", text="Detail Layers")
        col.prop(scene, "noise_roughness", text="Surface Roughness")

        # Color Properties
        color_box = layout.box()
        color_box.label(text="Color Properties")
        col = color_box.column(align=True)
        col.prop(scene, "color_primary", text="Primary Color")
        col.prop(scene, "color_secondary", text="Secondary Color")

        # Material Properties
        material_box = layout.box()
        material_box.label(text="Material Properties")
        col = material_box.column(align=True)
        col.prop(scene, "metallic", text="Metallic")
        col.prop(scene, "roughness", text="Roughness")

    def draw_basic_parameters(self, layout, scene, material):
        params_box = layout.box()
        params_box.label(text="Basic Parameters")
        col = params_box.column(align=True)
        col.prop(scene, "metallic", text="Metallic")
        col.prop(scene, "roughness", text="Roughness")
        col.prop(scene, "color_primary", text="Base Color")


def register():
    bpy.utils.register_class(SHADER_OT_CreatePlanetShader)
    bpy.utils.register_class(SHADER_OT_UpdatePlanetShader)
    bpy.utils.register_class(SHADER_PT_PlanetPanel)
    register_properties()

def unregister():
    unregister_properties()
    bpy.utils.unregister_class(SHADER_PT_PlanetPanel)
    bpy.utils.unregister_class(SHADER_OT_UpdatePlanetShader)
    bpy.utils.unregister_class(SHADER_OT_CreatePlanetShader)

def main():
    register()


if __name__ == "__main__":
    main()
