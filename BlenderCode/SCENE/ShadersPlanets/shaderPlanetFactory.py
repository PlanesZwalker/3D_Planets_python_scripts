import bpy
import sys
import os
from ShadersPlanets.shaderConfigLoader import ShaderConfigLoader
from ShadersPlanets.shaderManager import ShaderManager  # Ensure correct import path

class PlanetShaderFactory:
    @staticmethod
    def create_shader(name: str, noise_scale: float, noise_detail: float, color_primary: tuple,
                      color_secondary: tuple, shader_type: str, description: str,
                      emission_strength: float) -> bpy.types.Material:
        """Create a new shader material based on the provided parameters."""
        # Create a new material
        mat = bpy.data.materials.new(name=name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        node_links = mat.node_tree.links
        nodes.clear()

        # Create noise texture for surface detail
        noise = nodes.new('ShaderNodeTexNoise')
        noise.inputs['Scale'].default_value = noise_scale
        noise.inputs['Detail'].default_value = noise_detail
        noise.inputs['Distortion'].default_value = 0.5
        noise.location = (0, 0)

        # Create color ramp to blend primary and secondary colors
        color_ramp = nodes.new('ShaderNodeValToRGB')
        color_ramp.color_ramp.interpolation = 'EASE'
        color_ramp.color_ramp.elements[0].color = tuple(color_primary[:3]) + (1.0,)
        color_ramp.color_ramp.elements[1].color = tuple(color_secondary[:3]) + (1.0,)
        color_ramp.location = (300, 0)

        # Choose shader type from the dictionary and create the corresponding shader
        shader_function = {
            "glass": ShaderManager.create_glass_shader,
            "principled": ShaderManager.create_principled_shader,
            "emission": ShaderManager.create_emission_shader,
            "nebula": ShaderManager.create_nebula_shader,
            "crystal_emission": ShaderManager.create_crystal_emission_shader,
            "holographic": ShaderManager.create_holographic_shader,
            "solar_fire": ShaderManager.create_solar_fire_shader,
            "inferno": ShaderManager.create_inferno_shader,
            "default": ShaderManager.create_principled_shader
        }.get(shader_type.lower(), ShaderManager.create_principled_shader)

        shader = shader_function(nodes, node_links, color_primary)
        shader.location = (600, 0)

        # Create and configure emission shader for glow effect
        emission = nodes.new('ShaderNodeEmission')
        emission.inputs['Color'].default_value = tuple(color_primary[:3]) + (color_primary[3] + 0.1,) if len(
            color_primary) >= 4 else tuple(color_primary) + (1.0,)
        emission.inputs['Strength'].default_value = emission_strength  # Use the passed emission_strength here
        emission.location = (900, 0)

        # Create volumetric atmosphere (optional for gas planets)
        volume_shader = nodes.new('ShaderNodeVolumePrincipled')
        volume_shader.inputs['Density'].default_value = 0.1  # Adjust this for cloud density or gas giant effects
        volume_shader.inputs['Anisotropy'].default_value = 0.85  # Controls scattering in atmosphere
        volume_shader.location = (1200, 0)

        # Output node
        output = nodes.new('ShaderNodeOutputMaterial')
        output.location = (1500, 0)

        # Ensure proper connection of noise texture to color ramp
        node_links.new(noise.outputs['Fac'], color_ramp.inputs['Fac'])

        # Ensure color ramp is connected to the shader
        if 'Base Color' in shader.inputs:
            node_links.new(color_ramp.outputs['Color'], shader.inputs['Base Color'])
        elif 'Color' in shader.inputs:
            node_links.new(color_ramp.outputs['Color'], shader.inputs['Color'])

        # Handle mixing based on shader type (Emission or other shaders)
        if shader_type.lower() not in ["emission", "solar_fire", "inferno"]:
            # Mix the surface shader and the emission shader
            mix_shader = nodes.new('ShaderNodeMixShader')
            mix_shader.location = (1800, 0)

            # Mix the shaders: add base shader and emission shader
            node_links.new(shader.outputs[0], mix_shader.inputs[1])  # Base Shader (Surface)
            node_links.new(emission.outputs[0], mix_shader.inputs[2])  # Emission Shader

            # Connect to the output
            node_links.new(mix_shader.outputs[0], output.inputs['Surface'])
        else:
            # Directly connect emission to output for emission-based shaders
            node_links.new(emission.outputs[0], output.inputs['Surface'])

        return mat

    @staticmethod
    def load_and_create_planet_shaders():
        """Load shader configurations and create materials for selected planets."""
        shader_configs = ShaderConfigLoader.load_config()

        for planet_name, selected_planet_data in shader_configs.items():
            # Create shader for the planet
            material = PlanetShaderFactory.create_shader(
                selected_planet_data.name,
                selected_planet_data.noise_scale,
                selected_planet_data.noise_detail,
                selected_planet_data.color_primary,
                selected_planet_data.color_secondary,
                selected_planet_data.shader_type,
                selected_planet_data.description,
                selected_planet_data.emission_strength
            )

            # Apply the material to selected mesh objects in the scene
            for obj in bpy.context.selected_objects:
                if obj.type == 'MESH':
                    if len(obj.data.materials) == 0:
                        obj.data.materials.append(material)
                    else:
                        obj.data.materials[0] = material

            # Force update the object view
            bpy.context.view_layer.update()
