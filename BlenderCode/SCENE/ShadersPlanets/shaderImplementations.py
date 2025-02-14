import bpy
from typing import Any, Dict, Tuple
from .shaderBase import ShaderBase


class ShaderImplementations(ShaderBase):
    """Implements specific shader creation methods for different planet types."""

    @staticmethod
    def setup_common_nodes(nodes: Any) -> Dict[str, Any]:
        """Create and return commonly used nodes with proper positioning."""
        common_nodes = {
            'principled': nodes.new('ShaderNodeBsdfPrincipled'),
            'noise': nodes.new('ShaderNodeTexNoise'),
            'color_ramp': nodes.new('ShaderNodeValToRGB'),
            'mapping': nodes.new('ShaderNodeMapping'),
            'tex_coord': nodes.new('ShaderNodeTexCoord')
        }

        positions = {
            'principled': (400, 0),
            'noise': (-200, 0),
            'color_ramp': (0, 200),
            'mapping': (-400, 0),
            'tex_coord': (-600, 0)
        }

        for node_name, position in positions.items():
            if node_name in common_nodes:
                common_nodes[node_name].location = position

        return common_nodes

    @staticmethod
    def connect_basic_nodes(node_links: Any, nodes: Dict[str, Any]) -> None:
        """Connect commonly used nodes."""
        # Check if the 'noise' node has any outputs before trying to access them
        if hasattr(nodes['noise'], 'outputs'):
            noise_outputs = nodes['noise'].outputs

            # Check if the 'Fac' property exists in the 'color_ramp' node's inputs
            if hasattr(nodes['color_ramp'], 'inputs'):
                color_ramp_inputs = nodes['color_ramp'].inputs

                # Try to connect the nodes using their outputs and inputs
                for output in noise_outputs:
                    for input in color_ramp_inputs:
                        if output.name == input.name:
                            node_links.new(output, input)

    @staticmethod
    def setup_noise_node(noise: Any, config) -> None:
        """Configure noise node with standard parameters."""
        noise.inputs['Scale'].default_value = config.noise_scale
        noise.inputs['Detail'].default_value = config.noise_detail
        noise.inputs['Roughness'].default_value = config.noise_roughness

    @staticmethod
    def setup_color_ramp(color_ramp, config):
        # Get the elements
        elements = color_ramp.color_ramp.elements

        # Set interpolation mode
        color_ramp.color_ramp.interpolation = 'LINEAR'

        # Set first element
        elements[0].position = 0.0
        elements[0].color = ShaderBase.convert_to_tuple(config.color_primary)

        # Set second element
        if len(elements) < 2:
            elements.new(1.0)
        elements[1].position = 1.0
        elements[1].color = ShaderBase.convert_to_tuple(config.color_secondary)

        # Create new elements
        e1 = color_ramp.color_ramp.elements.new(0.0)
        e2 = color_ramp.color_ramp.elements.new(1.0)

        # Set colors
        e1.color = ShaderBase.convert_to_tuple(config.color_primary)
        e2.color = ShaderBase.convert_to_tuple(config.color_secondary)

    @staticmethod
    def create_rocky_planet_shader(nodes: Any, node_links: Any, config) -> Any:
        common_nodes = ShaderImplementations.setup_common_nodes(nodes)
        bump = nodes.new('ShaderNodeBump')
        bump.location = (200, -200)

        ShaderImplementations.setup_noise_node(common_nodes['noise'], config)
        ShaderImplementations.setup_color_ramp(common_nodes['color_ramp'], config)

        common_nodes['principled'].inputs['Roughness'].default_value = config.roughness
        common_nodes['principled'].inputs['Metallic'].default_value = config.metallic

        ShaderImplementations.connect_basic_nodes(node_links, common_nodes)
        node_links.new(common_nodes['noise'].outputs['Fac'], bump.inputs['Height'])
        node_links.new(bump.outputs['Normal'], common_nodes['principled'].inputs['Normal'])
        node_links.new(common_nodes['color_ramp'].outputs[0], common_nodes['principled'].inputs['Base Color'])

        return common_nodes['principled']

    @staticmethod
    def create_gas_planet_shader(nodes: Any, node_links: Any, config) -> Any:
        common_nodes = ShaderImplementations.setup_common_nodes(nodes)

        noise2 = nodes.new('ShaderNodeTexNoise')
        voronoi = nodes.new('ShaderNodeTexVoronoi')
        mix_rgb = nodes.new('ShaderNodeMixRGB')
        wave = nodes.new('ShaderNodeTexWave')

        noise2.location = (-200, -200)
        voronoi.location = (-200, -400)
        mix_rgb.location = (200, 0)
        wave.location = (-200, 200)

        wave.wave_type = 'BANDS'
        wave.bands_direction = 'X'
        wave.inputs['Scale'].default_value = 2.0
        wave.inputs['Distortion'].default_value = 2.0

        ShaderImplementations.setup_noise_node(common_nodes['noise'], config)
        noise2.inputs['Scale'].default_value = config.noise_scale * 2
        voronoi.inputs['Scale'].default_value = config.noise_scale * 3
        voronoi.feature = 'SMOOTH_F1'

        common_nodes['principled'].inputs['Metallic'].default_value = 0.0
        common_nodes['principled'].inputs['Roughness'].default_value = 0.3
        common_nodes['principled'].inputs['Specular IOR Level'].default_value = 1.45


        node_links.new(common_nodes['mapping'].outputs['Vector'], wave.inputs['Vector'])
        node_links.new(common_nodes['mapping'].outputs['Vector'], noise2.inputs['Vector'])
        node_links.new(common_nodes['mapping'].outputs['Vector'], voronoi.inputs['Vector'])
        node_links.new(wave.outputs['Fac'], mix_rgb.inputs[0])
        node_links.new(noise2.outputs['Fac'], mix_rgb.inputs[1])
        node_links.new(voronoi.outputs['Distance'], mix_rgb.inputs[2])
        node_links.new(mix_rgb.outputs['Color'], common_nodes['principled'].inputs['Base Color'])

        return common_nodes['principled']

    @staticmethod
    def create_ice_planet_shader(nodes: Any, node_links: Any, config) -> Any:
        common_nodes = ShaderImplementations.setup_common_nodes(nodes)

        noise2 = nodes.new('ShaderNodeTexNoise')
        voronoi = nodes.new('ShaderNodeTexVoronoi')
        mix_rgb = nodes.new('ShaderNodeMixRGB')
        bump = nodes.new('ShaderNodeBump')

        noise2.location = (-200, -200)
        voronoi.location = (-200, -400)
        mix_rgb.location = (200, 0)
        bump.location = (200, -200)

        ShaderImplementations.setup_noise_node(common_nodes['noise'], config)
        noise2.inputs['Scale'].default_value = config.noise_scale * 2
        voronoi.inputs['Scale'].default_value = config.noise_scale * 3

        common_nodes['principled'].inputs['Base Color'].default_value = (0.8, 0.9, 1.0, 1.0)
        common_nodes['principled'].inputs['Metallic'].default_value = 0.2
        common_nodes['principled'].inputs['Roughness'].default_value = 0.2
        common_nodes['principled'].inputs['IOR'].default_value = 1.31
        common_nodes['principled'].inputs['Clearcoat Roughness'].default_value = 0.5

        if 'Transmission' in common_nodes['principled'].inputs:
            common_nodes['principled'].inputs['Transmission'].default_value = 0.2
        elif 'Transmission Weight' in common_nodes['principled'].inputs:
            common_nodes['principled'].inputs['Transmission Weight'].default_value = 0.2

        node_links.new(common_nodes['mapping'].outputs['Vector'], noise2.inputs['Vector'])
        node_links.new(common_nodes['mapping'].outputs['Vector'], voronoi.inputs['Vector'])
        node_links.new(common_nodes['noise'].outputs['Fac'], mix_rgb.inputs[0])
        node_links.new(noise2.outputs['Fac'], mix_rgb.inputs[1])
        node_links.new(voronoi.outputs['Distance'], mix_rgb.inputs[2])
        node_links.new(mix_rgb.outputs['Color'], common_nodes['principled'].inputs['Base Color'])
        node_links.new(noise2.outputs['Fac'], bump.inputs['Height'])
        node_links.new(bump.outputs['Normal'], common_nodes['principled'].inputs['Normal'])

        return common_nodes['principled']

    @staticmethod
    def create_lava_planet_shader(nodes: Any, node_links: Any, config) -> Any:
        common_nodes = ShaderImplementations.setup_common_nodes(nodes)

        emission = nodes.new('ShaderNodeEmission')
        mix_shader = nodes.new('ShaderNodeMixShader')
        noise2 = nodes.new('ShaderNodeTexNoise')
        voronoi = nodes.new('ShaderNodeTexVoronoi')

        emission.location = (200, -200)
        mix_shader.location = (400, -200)
        noise2.location = (-200, -200)
        voronoi.location = (-200, -400)

        ShaderImplementations.setup_noise_node(common_nodes['noise'], config)
        noise2.inputs['Scale'].default_value = config.noise_scale * 3
        voronoi.inputs['Scale'].default_value = config.noise_scale * 2

        emission.inputs['Strength'].default_value = 5.0
        common_nodes['principled'].inputs['Roughness'].default_value = 0.9
        common_nodes['principled'].inputs['Metallic'].default_value = 0.0

        node_links.new(common_nodes['mapping'].outputs['Vector'], noise2.inputs['Vector'])
        node_links.new(common_nodes['mapping'].outputs['Vector'], voronoi.inputs['Vector'])
        node_links.new(common_nodes['noise'].outputs['Fac'], common_nodes['principled'].inputs['Base Color'])
        node_links.new(noise2.outputs['Fac'], emission.inputs['Color'])
        node_links.new(voronoi.outputs['Distance'], mix_shader.inputs[0])
        node_links.new(common_nodes['principled'].outputs[0], mix_shader.inputs[1])
        node_links.new(emission.outputs[0], mix_shader.inputs[2])

        return mix_shader

    @staticmethod
    def create_earth_like_shader(nodes: Any, node_links: Any, config) -> Any:
        common_nodes = ShaderImplementations.setup_common_nodes(nodes)

        noise2 = nodes.new('ShaderNodeTexNoise')
        color_ramp2 = nodes.new('ShaderNodeValToRGB')
        mix_rgb = nodes.new('ShaderNodeMixRGB')

        noise2.location = (-200, -200)
        color_ramp2.location = (0, -200)
        mix_rgb.location = (200, 0)

        ShaderImplementations.setup_noise_node(common_nodes['noise'], config)
        noise2.inputs['Scale'].default_value = config.noise_scale * 2

        common_nodes['color_ramp'].color_ramp.elements[0].color = (0.0, 0.2, 0.5, 1.0)
        common_nodes['color_ramp'].color_ramp.elements[1].color = (0.2, 0.5, 0.1, 1.0)

        color_ramp2.color_ramp.elements[0].color = (0.8, 0.8, 0.8, 1.0)
        color_ramp2.color_ramp.elements[1].color = (0.2, 0.2, 0.2, 1.0)

        common_nodes['principled'].inputs['Roughness'].default_value = 0.5
        common_nodes['principled'].inputs['Metallic'].default_value = 0.0

        node_links.new(common_nodes['mapping'].outputs['Vector'], noise2.inputs['Vector'])
        node_links.new(common_nodes['noise'].outputs['Fac'], common_nodes['color_ramp'].inputs[0])
        node_links.new(noise2.outputs['Fac'], color_ramp2.inputs[0])
        node_links.new(common_nodes['color_ramp'].outputs['Color'], mix_rgb.inputs[1])
        node_links.new(color_ramp2.outputs['Color'], mix_rgb.inputs[2])
        node_links.new(mix_rgb.outputs['Color'], common_nodes['principled'].inputs['Base Color'])

        return common_nodes['principled']

    @staticmethod
    def create_alien_planet_shader(nodes: Any, node_links: Any, config) -> Any:
        common_nodes = ShaderImplementations.setup_common_nodes(nodes)

        voronoi1 = nodes.new('ShaderNodeTexVoronoi')
        voronoi2 = nodes.new('ShaderNodeTexVoronoi')
        color_ramp2 = nodes.new('ShaderNodeValToRGB')
        mix_rgb = nodes.new('ShaderNodeMixRGB')

        voronoi1.location = (-200, -200)
        voronoi2.location = (-200, -400)
        color_ramp2.location = (0, -200)
        mix_rgb.location = (200, 0)

        voronoi1.inputs['Scale'].default_value = config.noise_scale
        voronoi2.inputs['Scale'].default_value = config.noise_scale * 2
        common_nodes['noise'].inputs['Scale'].default_value = config.noise_scale * 3

        ShaderImplementations.setup_color_ramp(common_nodes['color_ramp'], config)
        color_ramp2.color_ramp.elements[0].color = (0.8, 0.4, 0.0, 1.0)
        color_ramp2.color_ramp.elements[1].color = (0.2, 0.0, 0.4, 1.0)

        common_nodes['principled'].inputs['Roughness'].default_value = 0.4
        common_nodes['principled'].inputs['Metallic'].default_value = 0.2

        node_links.new(common_nodes['mapping'].outputs['Vector'], voronoi1.inputs['Vector'])
        node_links.new(common_nodes['mapping'].outputs['Vector'], voronoi2.inputs['Vector'])
        node_links.new(voronoi1.outputs['Distance'], common_nodes['color_ramp'].inputs[0])
        node_links.new(voronoi2.outputs['Distance'], color_ramp2.inputs[0])
        node_links.new(common_nodes['color_ramp'].outputs['Color'], mix_rgb.inputs[1])
        node_links.new(color_ramp2.outputs['Color'], mix_rgb.inputs[2])
        node_links.new(common_nodes['noise'].outputs['Fac'], mix_rgb.inputs[0])
        node_links.new(mix_rgb.outputs['Color'], common_nodes['principled'].inputs['Base Color'])
        node_links.new(common_nodes['color_ramp'].outputs[0], common_nodes['principled'].inputs['Base Color'])

        return common_nodes['principled']

def register():
    bpy.utils.register_class(ShaderImplementations)

def unregister():
    bpy.utils.unregister_class(ShaderImplementations)

if __name__ == "__main__":
    register()
