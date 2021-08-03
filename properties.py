import bpy


class Timelapse_Addon_Properties(bpy.types.PropertyGroup):
    seconds_per_frame: bpy.props.FloatProperty(
        name="",
        description="Time between each screenshot taken",
        min=1,
        default=10,
        subtype="TIME",
        unit="TIME"
    )

    file_format: bpy.props.EnumProperty(
        name="File Format",
        items=(
            ('PNG', 'PNG', ''),
            ('BMP', 'BMP', ''),
            ('JPEG', 'JPEG', ''),
            ('TIFF', 'TIFF', ''),
            ('TARGA', 'Targa', ''),
            ('OPEN_EXR', 'OpenEXR', ''),
        ),
        default='PNG'
    )
    
    file_path: bpy.props.StringProperty(
        name="",
        description="timelapse screenshot output",
        default="./timelapse_screenshots",
        # maxlen=1024,
        subtype='DIR_PATH'
    )

    is_running: bpy.props.BoolProperty(
        name="Is Timelapse Running",
        default=False
    )


def register():
    # Properties
    bpy.utils.register_class(Timelapse_Addon_Properties)
    bpy.types.Scene.tl = bpy.props.PointerProperty(
        type=Timelapse_Addon_Properties)


def unregister():
    # Properties
    bpy.utils.unregister_class(Timelapse_Addon_Properties)
    del bpy.types.Scene.tl
