import importlib.util
from pathlib import Path
import sys

# Add Blender's Python path to the virtual environment
blender_python_path = r"C:\Program Files\Blender Foundation\Blender 4.3\4.3\python\bin"  # Update this path as needed
base_dir = Path("C:/3D_Planets_python_scripts/BlenderCode/SCENE")  # Update this path as needed

sys.path.append(blender_python_path)

def execute_mains():
    # Order of execution for your script files
    files_to_execute = [
        'citySphere.py',
        'cameraAnimations.py',
        'cityLighting.py',
        'spaceEnvironnement.py',
        'organizeHierarchie.py'
    ]

    # Ensure the base directory exists

    if not base_dir.exists():
        print(f"Error: The directory {base_dir} does not exist.")
        return  # Stop execution if the directory is invalid

    for script_name in files_to_execute:
        # Construct the full file path correctly
        script_path = base_dir / script_name

        if not script_path.exists():
            print(f"Error: The script {script_path} does not exist.")
            continue  # Skip to the next script if the current one doesn't exist

        print(f'Loading {script_name}')
        module_name = script_name[:-3]  # Remove the '.py' extension
        spec = importlib.util.spec_from_file_location(module_name, str(script_path))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Execute main() from the loaded script if available
        try:
            if hasattr(module, 'main'):
                print(f'Executing main() from {script_name}')
                module.main()
            else:
                print(f"Warning: {script_name} does not have a main() function.")
        except Exception as e:
            print(f"Error executing {script_name}: {str(e)}")


if __name__ == "__main__":
    execute_mains()
