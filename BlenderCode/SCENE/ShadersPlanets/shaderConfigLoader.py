import json
import os
from dataclasses import dataclass
from typing import Dict

@dataclass(frozen=True)
class ShaderConfig:
    name: str
    noise_scale: float
    noise_detail: float
    noise_roughness: float
    noise_distortion: float
    color_mix_factor: float
    color_primary: tuple
    color_secondary: tuple
    roughness: float
    metallic: float
    emission_strength: float
    shader_type: str
    description: str


class ShaderConfigLoader:
    @staticmethod
    def load_config(config_path: str = None) -> Dict[str, ShaderConfig]:
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), 'shader_planet_config.json')

        try:
            with open(config_path, 'r') as file:
                configs = json.load(file)

            shader_configs = {}
            for name, config in configs.items():
                # Ensure all required fields are included with default values where necessary
                shader_configs[name] = ShaderConfig(
                    name=name,
                    noise_scale=config.get('noise_scale', 10.0),
                    noise_detail=config.get('noise_detail', 15.0),
                    noise_roughness=config.get('noise_roughness', 0.5),  # Default to 0.5 if not provided
                    noise_distortion=config.get('noise_distortion', 0.0),  # Default to 0.0 if not provided
                    color_mix_factor=config.get('color_mix_factor', 0.5),  # Default to 0.5 if not provided
                    color_primary=tuple(config.get('color_primary', [0.1, 0.3, 0.7])),
                    color_secondary=tuple(config.get('color_secondary', [0.3, 0.6, 0.8])),
                    roughness=config.get('roughness', 0.5),  # Default to 0.5 if not provided
                    metallic=config.get('metallic', 0.5),    # Default to 0.5 if not provided
                    emission_strength=config.get('emission_strength', 1.0),  # Default to 1.0 if not provided
                    shader_type=config.get('shader_type', 'principled'),
                    description=config.get('description', 'No description available.')
                )
            return shader_configs
        except FileNotFoundError as e:
            print(f"Error: The configuration file {config_path} was not found.")
            print(str(e))
            return {}  # Return empty dictionary when file is not found
        except json.JSONDecodeError as e:
            print(f"Error: Failed to decode the JSON configuration file {config_path}.")
            print(str(e))
            return {}  # Return empty dictionary when JSON decoding fails
