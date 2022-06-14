import bpy
import os
from re import search
from .utils import registration


def update_counter_on_dir_change(self, context):
    tl = context.scene.tl

    screenshots = os.listdir(bpy.path.abspath(tl.dir_path))
    print(len(screenshots))
    if len(screenshots) == 0:
        tl.num_screenshots = 0
        return

    last_screenshot_num = 0

    for screenshot in screenshots:
        screenshot_num = search('(\d*)\..*$', screenshot)
        last_screenshot_num = max(
            last_screenshot_num, int(screenshot_num.group(1)))

    tl.num_screenshots = last_screenshot_num + 1

# Code adapted from https://blenderartists.org/t/prevent-panel-from-receiving-undo-hotkey-event/1192545/9
# Needed so that undo/redo does not affect these two attributes for the sake of consistent operation
def restore_tl_props(scene):
    def restore_tl_prop(prop_name):
        stored_prop = getattr(restore_tl_props, prop_name, None)
        current_prop = getattr(scene.tl, prop_name, None)
        if stored_prop is not None and current_prop != stored_prop:
            setattr(scene.tl, prop_name, stored_prop)
    restore_tl_prop("is_running")
    restore_tl_prop("num_screenshots")
    is_running = getattr(restore_tl_props, "is_running", None)
    # Prevent these settings from being changed while a timelapse is running
    if is_running:
        restore_tl_prop("seconds_per_frame")
        restore_tl_prop("output_name")
        restore_tl_prop("file_format")
        restore_tl_prop("enable_screenshot_notification")
        restore_tl_prop("remind_resume")
        restore_tl_prop("auto_resume")
        restore_tl_prop("dir_path")


def store_tl_props(self, context, prop_name):
    prop_to_store = getattr(self, prop_name, None)
    setattr(restore_tl_props, prop_name, prop_to_store)


class Timelapse_Addon_Properties(bpy.types.PropertyGroup):
    seconds_per_frame: bpy.props.FloatProperty(
        name="",
        description="Time between each screenshot taken",
        min=1,
        default=10,
        subtype="TIME",
        unit="TIME",
        update=lambda self, context: store_tl_props(
            self, context, "seconds_per_frame")
    )

    output_name: bpy.props.StringProperty(
        name="Output Name",
        description="Name of the output files, no extensions",
        default='timelapse-screenshot',
        update=lambda self, context: store_tl_props(
            self, context, "output_name")
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
        default='png',
        update=lambda self, context: store_tl_props(
            self, context, "file_format")
    )

    enable_screenshot_notification: bpy.props.BoolProperty(
        name="",
        default=False,
        update=lambda self, context: store_tl_props(
            self, context, "enable_screenshot_notification")
    )

    num_screenshots: bpy.props.IntProperty(
        name="",
        default=0,
        min=0,
        update=lambda self, context: store_tl_props(
            self, context, "num_screenshots")
    )

    remind_resume: bpy.props.BoolProperty(
        name="",
        default=True,
        update=lambda self, context: store_tl_props(
            self, context, "remind_resume")
    )

    auto_resume: bpy.props.BoolProperty(
        name="",
        default=False,
        update=lambda self, context: store_tl_props(
            self, context, "auto_resume")
    )

    def dir_path_update_func(self, context):
        store_tl_props(self, context, "dir_path")
        update_counter_on_dir_change(self, context)

    dir_path: bpy.props.StringProperty(
        name="",
        description="timelapse screenshot output directory path",
        default="//timelapse_screenshots/",
        subtype='DIR_PATH',
        update=dir_path_update_func
    )

    is_running: bpy.props.BoolProperty(
        name="Is Timelapse Running",
        default=False,
        update=lambda self, context: store_tl_props(
            self, context, "is_running")
    )


classes = [Timelapse_Addon_Properties]


def register():
    # Properties
    registration.register_classes(classes)
    bpy.types.Scene.tl = bpy.props.PointerProperty(
        type=Timelapse_Addon_Properties)
    bpy.app.handlers.undo_post.append(restore_tl_props)
    bpy.app.handlers.redo_post.append(restore_tl_props)


def unregister():
    # Properties
    registration.unregister_classes(classes)
    del bpy.types.Scene.tl
    bpy.app.handlers.undo_post.remove(restore_tl_props)
    bpy.app.handlers.redo_post.remove(restore_tl_props)
