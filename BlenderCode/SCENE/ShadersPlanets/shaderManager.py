import logging

logger = logging.getLogger(__name__)

class ShaderManager:
    shaders = {
        "cycles": {
            "glass": "create_glass_shader",
            "principled": "create_principled_shader",
            "emission": "create_emission_shader",
            "nebula": "create_nebula_shader",
            "crystal_emission": "create_crystal_emission_shader",
            "holographic": "create_holographic_shader",
            "solar_fire": "create_solar_fire_shader",
            "inferno": "create_inferno_shader"
        },
        "eevee": {
            "glass": "create_glass_shader",
            "principled": "create_principled_shader",
            "emission": "create_emission_shader",
            "nebula": "create_nebula_shader",
            "crystal_emission": "create_crystal_emission_shader",
            "holographic": "create_holographic_shader",
            "solar_fire": "create_solar_fire_shader",
            "inferno": "create_inferno_shader"
        }
    }

    best_for = {
        "cycles": ["principled", "glass", "emission", "nebula", "crystal_emission", "holographic", "solar_fire", "inferno"],
        "eevee": ["principled", "glass", "emission", "holographic", "solar_fire", "inferno"]
    }

    @staticmethod
    def convert_to_tuple(color):
        """Ensure the color is in RGBA format with a default alpha of 1.0."""
        if len(color) == 3:  # RGB input
            return tuple(color) + (1.0,)  # Add default alpha
        elif len(color) == 4:  # RGBA input
            return tuple(color)
        else:
            raise ValueError("Color must be a 3 or 4 component tuple")

    @staticmethod
    def create_shader_node(shader_type, nodes, node_links, color_primary, **params):
        """General method to create shader nodes based on type."""
        try:
            color_primary = ShaderManager.convert_to_tuple(color_primary)

            logger.debug(f"Creating shader '{shader_type}' with color {color_primary}")

            # Common properties for all shaders
            noise_texture = nodes.new('ShaderNodeTexNoise')
            noise_texture.inputs['Roughness'].default_value = params.get('noise_roughness', 0.5)
            noise_texture.inputs['Distortion'].default_value = params.get('noise_distortion', 0.0)

            color_mix = nodes.new('ShaderNodeMixRGB')
            color_mix.inputs[0].default_value = params.get('color_mix_factor', 0.5)

            # Call the appropriate shader creation method
            shader_creation_method = getattr(ShaderManager, f"create_{shader_type}_shader", None)
            if shader_creation_method:
                return shader_creation_method(nodes, node_links, color_primary)
            else:
                raise ValueError(f"Unknown shader type '{shader_type}'")

        except Exception as e:
            logger.error(f"Error creating shader node '{shader_type}': {e}")
            raise

    @staticmethod
    def create_principled_shader(nodes, node_links, color_primary):
        """Create a Principled BSDF shader."""
        try:
            color_primary = ShaderManager.convert_to_tuple(color_primary)

            shader = nodes.new("ShaderNodeBsdfPrincipled")
            shader.inputs['Base Color'].default_value = color_primary
            shader.inputs['Metallic'].default_value = 0.8  # Default value, can be adjusted
            shader.inputs['Roughness'].default_value = 0.2  # Default value, can be adjusted

            optional_props = {
                'Subsurface': 0.1,
                'Clearcoat': 0.5,
                'Sheen': 0.3
            }

            for prop, value in optional_props.items():
                if prop in shader.inputs:
                    shader.inputs[prop].default_value = value

            logger.debug("Principled Shader created successfully.")
            return shader
        except Exception as e:
            logger.error(f"Error creating Principled Shader: {e}")
            raise

    @staticmethod
    def create_glass_shader(nodes, node_links, color_primary):
        """Create Glass shader."""
        try:
            color_primary = ShaderManager.convert_to_tuple(color_primary)

            mix = nodes.new('ShaderNodeMixShader')
            glass1 = nodes.new('ShaderNodeBsdfGlass')
            glass2 = nodes.new('ShaderNodeBsdfGlass')

            glass1.inputs['Color'].default_value = color_primary
            glass2.inputs['Color'].default_value = (color_primary[2], color_primary[0], color_primary[1], 1.0)
            glass1.inputs['IOR'].default_value = 1.4
            glass2.inputs['IOR'].default_value = 1.2

            mix.inputs[0].default_value = 0.5
            node_links.new(glass1.outputs[0], mix.inputs[1])
            node_links.new(glass2.outputs[0], mix.inputs[2])

            logger.debug("Glass Shader created successfully.")
            return mix
        except Exception as e:
            logger.error(f"Error creating Glass Shader: {e}")
            raise

    @staticmethod
    def create_emission_shader(nodes, node_links, color_primary):
        """Create Emission shader."""
        try:
            color_primary = ShaderManager.convert_to_tuple(color_primary)

            # Create the emission shader node
            emission = nodes.new('ShaderNodeEmission')

            # Print out the available inputs for debugging purposes
            print("Emission Shader Inputs:")
            for input_name in emission.inputs:
                print(f"- {input_name}")

            # Now check if 'Color' and 'Strength' are available
            if 'Color' in emission.inputs and 'Strength' in emission.inputs:
                emission.inputs['Color'].default_value = color_primary  # Set color
                emission.inputs['Strength'].default_value = 5.0  # Set strength
            else:
                logger.error("Emission shader does not have expected inputs: Color or Strength missing")

            logger.debug("Emission Shader created successfully.")
            return emission
        except Exception as e:
            logger.error(f"Error creating Emission Shader: {e}")
            raise

    @staticmethod
    def create_nebula_shader(nodes, node_links, color_primary):
        """Create Nebula shader."""
        try:
            color_primary = ShaderManager.convert_to_tuple(color_primary)

            volume = nodes.new('ShaderNodeVolumePrincipled')
            volume.inputs['Color'].default_value = color_primary
            volume.inputs['Density'].default_value = 0.3

            logger.debug("Nebula Shader created successfully.")
            return volume
        except Exception as e:
            logger.error(f"Error creating Nebula Shader: {e}")
            raise

    @staticmethod
    def create_crystal_emission_shader(nodes, node_links, color_primary):
        """Create Crystal Emission shader."""
        try:
            color_primary = ShaderManager.convert_to_tuple(color_primary)

            mix = nodes.new('ShaderNodeMixShader')
            glass = nodes.new('ShaderNodeBsdfGlass')
            emission = nodes.new('ShaderNodeEmission')

            glass.inputs['Color'].default_value = color_primary
            glass.inputs['IOR'].default_value = 1.6
            emission.inputs['Color'].default_value = color_primary
            emission.inputs['Strength'].default_value = 1.5

            mix.inputs[0].default_value = 0.3
            node_links.new(glass.outputs[0], mix.inputs[1])
            node_links.new(emission.outputs[0], mix.inputs[2])

            logger.debug("Crystal Emission Shader created successfully.")
            return mix
        except Exception as e:
            logger.error(f"Error creating Crystal Emission Shader: {e}")
            raise

    @staticmethod
    def create_holographic_shader(nodes, node_links, color_primary):
        """Create Holographic shader."""
        try:
            color_primary = ShaderManager.convert_to_tuple(color_primary)

            shader = nodes.new("ShaderNodeBsdfPrincipled")
            shader.inputs['Base Color'].default_value = color_primary
            shader.inputs['Metallic'].default_value = 1.0
            shader.inputs['Roughness'].default_value = 0.1

            if 'Sheen' in shader.inputs:
                shader.inputs['Sheen'].default_value = 1.0

            logger.debug("Holographic Shader created successfully.")
            return shader
        except Exception as e:
            logger.error(f"Error creating Holographic Shader: {e}")
            raise

    @staticmethod
    def create_solar_fire_shader(nodes, node_links, color_primary):
        """Create Solar Fire shader."""
        try:
            color_primary = ShaderManager.convert_to_tuple(color_primary)

            mix = nodes.new('ShaderNodeMixShader')
            emission1 = nodes.new('ShaderNodeEmission')
            emission2 = nodes.new('ShaderNodeEmission')
            noise = nodes.new('ShaderNodeTexNoise')

            noise.inputs['Scale'].default_value = 10.0
            emission1.inputs['Color'].default_value = color_primary
            emission1.inputs['Strength'].default_value = 3.0
            emission2.inputs['Color'].default_value = (1.0, 0.5, 0.0, 1.0)
            emission2.inputs['Strength'].default_value = 5.0

            mix.inputs[0].default_value = 0.5
            node_links.new(noise.outputs[0], mix.inputs[0])
            node_links.new(emission1.outputs[0], mix.inputs[1])
            node_links.new(emission2.outputs[0], mix.inputs[2])

            logger.debug("Solar Fire Shader created successfully.")
            return mix
        except Exception as e:
            logger.error(f"Error creating Solar Fire Shader: {e}")
            raise

    @staticmethod
    def create_inferno_shader(nodes, node_links, color_primary):
        """Create Inferno shader."""
        try:
            color_primary = ShaderManager.convert_to_tuple(color_primary)

            mix = nodes.new('ShaderNodeMixShader')
            principled = nodes.new('ShaderNodeBsdfPrincipled')
            emission = nodes.new('ShaderNodeEmission')
            noise = nodes.new('ShaderNodeTexNoise')

            noise.inputs['Scale'].default_value = 15.0
            principled.inputs['Base Color'].default_value = (0.8, 0.3, 0.1, 1.0)
            principled.inputs['Metallic'].default_value = 0.2
            principled.inputs['Roughness'].default_value = 0.7
            emission.inputs['Color'].default_value = (1.0, 0.2, 0.0, 1.0)
            emission.inputs['Strength'].default_value = 8.0

            mix.inputs[0].default_value = 0.6
            node_links.new(noise.outputs[0], mix.inputs[0])
            node_links.new(principled.outputs[0], mix.inputs[1])
            node_links.new(emission.outputs[0], mix.inputs[2])

            logger.debug("Inferno Shader created successfully.")
            return mix
        except Exception as e:
            logger.error(f"Error creating Inferno Shader: {e}")
            raise
