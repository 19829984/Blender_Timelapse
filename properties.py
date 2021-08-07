import bpy
from .utils import registration

class Timelapse_Addon_Properties(bpy.types.PropertyGroup):
    seconds_per_frame: bpy.props.FloatProperty(
        name="",
        description="Time between each screenshot taken",
        min=1,
        default=10,
        subtype="TIME",
        unit="TIME"
    )

    output_name: bpy.props.StringProperty(
        name="Output Name",
        description="Name of the output files, no extensions",
        default='timelapse-screenshot'
    )

    file_format: bpy.props.EnumProperty(
        name="File Format",
        items=(
            ('png', 'PNG', ''),
            ('bmp', 'BMP', ''),
            ('jpeg', 'JPEG', ''),
            ('tiff', 'TIFF', ''),
            ('exr', 'OpenEXR', ''),
        ),
        default='png'
    )

    num_screenshots: bpy.props.IntProperty(
        name="",
        default=0,
        min=0
    )

    screenshot_is_due: bpy.props.BoolProperty(
        name="",
        default=False
    )

    remind_resume: bpy.props.BoolProperty(
        name="",
        default=True
    )

    auto_resume: bpy.props.BoolProperty(
        name="",
        default=False,
    )

    dir_path: bpy.props.StringProperty(
        name="",
        description="timelapse screenshot output directory path",
        default="//timelapse_screenshots/",
        # maxlen=1024,
        subtype='DIR_PATH'
    )

    is_running: bpy.props.BoolProperty(
        name="Is Timelapse Running",
        default=False
    )

classes = [Timelapse_Addon_Properties]

def register():
    # Properties
    registration.register_classes(classes)
    bpy.types.Scene.tl = bpy.props.PointerProperty(
        type=Timelapse_Addon_Properties)


def unregister():
    # Properties
    registration.unregister_classes(classes)
    del bpy.types.Scene.tl
