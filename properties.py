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
        print("checking " + prop_name)
        print("stored prop", stored_prop)
        print("current prop", current_prop)
        if stored_prop is not None and current_prop != stored_prop:
            print("restoring", prop_name, "to ",
                  stored_prop, "was ", current_prop)
            setattr(scene.tl, prop_name, stored_prop)

    restore_tl_prop("num_screenshots")
    restore_tl_prop("is_running")

    # if is_running:
    #     seconds_per_frame = getattr(restore_tl_props, "seconds_per_frame", None)
    #     output_name = getattr(restore_tl_props, "output_name", None)
    #     file_format = getattr(restore_tl_props, "file_format", None)
    #     is_running = getattr(restore_tl_props, "is_running", None)


def store_tl_props(self, context, prop_name):
    prop_to_store = getattr(self, prop_name, None)
    setattr(restore_tl_props, prop_name, prop_to_store)
    # restore_tl_props.num_screenshots = self.num_screenshots
    # restore_tl_props.is_running = self.is_running
    # if self.is_running: #Prevent settings from changing due to a undo/redo while a timelapse is taking place
    #     restore_tl_props.seconds_per_frame = self.seconds_per_frame
    #     restore_tl_props.output_name = self.output_name
    #     restore_tl_props.file_format = self.file_format
    #     restore_tl_props.enable_screenshot_notification = self.enable_screenshot_notification
    #     restore_tl_props.remind_resume = self.remind_resume
    #     restore_tl_props.auto_resume = self.auto_resume
    #     restore_tl_props.dir_path = self.dir_path


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

    enable_screenshot_notification: bpy.props.BoolProperty(
        name="",
        default=False
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
        subtype='DIR_PATH',
        update=update_counter_on_dir_change
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
