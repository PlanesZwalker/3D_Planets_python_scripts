import math
import random
import bpy
from mathutils import Color

def create_volumetric_atmosphere():
    """Creates a volumetric atmosphere in the world settings for enhanced depth and atmosphere"""
    world = bpy.context.scene.world
    world.use_nodes = True
    nodes = world.node_tree.nodes
    links = world.node_tree.links

    # Clear existing nodes
    nodes.clear()

    # Create nodes for volumetric atmosphere
    background = nodes.new('ShaderNodeBackground')
    volume_scatter = nodes.new('ShaderNodeVolumeScatter')
    volume_absorption = nodes.new('ShaderNodeVolumeAbsorption')
    add_shader = nodes.new('ShaderNodeAddShader')
    output = nodes.new('ShaderNodeOutputWorld')

    # Set up background
    background.inputs['Color'].default_value = (0.01, 0.01, 0.02, 1)
    background.inputs['Strength'].default_value = 0.5

    # Set up volume scatter for atmosphere
    volume_scatter.inputs['Color'].default_value = (0.3, 0.4, 0.6, 1)
    volume_scatter.inputs['Density'].default_value = 0.01
    volume_scatter.inputs['Anisotropy'].default_value = 0.3

    # Set up volume absorption
    volume_absorption.inputs['Color'].default_value = (0.8, 0.9, 1.0, 1)
    volume_absorption.inputs['Density'].default_value = 0.01

    # Link nodes
    links.new(background.outputs['Background'], output.inputs['Surface'])
    links.new(add_shader.outputs['Shader'], output.inputs['Volume'])
    links.new(volume_scatter.outputs['Volume'], add_shader.inputs[0])
    links.new(volume_absorption.outputs['Volume'], add_shader.inputs[1])

def create_rim_light(target_object, intensity=2.0, color=(1.0, 0.6, 0.3, 1.0)):
    """Creates a rim light to highlight the edges of planets"""
    bpy.ops.object.light_add(type='AREA', location=(3, -3, 0))
    rim_light = bpy.context.active_object
    rim_light.data.energy = intensity * 100
    rim_light.data.color = color[:3]
    rim_light.data.shape = 'DISK'
    rim_light.data.size = 5

    # Create track-to constraint to always point at the planet
    constraint = rim_light.constraints.new('TRACK_TO')
    constraint.target = target_object
    constraint.track_axis = 'TRACK_NEGATIVE_Z'
    constraint.up_axis = 'UP_Y'

    return rim_light

def setup_enhanced_lighting():
    """Sets up an enhanced lighting system with a controlled number of light sources."""
    # Ensure we have a world
    if not bpy.data.worlds:
        world = bpy.data.worlds.new("World")
        bpy.context.scene.world = world

    # Create volumetric atmosphere
    create_volumetric_atmosphere()

    # Create main directional light (sun)
    bpy.ops.object.light_add(type='SUN', location=(10, 10, 20))
    sun = bpy.context.active_object
    sun.data.energy = 5.0
    sun.data.color = (1, 0.95, 0.9)  # Warm sunlight
    sun.data.angle = 0.1  # Softer shadows

    # Create a fill light (blue-tinted)
    bpy.ops.object.light_add(type='SUN', location=(-10, -10, 10))
    fill_light = bpy.context.active_object
    fill_light.data.energy = 2.0
    fill_light.data.color = (0.7, 0.8, 1.0)  # Cool fill light
    fill_light.data.angle = 0.3

    # Limit the number of area lights to 2 or 3
    area_lights_count = 2  # Change this number to control the number of area lights

    for _ in range(area_lights_count):
        bpy.ops.object.light_add(type='AREA', location=(0, 0, 15))
        area_light = bpy.context.active_object
        area_light.data.energy = 300.0
        area_light.data.color = (1, 1, 1)
        area_light.scale = (15, 15, 15)
        area_light.data.spread = 90  # Wide spread for soft lighting

    # Create animated point lights for dynamic lighting
    lights = []
    num_point_lights = 3  # Limiting the number of point lights to 3
    for i in range(num_point_lights):
        bpy.ops.object.light_add(type='POINT', location=(random.uniform(-10, 10),
                                                         random.uniform(-10, 10),
                                                         random.uniform(5, 15)))
        point_light = bpy.context.active_object
        point_light.data.energy = random.uniform(100, 300)

        # Create random color for point light
        hue = random.random()
        color = Color()
        color.hsv = (hue, 0.8, 1.0)
        point_light.data.color = (color.r, color.g, color.b)

        # Add animation
        point_light.animation_data_create()
        frames = 250

        for frame in range(frames):
            # Orbital motion
            angle = (frame / frames) * 2 * math.pi
            radius = 5 + math.sin(frame * 0.1) * 2
            x = math.cos(angle) * radius
            y = math.sin(angle) * radius
            z = 5 + math.sin(frame * 0.05) * 3

            point_light.location = (x, y, z)
            point_light.keyframe_insert(data_path="location", frame=frame)

            # Animate energy/intensity
            point_light.data.energy = 200 + math.sin(frame * 0.1) * 100
            point_light.data.keyframe_insert(data_path="energy", frame=frame)

        lights.append(point_light)

    # Set up Cycles render settings for better lighting
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.samples = 256
    bpy.context.scene.cycles.use_denoising = True
    bpy.context.scene.cycles.caustics_reflective = True
    bpy.context.scene.cycles.caustics_refractive = True

    return {'sun': sun, 'fill': fill_light, 'area_lights': area_lights_count, 'point_lights': lights}


def apply_lighting_to_planets(planets):
    """Applies enhanced lighting effects to each planet"""
    for planet in planets:
        # Create rim light for each planet
        rim_light = create_rim_light(planet)

        # Add emission to planet material for subtle glow
        if planet.data.materials:
            material = planet.data.materials[0]
            if material.use_nodes:
                nodes = material.node_tree.nodes
                links = material.node_tree.links

                # Add subtle emission to existing shader
                emission = nodes.new('ShaderNodeEmission')
                emission.inputs['Color'].default_value = (1, 1, 1, 1)
                emission.inputs['Strength'].default_value = 0.1

                mix = nodes.new('ShaderNodeMixShader')
                mix.inputs['Fac'].default_value = 0.1

                # Get the existing output node
                output = None
                for node in nodes:
                    if node.type == 'OUTPUT_MATERIAL':
                        output = node
                        break

                if output:
                    # Store existing shader connection
                    existing_shader = output.inputs['Surface'].links[0].from_node

                    # Create new connections
                    links.new(existing_shader.outputs[0], mix.inputs[1])
                    links.new(emission.outputs[0], mix.inputs[2])
                    links.new(mix.outputs[0], output.inputs['Surface'])

def main():
    print("Setting up enhanced lighting system...")

    # Set up the main lighting
    lights = setup_enhanced_lighting()

    # Get all planet objects in the scene
    planets = [obj for obj in bpy.data.objects if obj.type == 'MESH']

    # Apply enhanced lighting to planets
    apply_lighting_to_planets(planets)

    print("Enhanced lighting setup completed successfully.")

if __name__ == "__main__":
    main()
