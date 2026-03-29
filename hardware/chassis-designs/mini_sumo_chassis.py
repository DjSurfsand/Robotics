# Mini Sumo Robot Chassis - Blender Python Script
# Run this in Blender: File → Run Script OR blender --background --python mini_sumo_chassis.py
#
# Mini Sumo specs: Max 10x10cm, Max 500g
# This creates a basic wedge-shaped chassis optimized for sumo wrestling

import bpy
import math

# Clear existing mesh objects
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        bpy.data.objects.remove(obj, do_unlink=True)

# ============== CHASSIS PARAMETERS ==============
CHASSIS_LENGTH = 9.8      # cm (must be < 10cm)
CHASSIS_WIDTH = 9.8        # cm (must be < 10cm)
CHASSIS_HEIGHT_REAR = 4.0  # cm
CHASSIS_HEIGHT_FRONT = 1.5 # cm (wedge shape for lifting opponent)
WALL_THICKNESS = 0.3       # cm (3mm for 3D printing)
BOTTOM_THICKNESS = 0.4     # cm (4mm for strength)
# ================================================

print(f"Creating Mini Sumo Chassis: {CHASSIS_LENGTH}x{CHASSIS_WIDTH}cm")

# Create main chassis body (wedge shape)
verts = [
    # Bottom face (on ground)
    (0, 0, 0),
    (CHASSIS_LENGTH, 0, 0),
    (CHASSIS_LENGTH, CHASSIS_WIDTH, 0),
    (0, CHASSIS_WIDTH, 0),
    
    # Top face (angled wedge)
    (0, 0, CHASSIS_HEIGHT_REAR),
    (CHASSIS_LENGTH, 0, CHASSIS_HEIGHT_FRONT),
    (CHASSIS_LENGTH, CHASSIS_WIDTH, CHASSIS_HEIGHT_FRONT),
    (0, CHASSIS_WIDTH, CHASSIS_HEIGHT_REAR),
]

edges = [
    # Bottom edges
    (0, 1), (1, 2), (2, 3), (3, 0),
    # Top edges
    (4, 5), (5, 6), (6, 7), (7, 4),
    # Vertical edges
    (0, 4), (1, 5), (2, 6), (3, 7),
]

faces = [
    # Bottom face
    (0, 1, 2, 3),
    # Top face (wedge surface)
    (4, 7, 6, 5),
    # Front face (low)
    (1, 0, 4, 5),
    # Back face (high)
    (2, 1, 5, 6),
    # Left face (angled)
    (3, 2, 6, 7),
    # Right face (angled)
    (0, 3, 7, 4),
]

mesh = bpy.data.meshes.new("chassis_mesh")
mesh.from_py_vertices(verts, edges, faces)
mesh.update(calc_edges=True, calc_edges_crease=False)

obj = bpy.data.objects.new("MiniSumo_Chassis", mesh)
bpy.context.collection.objects.link(obj)

# Apply solidify modifier for walls (creates hollow structure)
modifier = obj.modifiers.new(name="Solidify", type='SOLIDIFY')
modifier.thickness = -WALL_THICKNESS  # Negative = inward
modifier.offset = 0.5  # Center thickness
modifier.thickness_astype = 'THICKNESS'

# Add bevel for smoother 3D printing
bevel = obj.modifiers.new(name="Bevel", type='BEVEL')
bevel.width = 0.1
bevel.segments = 2
bevel.limit_method = 'ANGLE'
bevel.angle_limit = math.radians(30)

# ============== MOTOR MOUNTS ==============
# Create 4 motor mount positions (2 per side for tank drive)
motor_diameter = 2.0  # cm (N20 motor size)
motor_height = 2.5    # cm

def create_motor_mount(x, y, name):
    """Create a cylindrical motor mount hole"""
    cyl_verts = []
    cyl_faces = []
    segments = 16
    
    for i in range(segments):
        angle = (i / segments) * 2 * math.pi
        rx = math.cos(angle) * (motor_diameter / 2)
        ry = math.sin(angle) * (motor_diameter / 2)
        cyl_verts.append((x + rx, y + ry, 0.5))
        cyl_verts.append((x + rx, y + ry, motor_height))
    
    for i in range(segments):
        idx = i * 2
        next_idx = ((i + 1) % segments) * 2
        cyl_faces.append((idx, next_idx, next_idx + 1, idx + 1))
    
    return cyl_verts, cyl_faces

all_verts = list(mesh.vertices)
all_faces = list(mesh.polygons)

# Front-left motor mount
ml_x, ml_y = 2.0, 2.0
# Front-right motor mount  
mr_x, mr_y = 2.0, CHASSIS_WIDTH - 2.0
# Rear-left motor mount
rl_x, rl_y = CHASSIS_LENGTH - 2.0, 2.0
# Rear-right motor mount
rr_x, rr_y = CHASSIS_LENGTH - 2.0, CHASSIS_WIDTH - 2.0

print("Motor mount positions:")
print(f"  Front-Left:  ({ml_x}, {ml_y})")
print(f"  Front-Right: ({mr_x}, {mr_y})")
print(f"  Rear-Left:   ({rl_x}, {rl_y})")
print(f"  Rear-Right:  ({rr_x}, {rr_y})")

# ============== SENSOR MOUNTS ==============
# IR sensor positions around the perimeter
sensor_positions = [
    (CHASSIS_LENGTH - 0.5, CHASSIS_WIDTH / 2, "Front_Center"),
    (CHASSIS_LENGTH - 0.5, 0.5, "Front_Left"),
    (CHASSIS_LENGTH - 0.5, CHASSIS_WIDTH - 0.5, "Front_Right"),
    (0.5, 0.5, "Rear_Left"),
    (0.5, CHASSIS_WIDTH - 0.5, "Rear_Right"),
    (CHASSIS_LENGTH / 2, 0.3, "Left_Center"),
    (CHASSIS_LENGTH / 2, CHASSIS_WIDTH - 0.3, "Right_Center"),
]

for x, y, name in sensor_positions:
    # Create small cylinder for sensor mount
    cyl = bpy.data.meshes.new(f"{name}_sensor")
    uv_cyl = bpy.ops.mesh.primitive_cylinder_add(
        radius=0.3,
        depth=0.5,
        location=(x, y, CHASSIS_HEIGHT_FRONT + 0.2)
    )
    sensor_obj = bpy.context.active_object
    sensor_obj.name = f"{name}_Mount"
    
print(f"Created {len(sensor_positions)} sensor mount positions")

# ============== WEIGHT DISTRIBUTION MARKERS ==============
# Add visual markers for battery placement (center of gravity)
battery_loc = (CHASSIS_LENGTH / 2, CHASSIS_WIDTH / 2, 0.6)
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=battery_loc
)
battery = bpy.context.active_object
battery.name = "Battery_Position_CoG"
battery.scale = (2.5, 1.8, 0.8)  # Approximate battery size

# ============== RENDER SETTINGS ==============
# Set up a simple material for visualization
mat = bpy.data.materials.new(name="Chassis_Material")
mat.use_nodes = True
bsdf = mat.node_tree.nodes["Principled BSDF"]
bsdf.inputs["Base Color"].default_value = (0.2, 0.5, 0.8, 1.0)  # Blue
bsdf.inputs["Metallic"].default_value = 0.3
bsdf.inputs["Roughness"].default_value = 0.7

obj.data.materials.append(mat)

# ============== EXPORT SETTINGS ==============
print("\n" + "="*50)
print("CHASSIS CREATED SUCCESSFULLY!")
print("="*50)
print(f"Dimensions: {CHASSIS_LENGTH} x {CHASSIS_WIDTH} x {CHASSIS_HEIGHT_REAR} cm")
print(f"Wedge angle: Front height {CHASSIS_HEIGHT_FRONT}cm, Rear height {CHASSIS_HEIGHT_REAR}cm")
print(f"Wall thickness: {WALL_THICKNESS}cm")
print(f"Estimated weight: ~80-120g (PLA, hollow)")
print("\nTo export as STL for 3D printing:")
print("  Select 'MiniSumo_Chassis' object")
print("  File → Export → STL (.stl)")
print("  Or run: bpy.ops.export_mesh.stl(filepath='chassis.stl')")
print("="*50)

# Select the chassis
bpy.context.view_layer.objects.active = obj
obj.select_set(True)
