import math
import random
import bpy
import sys
import os

# Add the directory containing planetShaders.py to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from planetShaders import PlanetShaders, register

def create_sphere(location, radius=0.5):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=location, segments=32, ring_count=16)
    sphere = bpy.context.active_object

    # Add subdivision surface modifier
    subsurf = sphere.modifiers.new(name="Subsurf", type='SUBSURF')
    subsurf.levels = 2
    subsurf.render_levels = 3

    return sphere

def animate_spheres_worm(spheres):
    frames = 300
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
                math.sin(delayed_frame * 0.15) * 0.7,
                math.cos(delayed_frame * 0.12) * 0.7,
                t * math.pi * 2
            )
            sphere.keyframe_insert(data_path="rotation_euler", frame=frame)

            # Add scale animation
            scale = 1 + math.sin(delayed_frame * 0.2) * 0.2
            sphere.scale = (scale, scale, scale)
            sphere.keyframe_insert(data_path="scale", frame=frame)

def main():
    print("Executing enhanced spheres animations...")

    # Register planet shader property
    register()

    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # Create spheres with varying sizes
    spheres = []
    num_spheres = 15
    for i in range(num_spheres):
        radius = 0.25 + random.random() * 0.15
        sphere = create_sphere(location=(i * -1, 0, 2), radius=radius)

        # Assign different planet shaders
        shader_types = list(PlanetShaders.create_shader_collection().keys())
        if shader_types:
            sphere["planet_shader"] = random.choice(shader_types)

        # Apply the shader
        PlanetShaders.apply_shader(sphere)

        spheres.append(sphere)

    animate_spheres_worm(spheres)

    # Enhanced render settings
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.samples = 256
    bpy.context.scene.cycles.use_denoising = True

    # Set world background to dark
    world = bpy.context.scene.world
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs[0].default_value = (0.01, 0.01, 0.02, 1)
    world.node_tree.nodes["Background"].inputs[1].default_value = 1.0

    # Debug: Print sphere positions and visibility
    scene = bpy.context.scene
    for frame in range(scene.frame_start, scene.frame_end + 1):
        scene.frame_set(frame)
        print(f"Frame {frame}:")
        for sphere in spheres:
            print(f"Sphere {sphere.name}: Location {sphere.location}, Visible {sphere.visible_get()}")

    print("Enhanced spheres animation completed.")

if __name__ == "__main__":
    main()
