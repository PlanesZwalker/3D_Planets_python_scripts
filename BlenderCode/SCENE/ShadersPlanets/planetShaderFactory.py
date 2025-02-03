import os
import sys

import bpy

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ShadersPlanets.shaders import (
    create_glass_shader,
    create_principled_shader,
    create_emission_shader,
    create_nebula_shader,
    create_crystal_emission_shader,
    create_holographic_shader,
    create_solar_fire_shader,
    create_inferno_shader
)


class PlanetShaderFactory:
    @staticmethod
    def create_shader(name: str, noise_scale: float, noise_detail: float, color_primary: tuple, color_secondary: tuple,
                      shader_type: str) -> bpy.types.Material:
        mat = bpy.data.materials.new(name=name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        node_links = mat.node_tree.links
        nodes.clear()

        noise = nodes.new('ShaderNodeTexNoise')
        noise.inputs['Scale'].default_value = noise_scale
        noise.inputs['Detail'].default_value = noise_detail
        noise.inputs['Distortion'].default_value = 0.5

        color_ramp = nodes.new('ShaderNodeValToRGB')
        color_ramp.color_ramp.interpolation = 'EASE'
        color_ramp.color_ramp.elements[0].color = color_primary + (1,)
        color_ramp.color_ramp.elements[1].color = color_secondary + (1,)

        shader_dict = {
            "glass": lambda: create_glass_shader(nodes, node_links, color_primary),
            "principled": lambda: create_principled_shader(nodes, node_links, color_primary),
            "emission": lambda: create_emission_shader(nodes, node_links, color_primary),
            "nebula": lambda: create_nebula_shader(nodes, node_links, color_primary),
            "crystal_emission": lambda: create_crystal_emission_shader(nodes, node_links, color_primary),
            "holographic": lambda: create_holographic_shader(nodes, node_links, color_primary),
            "solar_fire": lambda: create_solar_fire_shader(nodes, node_links, color_primary),
            "inferno": lambda: create_inferno_shader(nodes, node_links, color_primary),
            "default": lambda: create_principled_shader(nodes, node_links, color_primary),
        }

        shader_function = shader_dict.get(shader_type.lower(), shader_dict["default"])
        shader = shader_function()

        emission = nodes.new("ShaderNodeEmission")
        emission.inputs['Color'].default_value = color_primary + (0.1,)
        emission.inputs['Strength'].default_value = 0.5

        output = nodes.new('ShaderNodeOutputMaterial')

        node_links.new(noise.outputs['Fac'], color_ramp.inputs['Fac'])

        if 'Base Color' in shader.inputs:
            node_links.new(color_ramp.outputs['Color'], shader.inputs['Base Color'])
        elif 'Color' in shader.inputs:
            node_links.new(color_ramp.outputs['Color'], shader.inputs['Color'])

        if shader_type.lower() not in ["emission", "solar_fire", "inferno"]:
            mix_shader = nodes.new('ShaderNodeMixShader')
            node_links.new(shader.outputs[0], mix_shader.inputs[1])
            node_links.new(emission.outputs[0], mix_shader.inputs[2])
            node_links.new(mix_shader.outputs[0], output.inputs['Surface'])
        else:
            node_links.new(shader.outputs[0], output.inputs['Surface'])

        return mat
