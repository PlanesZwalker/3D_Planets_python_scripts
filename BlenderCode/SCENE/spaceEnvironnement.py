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
        bpy.ops.mesh.primitive_uv_sphere_add(radius=150 + i * 20)
        stars = bpy.context.active_object
        stars.name = f'Deep_Space_Stars_{i}'

        mat = bpy.data.materials.new(name=f"Star_Field_{i}")
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()

        emission = nodes.new('ShaderNodeEmission')
        voronoi = nodes.new('ShaderNodeTexVoronoi')
        color_ramp = nodes.new('ShaderNodeValToRGB')
        output = nodes.new('ShaderNodeOutputMaterial')

        # Ultra-fine star settings
        voronoi.inputs['Scale'].default_value = 3000.0 + i * 500

        # Extreme contrast for stars
        color_ramp.color_ramp.elements[0].position = 0.999
        color_ramp.color_ramp.elements[0].color = (0, 0, 0, 1)
        color_ramp.color_ramp.elements[1].position = 1.0
        color_ramp.color_ramp.elements[1].color = (0.2, 0.2, 0.3, 1)

        emission.inputs['Strength'].default_value = 2.0 - (i * 0.5)

        links.new(voronoi.outputs['Distance'], color_ramp.inputs['Fac'])
        links.new(color_ramp.outputs['Color'], emission.inputs['Color'])
        links.new(emission.outputs['Emission'], output.inputs['Surface'])

        stars.data.materials.append(mat)


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
