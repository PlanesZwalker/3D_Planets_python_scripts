bl_info = {
    "name": "Planet Shader Creator",
    "blender": (4, 3, 2),
    "category": "Shading",
    "author": "AnnJ",
    "version": (1, 0),
    "description": "Create and manage planet shaders",
}

import bpy
from .shaderBase import ShaderBase
from .shaderManager import ShaderManager
from .shaderImplementations import ShaderImplementations
from .shaderOperators import SHADER_OT_CreatePlanetShader, SHADER_OT_UpdatePlanetShader
from .shaderProperties import register as register_properties, unregister as unregister_properties
from .shaderPanel import register as register_panel, unregister as unregister_panel

classes = (
    ShaderBase,
    ShaderManager,
    ShaderImplementations,
    SHADER_OT_CreatePlanetShader,
    SHADER_OT_UpdatePlanetShader
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    register_properties()
    register_panel()

def unregister():
    unregister_panel()
    unregister_properties()
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
