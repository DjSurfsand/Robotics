# Mini Sumo Robot Chassis - Blender Python Script
# Run: blender --background --python mini_sumo_chassis.py
#
# Mini Sumo specs: Max 10x10cm, Max 500g
# Creates a wedge-shaped chassis optimized for sumo wrestling

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

# Create main chassis body using Blender's primitive and modifiers
# Start with a cube and scale/modify it
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
chassis = bpy.context.active_object
chassis.name = "MiniSumo_Chassis"

# Scale to chassis dimensions (centered at origin)
chassis.scale = (CHASSIS_LENGTH/2, CHASSIS_WIDTH/2, CHASSIS_HEIGHT_REAR/2)
chassis.location = (CHASSIS_LENGTH/2 - 1, CHASSIS_WIDTH/2 - 1, CHASSIS_HEIGHT_REAR/2)

# Apply scale to make transformations work correctly
import bpy
bpy.context.view_layer.objects.active = chassis
bpy.ops.object.transform_apply(scale=True, location=False, rotation=False)

# Now we need to create the wedge shape by manipulating vertices
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')

# Get the front-top vertices and lower them to create wedge
# Vertices 4,5,6,7 are the front/top in default cube
for vert in chassis.data.vertices:
    coord = vert.co
    # Lower front vertices (higher X values)
    if coord[0] > CHASSIS_LENGTH * 0.7:  # Front portion
        vert.co[2] = CHASSIS_HEIGHT_FRONT

bpy.ops.object.mode_set(mode='OBJECT')

# Add solidify modifier for hollow walls
modifier = chassis.modifiers.new(name="Solidify", type='SOLIDIFY')
modifier.thickness = -WALL_THICKNESS  # Negative = inward
modifier.offset = 0.5  # Center thickness

# Add bevel for smoother 3D printing
bevel = chassis.modifiers.new(name="Bevel", type='BEVEL')
bevel.width = 0.1
bevel.segments = 2
bevel.limit_method = 'ANGLE'
bevel.angle_limit = math.radians(30)

# ============== MOTOR MOUNTS ==============
# Create cylindrical cutouts for motor positions
motor_diameter = 2.0  # cm (N20 motor size)
motor_height = 2.5    # cm

def create_motor_hole(x, y, z, radius, depth, name):
    """Create a cylinder for boolean cutout"""
    bpy.ops.mesh.primitive_cylinder_add(
        radius=radius,
        depth=depth,
        location=(x, y, z)
    )
    hole = bpy.context.active_object
    hole.name = f"{name}_Hole"
    return hole

# Motor positions (2 front, 2 rear for tank drive)
ml_pos = (2.0, 2.0, BOTTOM_THICKNESS + motor_diameter/2)
mr_pos = (2.0, CHASSIS_WIDTH - 2.0, BOTTOM_THICKNESS + motor_diameter/2)
rl_pos = (CHASSIS_LENGTH - 2.0, 2.0, BOTTOM_THICKNESS + motor_diameter/2)
rr_pos = (CHASSIS_LENGTH - 2.0, CHASSIS_WIDTH - 2.0, BOTTOM_THICKNESS + motor_diameter/2)

ml_hole = create_motor_hole(*ml_pos, motor_diameter/2, motor_height, "Motor_FL")
mr_hole = create_motor_hole(*mr_pos, motor_diameter/2, motor_height, "Motor_FR")
rl_hole = create_motor_hole(*rl_pos, motor_diameter/2, motor_height, "Motor_RL")
rr_hole = create_motor_hole(*rr_pos, motor_diameter/2, motor_height, "Motor_RR")

print("Motor mount positions:")
print(f"  Front-Left:  {ml_pos[:2]}")
print(f"  Front-Right: {mr_pos[:2]}")
print(f"  Rear-Left:   {rl_pos[:2]}")
print(f"  Rear-Right:  {rr_pos[:2]}")

# ============== SENSOR MOUNTS ==============
# Create small cylindrical posts for IR sensors
sensor_positions = [
    (CHASSIS_LENGTH - 0.5, CHASSIS_WIDTH / 2, "Front_Center"),
    (CHASSIS_LENGTH - 0.5, 0.5, "Front_Left"),
    (CHASSIS_LENGTH - 0.5, CHASSIS_WIDTH - 0.5, "Front_Right"),
    (0.5, 0.5, "Rear_Left"),
    (0.5, CHASSIS_WIDTH - 0.5, "Rear_Right"),
    (CHASSIS_LENGTH / 2, 0.3, "Left_Center"),
    (CHASSIS_LENGTH / 2, CHASSIS_WIDTH - 0.3, "Right_Center"),
]

sensor_height = CHASSIS_HEIGHT_FRONT + 0.5

for x, y, name in sensor_positions:
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.3,
        depth=0.8,
        location=(x, y, sensor_height)
    )
    sensor = bpy.context.active_object
    sensor.name = f"{name}_Mount"

print(f"Created {len(sensor_positions)} sensor mount positions")

# ============== WEIGHT DISTRIBUTION MARKERS ==============
# Battery placement marker (center of gravity)
battery_loc = (CHASSIS_LENGTH / 2, CHASSIS_WIDTH / 2, BOTTOM_THICKNESS + 0.5)
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=battery_loc
)
battery = bpy.context.active_object
battery.name = "Battery_Position_CoG"
battery.scale = (2.5, 1.8, 0.8)  # Approximate battery size

# ============== MATERIALS ==============
# Chassis material
chassis_mat = bpy.data.materials.new(name="Chassis_Material")
chassis_mat.use_nodes = True
bsdf = chassis_mat.node_tree.nodes["Principled BSDF"]
bsdf.inputs["Base Color"].default_value = (0.2, 0.5, 0.8, 1.0)  # Blue
bsdf.inputs["Metallic"].default_value = 0.3
bsdf.inputs["Roughness"].default_value = 0.7

if chassis.data.materials:
    chassis.data.materials[0] = chassis_mat
else:
    chassis.data.materials.append(chassis_mat)

# Sensor mount material (red for visibility)
sensor_mat = bpy.data.materials.new(name="Sensor_Mounts")
sensor_mat.use_nodes = True
sensor_bsdf = sensor_mat.node_tree.nodes["Principled BSDF"]
sensor_bsdf.inputs["Base Color"].default_value = (0.9, 0.2, 0.2, 1.0)  # Red

for obj in bpy.data.objects:
    if "Mount" in obj.name:
        if obj.data.materials:
            obj.data.materials[0] = sensor_mat
        else:
            obj.data.materials.append(sensor_mat)

# Battery marker material (yellow)
battery_mat = bpy.data.materials.new(name="Battery_Position")
battery_mat.use_nodes = True
battery_bsdf = battery_mat.node_tree.nodes["Principled BSDF"]
battery_bsdf.inputs["Base Color"].default_value = (0.9, 0.8, 0.2, 1.0)  # Yellow

if battery.data.materials:
    battery.data.materials[0] = battery_mat
else:
    battery.data.materials.append(battery_mat)

# ============== APPLY MODIFIERS AND EXPORT ==============
# Apply solidify modifier to make it a real mesh
bpy.context.view_layer.objects.active = chassis
for mod in chassis.modifiers:
    bpy.ops.object.modifier_apply(modifier=mod.name)

# Export as STL (export all objects)
stl_path = "/home/j23/Robotics/hardware/chassis-designs/mini_sumo_chassis.stl"
bpy.ops.wm.stl_export(filepath=stl_path)

# Also export OBJ format (preserves materials)
obj_path = "/home/j23/Robotics/hardware/chassis-designs/mini_sumo_chassis.obj"
bpy.ops.wm.obj_export(filepath=obj_path)

# ============== SUMMARY ==============
print("\n" + "="*60)
print("CHASSIS CREATED SUCCESSFULLY!")
print("="*60)
print(f"Dimensions: {CHASSIS_LENGTH} x {CHASSIS_WIDTH} x {CHASSIS_HEIGHT_REAR} cm")
print(f"Wedge shape: Front {CHASSIS_HEIGHT_FRONT}cm, Rear {CHASSIS_HEIGHT_REAR}cm")
print(f"Wall thickness: {WALL_THICKNESS}cm")
print(f"Estimated weight: ~80-120g (PLA, hollow)")
print(f"\nEXPORTED FILES:")
print(f"  STL: {stl_path}")
print(f"  OBJ: {obj_path}")
print("\nTo view in Blender GUI:")
print(f"  blender {stl_path}")
print("\nTo open in Windows (from WSL):")
print(f"  explorer.exe {stl_path.replace('/home/j23', '//wsl$//home/j23')}")
print("="*60)
