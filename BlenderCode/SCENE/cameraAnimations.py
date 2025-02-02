import bpy
from mathutils import Vector
from math import sin, cos, pi

def create_camera(name, location, lens=35):
    """Creates a camera with specific settings and returns it"""
    bpy.ops.object.camera_add(location=location)
    camera = bpy.context.active_object
    camera.name = name
    camera.data.lens = lens

    # Set up depth of field if available
    if hasattr(camera.data, 'dof'):
        camera.data.dof.use_dof = False  # Disable depth of field to avoid blurriness

    return camera

def setup_main_camera(frame_start, frame_end):
    """Sets up the main tracking camera with smooth movement"""
    main_cam = create_camera("MainCamera", (0, -15, 8))

    # Create target for camera to track
    bpy.ops.object.empty_add(type='PLAIN_AXES')
    focus_target = bpy.context.active_object
    focus_target.name = "CameraTarget"

    # Set up tracking constraint
    track = main_cam.constraints.new(type='TRACK_TO')
    track.target = focus_target
    track.track_axis = 'TRACK_NEGATIVE_Z'
    track.up_axis = 'UP_Y'

    # Animate camera and target
    for frame in range(frame_start, frame_end + 1):
        t = (frame - frame_start) / (frame_end - frame_start)

        # Camera movement
        main_cam.location = (
            t * 25.0 - 5 + sin(t * 2 * pi) * 3,  # X: Follow movement with wave
            -15 + sin(t * pi) * 5,               # Y: Gentle sway
            8 + sin(t * 4 * pi) * 2              # Z: Slight up/down motion
        )

        # Target movement
        focus_target.location = (
            t * 25.0,                            # X: Follow main movement
            sin(t * 2 * pi) * 2,                 # Y: Smooth weaving
            2 + sin(t * 3 * pi)                  # Z: Height variation
        )

        # Insert keyframes
        main_cam.keyframe_insert(data_path="location", frame=frame)
        focus_target.keyframe_insert(data_path="location", frame=frame)

        # Animate focal length for dynamic shots
        main_cam.data.lens = 35 + sin(t * 2 * pi) * 15
        main_cam.data.keyframe_insert(data_path="lens", frame=frame)

    # Ensure looping by matching the first and last frames
    main_cam.location = (0, -15, 8)
    focus_target.location = (0, 0, 2)
    main_cam.data.lens = 35
    main_cam.keyframe_insert(data_path="location", frame=frame_end)
    focus_target.keyframe_insert(data_path="location", frame=frame_end)
    main_cam.data.keyframe_insert(data_path="lens", frame=frame_end)

    return main_cam

def setup_orbit_camera(frame_start, frame_end):
    """Sets up an orbiting camera for sweeping shots"""
    orbit_cam = create_camera("OrbitCamera", (0, -10, 5), lens=50)

    for frame in range(frame_start, frame_end + 1):
        t = (frame - frame_start) / (frame_end - frame_start)

        # Smooth spiral orbit movement
        radius = 15 + sin(t * 2 * pi) * 5
        angle = t * 2 * pi  # Slower orbit for smoother movement
        height = 5 + sin(t * pi) * 3

        # Calculate position
        orbit_cam.location = (
            radius * cos(angle),
            radius * sin(angle),
            height
        )

        # Point camera at the action
        look_at = Vector((t * 25.0, 0, 2))
        direction = look_at - Vector(orbit_cam.location)
        rot_quat = direction.to_track_quat('-Z', 'Y')
        orbit_cam.rotation_euler = rot_quat.to_euler()

        # Insert keyframes
        orbit_cam.keyframe_insert(data_path="location", frame=frame)
        orbit_cam.keyframe_insert(data_path="rotation_euler", frame=frame)

    # Ensure looping by matching the first and last frames
    orbit_cam.location = (0, -10, 5)
    orbit_cam.rotation_euler = (0, 0, 0)
    orbit_cam.keyframe_insert(data_path="location", frame=frame_end)
    orbit_cam.keyframe_insert(data_path="rotation_euler", frame=frame_end)

    return orbit_cam

def setup_cameras(spheres):
    """Main function to set up all cameras and bind them to markers"""
    # Clear existing cameras
    for obj in bpy.data.objects:
        if obj.type == 'CAMERA':
            bpy.data.objects.remove(obj, do_unlink=True)

    # Scene settings
    scene = bpy.context.scene
    frame_start = 1
    frame_end = 250
    scene.frame_start = frame_start
    scene.frame_end = frame_end

    # Create cameras
    main_cam = setup_main_camera(frame_start, frame_end)
    orbit_cam = setup_orbit_camera(frame_start, frame_end)

    # Clear existing markers
    scene.timeline_markers.clear()

    # Create markers for camera switching
    markers = [
        (1, main_cam, "Main View"),
        (60, orbit_cam, "Orbit Shot"),
        (180, orbit_cam, "Return to Orbit"),
        (220, main_cam, "Final View")
    ]

    # Set up markers and bind cameras
    for frame, camera, name in markers:
        marker = scene.timeline_markers.new(name=name, frame=frame)
        marker.camera = camera

        # Set the scene's active camera at each marker
        scene.frame_set(frame)
        scene.camera = camera

    # Return to frame 1
    scene.frame_set(1)
    scene.camera = main_cam

    # Set up render properties
    scene.render.fps = 24

    # Debug: Print camera and sphere positions at frame 128
    scene.frame_set(128)
    print(f"Frame 128:")
    print(f"MainCamera Location: {main_cam.location}, Rotation: {main_cam.rotation_euler}, Lens: {main_cam.data.lens}")
    print(f"OrbitCamera Location: {orbit_cam.location}, Rotation: {orbit_cam.rotation_euler}, Lens: {orbit_cam.data.lens}")
    for sphere in spheres:
        print(f"Sphere {sphere.name}: Location {sphere.location}, Visible {sphere.visible_get()}")

    return main_cam, orbit_cam

def main():
    print("Setting up enhanced camera system...")

    # Get all planet objects in the scene
    spheres = [obj for obj in bpy.data.objects if obj.type == 'MESH']

    cameras = setup_cameras(spheres)
    print("Camera setup completed successfully.")

if __name__ == "__main__":
    main()
