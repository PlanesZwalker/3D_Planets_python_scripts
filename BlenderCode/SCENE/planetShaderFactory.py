import bpy
from shaders import create_glass_shader, create_principled_shader, create_emission_shader

class PlanetShaderFactory:
    @staticmethod
    def create_shader(name: str, noise_scale: float, noise_detail: float, color_primary: tuple, color_secondary: tuple, shader_type: str) -> bpy.types.Material:
        mat = bpy.data.materials.new(name=name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()  # Clear any default nodes

        # Add Noise Texture node to simulate roughness and icy details
        noise = nodes.new('ShaderNodeTexNoise')
        noise.inputs['Scale'].default_value = noise_scale
        noise.inputs['Detail'].default_value = noise_detail
        noise.inputs['Distortion'].default_value = 0.5  # Slight distortion for realistic icy roughness

        # Add a Color Ramp node for blending the noise texture into color
        color_ramp = nodes.new('ShaderNodeValToRGB')
        color_ramp.color_ramp.interpolation = 'EASE'  # Smooth color transition
        color_ramp.color_ramp.elements[0].color = color_primary + (1,)
        color_ramp.color_ramp.elements[1].color = color_secondary + (1,)

        # Define the switch-case dictionary mapping for shader types
        shader_dict = {
            "glass": lambda: create_glass_shader(nodes, color_primary),
            "principled": lambda: create_principled_shader(nodes, color_primary),
            "emission": lambda: create_emission_shader(nodes, color_primary),
            "default": lambda: create_principled_shader(nodes, color_primary),  # Default case
        }

        # Switch case: get shader function based on shader_type
        shader_function = shader_dict.get(shader_type.lower(), shader_dict["default"])
        shader = shader_function()

        # Optional: Add subtle emission to give some slight cold glow effect in the night scene
        emission = nodes.new("ShaderNodeEmission")
        emission.inputs['Color'].default_value = color_primary + (0.1,)  # Subtle emission effect
        emission.inputs['Strength'].default_value = 0.5  # Low emission strength for night scene glow

        # Add output node
        output = nodes.new('ShaderNodeOutputMaterial')

        # Connect the nodes
        links.new(noise.outputs['Fac'], color_ramp.inputs['Fac'])

        # Connect color ramp to the shader based on shader type
        if 'Base Color' in shader.inputs:
            links.new(color_ramp.outputs['Color'], shader.inputs['Base Color'])
        elif 'Color' in shader.inputs:
            links.new(color_ramp.outputs['Color'], shader.inputs['Color'])

        # Mix the emission with the final shader (optional)
        if shader_type.lower() != "emission":  # Avoid mixing if the shader is already emission
            mix_shader = nodes.new('ShaderNodeMixShader')
            links.new(shader.outputs[0], mix_shader.inputs[1])
            links.new(emission.outputs[0], mix_shader.inputs[2])
            links.new(mix_shader.outputs[0], output.inputs['Surface'])
        else:
            links.new(shader.outputs[0], output.inputs['Surface'])

        return mat
