import bpy
import functools
import os
from .utils import registration

def screenshot_timer(context, report, seconds):
    tl = context.scene.tl
    print("Timer Running")
    if not tl.is_running:
        print("Timer stopped")
        return None
    print("Runing capture")
    if tl.enable_screenshot_notification:
        report(
            {"INFO"}, ("Taking {}th screenshot".format(tl.num_screenshots)))
    abs_path = bpy.path.abspath(tl.dir_path)
    if not os.path.isdir(abs_path):
        report(
            {"INFO"}, ("{} does not exist, creating folder".format(abs_path)))
        try:
            os.mkdir(abs_path)
        except PermissionError as err:
            report({"ERROR"}, err)
            bpy.ops.timelapse.pause_operator()
            return None
    try:
        bpy.ops.screen.screenshot(
            filepath="{}{}-{}.{}".format(tl.dir_path, tl.output_name,
                                            str(tl.num_screenshots), tl.file_format),
            check_existing=True)
    except RuntimeError:
        report({"ERROR"}, abs_path +
                            " is invalid! Check your permissions")
        bpy.ops.timelapse.pause_operator()
        return None
    tl.num_screenshots += 1

    return seconds


class Timelapse_OT_start_timelapse_operator(bpy.types.Operator):
    bl_idname = "timelapse.start_operator"
    bl_description = "Start the timelapse recording"
    bl_label = "Start Timelapse"

    def __init__(self):
        self.report({'INFO'}, "Starting Timelapse")

    def execute(self, context):
        if not bpy.data.is_saved:
            self.report(
                {"ERROR"}, "File hasn't been saved yet, please save and try again")
            return {"FINISHED"}
        tl = context.scene.tl

        if tl.is_running:
            self.report({"INFO"}, "Timelapse already started!")
            return {'FINISHED'}

        tl.is_running = True
        self.report({"INFO"}, "Timelapse started")

        bpy.app.timers.register(
            functools.partial(
                screenshot_timer, context, self.report, tl.seconds_per_frame))

        return {'FINISHED'}


class Timelapse_OT_pause_timelapse_operator(bpy.types.Operator):
    bl_idname = "timelapse.pause_operator"
    bl_description = "Pause the timelapse recording"
    bl_label = "Pause Timelapse"


    def execute(self, context):
        tl = context.scene.tl

        if tl.is_running:
            tl.is_running = False
            self.report({"INFO"}, "Timelapse paused")
            return {'FINISHED'}

        self.report({'WARNING'}, "No timelapse is being recorded.")
        return {'FINISHED'}


class Timelapse_OT_end_timelapse_operator(bpy.types.Operator):
    bl_idname = "timelapse.end_operator"
    bl_description = "End the timelapse recording and reset"
    bl_label = "End Timelapse"

    def execute(self, context):
        tl = context.scene.tl

        tl.num_screenshots = 0
        self.report({"INFO"}, "Timelapse ended")
        return bpy.ops.timelapse.pause_operator()


classes = [Timelapse_OT_start_timelapse_operator,
           Timelapse_OT_pause_timelapse_operator,
           Timelapse_OT_end_timelapse_operator]


def register():
    registration.register_classes(classes)


def unregister():
    registration.unregister_classes(classes)
