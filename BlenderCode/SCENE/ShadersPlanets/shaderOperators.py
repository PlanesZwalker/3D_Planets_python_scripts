import bpy
from typing import Optional
from .shaderImplementations import ShaderImplementations
from .shaderConfigLoader import ShaderConfig
from .shaderManager import ShaderManager

class SHADER_OT_CreatePlanetShader(bpy.types.Operator):
    bl_idname = "shader.create_planet_shader"
    bl_label = "Create Planet Shader"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object
        if not obj or obj.type != 'MESH':
            self.report({'ERROR'}, "Select a mesh object first")
            return {'CANCELLED'}

        try:
            config = self.build_shader_config(context.scene)
            material = self.create_material(config)
            self.apply_material_to_selected(material)
            context.space_data.shading.type = 'MATERIAL'
            context.view_layer.update()
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Failed to create shader: {str(e)}")
            return {'CANCELLED'}

    @staticmethod
    def build_shader_config(scene) -> ShaderConfig:
        return ShaderConfig(
            name=f"Planet_{scene.shader_type.capitalize()}",
            shader_type=scene.shader_type,
            noise_scale=scene.noise_scale,
            noise_detail=scene.noise_detail,
            noise_roughness=scene.get('noise_roughness', 0.5),
            noise_distortion=scene.get('noise_distortion', 0.3),
            color_mix_factor=scene.get('color_mix_factor', 0.5),
            color_primary=scene.color_primary,
            color_secondary=scene.color_secondary,
            roughness=scene.roughness,
            metallic=scene.metallic,
            emission_strength=scene.emission_strength,
            subsurface=scene.get('subsurface', 0.0),
            clearcoat=scene.get('clearcoat', 0.0),
            sheen=scene.get('sheen', 0.0),
            description=f"Generated {scene.shader_type} planet shader"
        )

    @staticmethod
    def create_material(config: ShaderConfig) -> bpy.types.Material:
        material = bpy.data.materials.new(name=config.name)
        material.use_nodes = True
        ShaderManager.create_or_update_shader(config.name, config)
        return material

    @staticmethod
    def apply_material_to_selected(material: bpy.types.Material) -> None:
        for obj in bpy.context.selected_objects:
            if obj.type == 'MESH':
                if len(obj.data.materials) == 0:
                    obj.data.materials.append(material)
                else:
                    obj.data.materials[0] = material

class SHADER_OT_UpdatePlanetShader(bpy.types.Operator):
    bl_idname = "shader.update_planet_shader"
    bl_label = "Update Planet Shader"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object
        if obj and obj.active_material:
            config = SHADER_OT_CreatePlanetShader.build_shader_config(context.scene)
            ShaderManager.create_or_update_shader(obj.active_material.name, config)
            context.view_layer.update()
            return {'FINISHED'}
        return {'CANCELLED'}

classes = (SHADER_OT_CreatePlanetShader, SHADER_OT_UpdatePlanetShader)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
