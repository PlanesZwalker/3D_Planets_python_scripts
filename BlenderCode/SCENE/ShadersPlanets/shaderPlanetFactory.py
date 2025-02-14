import bpy
from .shaderConfigLoader import ShaderConfigLoader, ShaderConfig, logger
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class PlanetShaderFactory:
    @staticmethod
    def validate_shader_type(shader_type: str) -> str:
        if isinstance(shader_type, str):
            return shader_type.strip().lower()
        print(f"WARNING: Invalid shader_type '{shader_type}', defaulting to 'principled'")
        return "principled"

    @staticmethod
    def create_noise_texture(nodes, noise_scale: float, noise_detail: float) -> bpy.types.Node:
        noise = nodes.new('ShaderNodeTexNoise')
        noise.inputs['Scale'].default_value = noise_scale
        noise.inputs['Detail'].default_value = noise_detail
        noise.inputs['Distortion'].default_value = 0.5
        noise.location = (0, 0)
        return noise

    @staticmethod
    def create_color_ramp(nodes, color_primary: tuple, color_secondary: tuple) -> bpy.types.Node:
        color_ramp = nodes.new('ShaderNodeValToRGB')
        color_ramp.color_ramp.interpolation = 'EASE'

        primary_color = (*color_primary[:3], color_primary[3] if len(color_primary) > 3 else 1.0)
        secondary_color = (*color_secondary[:3], color_secondary[3] if len(color_secondary) > 3 else 1.0)

        color_ramp.color_ramp.elements[0].color = primary_color
        color_ramp.color_ramp.elements[1].color = secondary_color
        color_ramp.location = (300, 0)
        return color_ramp

    @staticmethod
    def create_emission_shader(nodes, primary_color: tuple, emission_strength: float) -> bpy.types.Node:
        emission = nodes.new('ShaderNodeEmission')
        emission.inputs['Color'].default_value = primary_color
        emission.inputs['Strength'].default_value = emission_strength
        emission.location = (900, 0)
        return emission

    @staticmethod
    def create_volume_shader(nodes) -> bpy.types.Node:
        volume_shader = nodes.new('ShaderNodeVolumePrincipled')
        volume_shader.inputs['Density'].default_value = 0.1
        volume_shader.inputs['Anisotropy'].default_value = 0.85
        volume_shader.location = (1200, 0)
        return volume_shader

    @staticmethod
    def link_nodes(node_links, output_node, input_node, output_socket, input_socket):
        """Helper function to link nodes."""
        try:
            # Use index-based connection for reliability across all node types
            node_links.new(output_node.outputs[0], input_node.inputs[input_socket])
            logger.debug(f"Successfully linked nodes: {output_node.name} -> {input_node.name}")
        except Exception as e:
            logger.error(f"Failed to link nodes: {e}")

    @staticmethod
    def create_shader(config: ShaderConfig) -> bpy.types.Material:
        from .shaderManager import ShaderManager
        logger = logging.getLogger(__name__)

        # Initial setup
        logger.debug(f"Starting shader creation for {config.name}")
        shader_type = PlanetShaderFactory.validate_shader_type(config.shader_type)
        logger.debug(f"Using shader type: {shader_type}")

        # Material creation
        mat = bpy.data.materials.new(name=config.name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        node_links = mat.node_tree.links
        nodes.clear()
        logger.debug("Material node tree initialized")

        # Node creation with detailed logging
        noise = PlanetShaderFactory.create_noise_texture(nodes, config.noise_scale, config.noise_detail)
        logger.debug(f"Noise texture created: scale={config.noise_scale}, detail={config.noise_detail}")

        color_ramp = PlanetShaderFactory.create_color_ramp(nodes, config.color_primary, config.color_secondary)
        logger.debug(f"Color ramp created with colors: {config.color_primary} -> {config.color_secondary}")

        shader = ShaderManager.create_shader_from_config(nodes, node_links, config)
        shader.location = (600, 0)
        logger.debug(f"Main shader created: {shader.name}")

        emission = PlanetShaderFactory.create_emission_shader(nodes, config.color_primary, config.emission_strength)
        logger.debug(f"Emission shader created with strength: {config.emission_strength}")

        volume_shader = PlanetShaderFactory.create_volume_shader(nodes)
        logger.debug("Volume shader created")

        output = nodes.new('ShaderNodeOutputMaterial')
        output.location = (1500, 0)
        logger.debug("Output node created")

        # Node linking with detailed logging
        logger.debug("Starting node connections...")

        # Log available inputs/outputs
        logger.debug(f"Noise outputs: {[o.name for o in noise.outputs]}")
        logger.debug(f"Color ramp inputs: {[i.name for i in color_ramp.inputs]}")
        logger.debug(f"Shader inputs: {[i.name for i in shader.inputs]}")

        # Link nodes
        PlanetShaderFactory.link_nodes(node_links, noise, color_ramp, 'Fac', 'Fac')
        logger.debug("Noise -> Color Ramp linked")

        PlanetShaderFactory.link_nodes(node_links, color_ramp, shader, 'Color', 0)
        logger.debug("Color Ramp -> Shader linked")

        # Update the emission to output connection in create_shader method
        if shader_type.lower() not in ["emission", "solar_fire", "inferno"]:
            mix_shader = nodes.new('ShaderNodeMixShader')
            mix_shader.location = (1800, 0)
            logger.debug("Created mix shader node")

            # Use correct socket indices for reliable connections
            node_links.new(shader.outputs[0], mix_shader.inputs[1])
            node_links.new(emission.outputs[0], mix_shader.inputs[2])
            node_links.new(mix_shader.outputs[0], output.inputs['Surface'])
            logger.debug("Mix shader connections completed")
        else:
            # Direct connection using node_links.new for emission shader
            node_links.new(emission.outputs[0], output.inputs['Surface'])
            logger.debug("Direct emission to output connection completed")

        logger.debug(f"Shader creation completed for {config.name}")
        return mat

    @staticmethod
    def create_dynamic_material(material_name: str, config: ShaderConfig) -> bpy.types.Material:
        """Create a new material with dynamic parameters"""
        mat = bpy.data.materials.new(name=material_name)
        mat.use_nodes = True

        # Initialize dynamic properties
        mat.dynamic_shader.noise_scale = config.noise_scale
        mat.dynamic_shader.noise_detail = config.noise_detail
        mat.dynamic_shader.noise_roughness = config.noise_roughness
        mat.dynamic_shader.metallic = config.metallic
        mat.dynamic_shader.roughness = config.roughness
        mat.dynamic_shader.color_primary = config.color_primary
        mat.dynamic_shader.color_secondary = config.color_secondary

        # Create initial shader setup
        ShaderManager.create_or_update_shader(material_name, config)

        return mat

    @staticmethod
    def update_material_parameters(material: bpy.types.Material) -> None:
        """Update shader parameters based on dynamic properties"""
        if not material.use_nodes:
            return

        group_node = next((node for node in material.node_tree.nodes
                           if node.type == 'GROUP'), None)
        if not group_node:
            return

        # Update node group inputs
        group_node.inputs['Color Primary'].default_value = material.dynamic_shader.color_primary
        group_node.inputs['Color Secondary'].default_value = material.dynamic_shader.color_secondary
        group_node.inputs['Metallic'].default_value = material.dynamic_shader.metallic
        group_node.inputs['Roughness'].default_value = material.dynamic_shader.roughness
        group_node.inputs['Noise Scale'].default_value = material.dynamic_shader.noise_scale

    @staticmethod
    def load_and_create_planet_shaders():
        """Load configurations and create dynamic materials"""
        try:
            shader_configs = ShaderConfigLoader.load_config()

            for planet_name, config in shader_configs.items():
                material = PlanetShaderFactory.create_dynamic_material(planet_name, config)

                # Apply material to selected objects
                for obj in bpy.context.selected_objects:
                    if obj.type == 'MESH':
                        if len(obj.data.materials) == 0:
                            obj.data.materials.append(material)
                        else:
                            obj.data.materials[0] = material

                # Set up update callback
                material.update_tag()
                PlanetShaderFactory.update_material_parameters(material)

            bpy.context.view_layer.update()

        except Exception as e:
            logger.error(f"Error creating planet shaders: {e}")

def register():
    """Register factory components"""
    ShaderConfigLoader.register_properties()
    logger.info("Planet Shader Factory registered")

def unregister():
    """Unregister factory components"""
    ShaderConfigLoader.unregister_properties()
    logger.info("Planet Shader Factory unregistered")

