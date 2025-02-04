import importlib.util
import sys
import logging
from pathlib import Path

# Setup logging for debugging
logging.basicConfig(level=logging.DEBUG)

# Define paths
blender_python_path = r"C:\Program Files\Blender Foundation\Blender 4.3\4.3\python\bin"  # Update this if needed
base_dir = Path("C:/3D_Planets_python_scripts/BlenderCode/SCENE")  # Update this path as needed
venv_site_packages = Path("C:/3D_Planets_python_scripts/.venv/Lib/site-packages")

# Add necessary paths to sys.path
sys.path.insert(0, str(base_dir))  # Ensure SCENE directory is accessible
sys.path.insert(0, blender_python_path)  # Blender's Python
sys.path.insert(0, str(venv_site_packages))  # Virtual environment

# Debugging output
logging.debug(f"sys.path: {sys.path}")

def execute_mains():
    """Load and execute scripts in a specific order."""
    files_to_execute = [
        'MeshesSetups/citySphere.py',
        'CamerasSetups/cameraAnimations.py',
        'LightingsSetups/cityLighting.py',
        'EnvironnementsSetups/spaceEnvironnement.py',
        'Utils/organizeHierarchie.py',
        'ShadersPlanets/shaderPanel.py',
    ]

    if not base_dir.exists():
        logging.error(f"Error: The directory {base_dir} does not exist.")
        return  # Stop execution if the directory is invalid

    for script_name in files_to_execute:
        script_path = base_dir / script_name

        if not script_path.exists():
            logging.error(f"Error: The script {script_path} does not exist.")
            continue  # Skip to the next script if the current one doesn't exist

        logging.info(f'Loading {script_name}')

        # Convert path to module format (e.g., "ShadersPlanets.shaderPanel")
        module_name = script_name.replace("/", ".").replace("\\", ".")[:-3]

        try:
            spec = importlib.util.spec_from_file_location(module_name, str(script_path))
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Execute main() if it exists
            if hasattr(module, 'main'):
                logging.info(f'Executing main() from {script_name}')
                module.main()
            else:
                logging.warning(f"Warning: {script_name} does not have a main() function.")
        except Exception as e:
            logging.error(f"Error executing {script_name}: {str(e)}")

if __name__ == "__main__":
    execute_mains()
