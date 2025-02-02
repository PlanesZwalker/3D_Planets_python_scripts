import json
from typing import Dict
from dataclasses import dataclass

@dataclass(frozen=True)
class ShaderConfig:
    name: str
    noise_scale: float
    noise_detail: float
    color_primary: tuple
    color_secondary: tuple
    shader_type: str

class ShaderConfigLoader:
    @staticmethod
    def load_config(config_path: str = 'planet_shader_config.json') -> Dict[str, ShaderConfig]:
        try:
            with open(config_path, 'r') as file:
                configs = json.load(file)

            shader_configs = {}
            for name, config in configs.items():
                shader_configs[name] = ShaderConfig(
                    name=name,
                    noise_scale=config.get('noise_scale', 10.0),
                    noise_detail=config.get('noise_detail', 15.0),
                    color_primary=tuple(config.get('color_primary', [0.1, 0.3, 0.7])),
                    color_secondary=tuple(config.get('color_secondary', [0.3, 0.6, 0.8])),
                    shader_type=config.get('shader_type', 'principled')
                )
            return shader_configs
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"Error loading configuration file {config_path}. Using default configurations.")
            return {}
