import bpy
import math

def create_milky_way_core():
    world = bpy.context.scene.world
    world.use_nodes = True
    nodes = world.node_tree.nodes
    links = world.node_tree.links

    nodes.clear()

    # Create nodes for deep space effect
    output = nodes.new('ShaderNodeOutputWorld')
    background = nodes.new('ShaderNodeBackground')

    # Set pure black background
    background.inputs['Color'].default_value = (0.001, 0.001, 0.002, 1)
    background.inputs['Strength'].default_value = 0.5

    # Connect to output
    links.new(background.outputs['Background'], output.inputs['Surface'])


def create_dense_starfield():
    for i in range(3):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=150 + i * 20)  # Create the stars
        stars = bpy.context.active_object  # Get the active object (newly created sphere)
        stars.name = f'Deep_Space_Stars_{i}'  # Set name for the stars

        # Create new material and use nodes
        mat = bpy.data.materials.new(name=f"Star_Field_{i}")
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()  # Clear any existing nodes

        # Create shader nodes
        emission = nodes.new('ShaderNodeEmission')  # Emission Shader
        voronoi = nodes.new('ShaderNodeTexVoronoi')  # Voronoi texture for starfield texture
        color_ramp = nodes.new('ShaderNodeValToRGB')  # Color Ramp for contrast
        output = nodes.new('ShaderNodeOutputMaterial')  # Output Material Node

        # Set up Voronoi texture properties
        voronoi.inputs['Scale'].default_value = 3000.0 + i * 500  # Fine-tune the star field

        # Set up Color Ramp properties for extreme contrast
        color_ramp.color_ramp.elements[0].position = 0.999
        color_ramp.color_ramp.elements[0].color = (0, 0, 0, 1)  # Black (Space Background)
        color_ramp.color_ramp.elements[1].position = 1.0
        color_ramp.color_ramp.elements[1].color = (0.2, 0.2, 0.3, 1)  # Blueish Star Color

        # Set up emission strength based on the sphere index (for variation)
        emission.inputs['Strength'].default_value = 2.0 - (i * 0.5)

        # Add checks before making links
        if 'Distance' in voronoi.outputs and 'Fac' in color_ramp.inputs:
            links.new(voronoi.outputs['Distance'], color_ramp.inputs['Fac'])  # Voronoi texture to Color Ramp
        else:
            print(f"Warning: Cannot link Voronoi and Color Ramp for material {i}.")

        if 'Color' in color_ramp.outputs and 'Color' in emission.inputs:
            links.new(color_ramp.outputs['Color'], emission.inputs['Color'])  # Color Ramp to Emission Shader
        else:
            print(f"Warning: Cannot link Color Ramp and Emission for material {i}.")

        if 'Emission' in emission.outputs and 'Emission' in output.inputs:
            links.new(emission.outputs['Emission'], output.inputs['Emission'])  # Emission Shader to Output Material
        else:
            print(f"Warning: Cannot link Emission Shader and Output Material for material {i}.")

        # Apply the material to the star object
        stars.data.materials.append(mat)  # Add the material to the star object

        # Debugging: Log the connections for confirmation
        print(f"Starfield Material {i} created and linked successfully.")



def setup_camera_view():
    if 'MainCamera' not in bpy.data.objects:
        bpy.ops.object.camera_add()
    camera = bpy.data.objects['MainCamera']
    camera.location = (0, -10, 2)
    camera.rotation_euler = (math.radians(80), 0, 0)
    bpy.context.scene.camera = camera


def main():
    print("Creating deep space environment...")

    create_milky_way_core()
    create_dense_starfield()
    setup_camera_view()

    # Optimized render settings for dark space
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.samples = 512
    bpy.context.scene.cycles.use_denoising = True

    print("Deep space environment completed.")


if __name__ == "__main__":
    main()
