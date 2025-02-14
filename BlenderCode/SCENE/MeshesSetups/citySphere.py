import math
import os
import random
import sys

import bpy

# Get the absolute path of the main SCENE folder
scene_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(scene_path)
print(scene_path)
# Import the PlanetShaders module (assumed to read shader_planet_config.json)
from ShadersPlanets.shaderPlanet import PlanetShaders, register as register_planet

def create_sphere(location, radius=0.5):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=location, segments=32, ring_count=16)
    sphere = bpy.context.active_object

    # Add subdivision surface modifier
    subsurf = sphere.modifiers.new(name="Subsurf", type='SUBSURF')
    subsurf.levels = 2
    subsurf.render_levels = 3

    return sphere


def animate_spheres_worm(spheres):
    frames = 250
    delay_frames = 4
    amplitude = 2.5
    frequency = 2.5

    for sphere_idx, sphere in enumerate(spheres):
        sphere.animation_data_create()

        for frame in range(frames):
            delayed_frame = frame - (sphere_idx * delay_frames)
            t = delayed_frame / frames

            # Enhanced motion path
            x = t * 25.0
            y = math.sin(delayed_frame * 0.1) * amplitude + math.cos(delayed_frame * 0.05) * (amplitude * 0.3)
            z = 2.0 + math.cos(delayed_frame * 0.1) * amplitude + math.sin(delayed_frame * 0.05) * (amplitude * 0.3)

            sphere.location = (x, y, z)
            sphere.keyframe_insert(data_path="location", frame=frame)

            # More complex rotation
            sphere.rotation_euler = (
                math.sin(delayed_frame * 0.15) * math.cos(delayed_frame * 0.12),
                math.cos(delayed_frame * 0.12) * math.sin(delayed_frame * 0.15),
                t * math.pi * 2
            )
            sphere.keyframe_insert(data_path="rotation_euler", frame=frame)

            # Add scale animation
            scale = 1 + math.sin(delayed_frame * 0.2) * math.cos(delayed_frame * 0.12)
            sphere.scale = (scale, scale, scale)
            sphere.keyframe_insert(data_path="scale", frame=frame)


def main():
    print("Executing enhanced spheres animations...")

    # Register planet shader property (this should be done only once at the start)
    register_planet()

    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # Get all available shader types defined in shader_planet_config.json via PlanetShaders
    shader_types = list(PlanetShaders.create_shader_collection().keys())
    num_shaders = len(shader_types)
    print(f"Found {num_shaders} shader(s): {shader_types}")

    # Create spheres with unique shaders (one per shader)
    spheres = []
    for i, shader_name in enumerate(shader_types):
        radius = 0.25 + random.random() * 0.15
        # Space spheres along the X-axis so each is visible
        sphere = create_sphere(location=(i * 2.0, 0, 2), radius=radius)

        # Save shader name in sphere's custom property
        sphere["planet_shader"] = shader_name

        # Apply the corresponding shader to the sphere
        PlanetShaders.apply_shader(sphere, shader_name)
        spheres.append(sphere)

    animate_spheres_worm(spheres)

    # Enhanced render settings
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.samples = 256
    bpy.context.scene.cycles.use_denoising = True

    # Set world background to dark (RGBA format)
    world = bpy.context.scene.world
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs[0].default_value = (0.01, 0.01, 0.02, 1)
    world.node_tree.nodes["Background"].inputs[1].default_value = 1.0

    # For debug: cycle through frames and print positions
    scene = bpy.context.scene
    for frame in range(scene.frame_start, scene.frame_end + 1):
        scene.frame_set(frame)
        print(f"Frame {frame}:")

    print("Enhanced spheres animation completed.")


if __name__ == "__main__":
    main()
