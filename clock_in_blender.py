import sys
import bpy
from math import pi
from random import randrange

# Settings:

CLOCK_RADIUS = 6.75
CLOCK_DEPTH = 0.5

SURFACES = [
    # color Light Blue
    {'name': "hand", 'color': (0.7, 0.8, 1, 1)},
    # color Blue
    {'name': "line", 'color':  (0.1, 0.5, 1, 1)},
    # color Grey
    {'name': "board", 'color':  (0.2, 0.2, 0.2, 1)}, 
]

# Code:

def get_inputs():
    """Extracting line arguments.

    Use of argparse module is in direct conflict with blender arguments,
    so I used custom solution instead of rewriting part of the module.
    """
    inputs = [0,0] # default values
    arguments = sys.argv
    
    if '--' in arguments:
        # separating non-blender related arguments after mark "--"
        arguments = arguments[arguments.index('--') +1:]    
        for part in arguments:
            match part:
                case '--hours' | '-h':
                    inputs[0] = extract_argument(arguments, part, 24)
                case '--minutes' | '-m':
                    inputs[1] = extract_argument(arguments, part, 60)
                case '--random'| '-r':
                    inputs = random_time()
                # skipping expected number parameters
                case part if part.isnumeric():
                    pass
                case _:
                    print(f'Unexpected argument: {part}')
    
    if inputs == [0,0]: # giving guidance in case of no argument is set
        print_help()
    return inputs


def extract_argument(group, selection, limit):
    """Evaluation of the next argument with defined number limit."""
    position = group.index(selection)
    try:
        # expecting number after argument
        argument = int(group[position +1])
        # limit evaluation
        if argument < limit:
            return argument
        else:
            raise ValueError
    # printing help in case of invalid argument
    except ValueError:
        print(f'Argument {selection} has to specified with number to maximum of {limit}')
        print_help()


def random_time():
    time = [0,0]
    time[0] = randrange(24) # set random hour (0-23)
    time[1] = randrange(60) # set random minute (0-59)
    return time


def print_help():
    """Providing guidance to the user how to set arguments."""
    print(f"""Set your arguments in format:
    blender --python clock_in_blender.py -- --hours 0-23 --minutes 0-59""")


def clean_environment():
    """Erasing default blender objects."""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    

def create_clock():
    """Overarching function for object of clock as whole."""
    create_materials()
    create_board()
    create_section_lines()


def create_materials():
    """Defining colors of the clock's parts."""
    for item in SURFACES:
        material = bpy.data.materials.new(name=item['name'])
        material.diffuse_color = (item['color'])


def create_board():
    """Creation of clock's background."""
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=64, radius=CLOCK_RADIUS, depth=0.2*CLOCK_DEPTH)
    rename('Board')
    assign_material('board')


def rename(new_name):
    """Give object recognizable name in Blender GUI."""
    last_object = bpy.context.active_object
    last_object.name = new_name


def assign_material(material_name):
    last_object = bpy.context.active_object
    material = bpy.data.materials[material_name]
    last_object.data.materials.append(material)


def create_section_lines():
    """Creation of lines, which serves as indication of hours."""
    for number in range(12):
        add_line(number * (-pi/6))


def add_line(angle):
    bpy.ops.mesh.primitive_cube_add(
        scale=(0.5*CLOCK_DEPTH, 0.1*CLOCK_RADIUS, CLOCK_DEPTH), rotation=(0, 0, angle))
    # translating lanes based on their rotation around z-axis into correct hour position
    bpy.ops.transform.translate(value=(0, 0.8*CLOCK_RADIUS, 0), orient_type='LOCAL')
    rename('Line')
    assign_material('line')


def set_time(hours, minutes):
    """Overarching function for seting hands on the clock."""
    set_hours(hours, minutes)
    set_minutes(minutes)


def set_hours(hours, minutes):
    # simple change of 24 hour format into analog 12 hour format
    if hours >= 12:
        hours -= 12
    # adjusting position of hour hand according to number of minutes    
    hours = hours + float(minutes/60)
    # adding hand into correct angle with z-axis based on hours parameter
    bpy.ops.mesh.primitive_cube_add(
        scale=(0.7*CLOCK_DEPTH, 0.3*CLOCK_RADIUS, 1.2*CLOCK_DEPTH), rotation=(0, 0, hours * (-pi/6)))
    # moving hand to position, when its beginning is in global position (0,0)
    bpy.ops.transform.translate(value=(0 ,0.3*CLOCK_RADIUS, 0), orient_type='LOCAL')
    rename('Hand_Hours')
    assign_material('hand')


def set_minutes(minutes):
    """Adding hand into correct angle with z-axis based on minutes parameter."""
    bpy.ops.mesh.primitive_cube_add(
        scale=(0.7*CLOCK_DEPTH, 0.45*CLOCK_RADIUS, 1.2*CLOCK_DEPTH), rotation=(0, 0, minutes * (-pi/30)))
    # moving hand to position, when its beginning is on global position (0,0)
    bpy.ops.transform.translate(value=(0, 0.45*CLOCK_RADIUS, 0), orient_type='LOCAL')
    rename('Hand_Minutes')
    assign_material('hand')


def set_front_view():
    """Rotation view for default position."""
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            with bpy.context.temp_override(area=area, region=area.regions[-1]):
                # selecting position from above with direct look at the clock
                bpy.ops.view3d.view_axis(type='TOP')
            break


# Execution:

if __name__ == "__main__":
    hours, minutes = get_inputs()
    clean_environment()
    create_clock()
    set_time(hours, minutes)
    set_front_view()