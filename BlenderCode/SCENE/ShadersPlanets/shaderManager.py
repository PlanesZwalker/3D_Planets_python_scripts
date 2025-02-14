import logging
import bpy
from typing import Tuple, Dict, Callable, Any, Optional
from bpy.types import NodeSocketColor, Node, NodeGroup
from .shaderBase import ShaderBase
from .shaderImplementations import ShaderImplementations

logger = logging.getLogger(__name__)

class ShaderManager(ShaderBase):
    @staticmethod
    def create_shader_group(name: str) -> NodeGroup:
        if name in bpy.data.node_groups:
            return bpy.data.node_groups[name]

        group = bpy.data.node_groups.new(name=name, type='ShaderNodeTree')
        group.inputs.new('NodeSocketColor', 'Color Primary')
        group.inputs.new('NodeSocketColor', 'Color Secondary')
        group.inputs.new('NodeSocketFloat', 'Metallic')
        group.inputs.new('NodeSocketFloat', 'Roughness')
        group.inputs.new('NodeSocketFloat', 'Noise Scale')
        group.outputs.new('NodeSocketShader', 'Shader')
        return group

    @staticmethod
    def setup_group_nodes(group: NodeGroup, config) -> None:
        nodes = group.nodes
        links = group.links
        nodes.clear()

        group_in = nodes.new('NodeGroupInput')
        group_out = nodes.new('NodeGroupOutput')
        principled = ShaderBase.create_principled_shader(nodes, links, config)

        links.new(group_in.outputs['Metallic'], principled.inputs['Metallic'])
        links.new(group_in.outputs['Roughness'], principled.inputs['Roughness'])
        links.new(principled.outputs[0], group_out.inputs['Shader'])

    @classmethod
    def create_shader_from_config(cls, nodes: Any, node_links: Any, config) -> Node:
        nodes.clear()
        output = nodes.new('ShaderNodeOutputMaterial')
        output.location = (600, 0)

        shader_type = cls.validate_shader_type(config.shader_type, config)
        shader_methods = {
            "rocky_planet": ShaderImplementations.create_rocky_planet_shader,
            "gas_planet": ShaderImplementations.create_gas_planet_shader,
            "ice_planet": ShaderImplementations.create_ice_planet_shader,
            "lava_planet": ShaderImplementations.create_lava_planet_shader,
            "earth_like": ShaderImplementations.create_earth_like_shader,
            "alien_planet": ShaderImplementations.create_alien_planet_shader
        }

        shader_method = shader_methods.get(shader_type)
        if shader_method:
            shader = shader_method(nodes, node_links, config)
            node_links.new(shader.outputs[0], output.inputs['Surface'])
            return shader

        shader = cls.create_principled_shader(nodes, node_links, config)
        node_links.new(shader.outputs[0], output.inputs['Surface'])
        return shader

    @classmethod
    def create_or_update_shader(cls, material_name: str, config) -> None:
        mat = bpy.data.materials.get(material_name)
        if not mat:
            mat = bpy.data.materials.new(name=material_name)
        mat.use_nodes = True

        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        shader = cls.create_shader_from_config(nodes, links, config)

        mat["color_primary"] = config.color_primary
        mat["color_secondary"] = config.color_secondary
        mat["metallic"] = config.metallic
        mat["roughness"] = config.roughness
        mat["noise_scale"] = config.noise_scale

    @classmethod
    def validate_shader_type(cls, shader_type: Optional[str], config) -> str:
        if not isinstance(shader_type, str):
            return "principled"
        normalized_type = shader_type.lower().strip()
        return normalized_type if normalized_type in cls.VALID_SHADER_TYPES else "principled"
