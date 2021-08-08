import bpy
import functools
import os
from .events import events
from .utils import registration

def screenshot_timer(tl, seconds):
    tl.screenshot_is_due = True
    return seconds


class Timelapse_OT_start_timelapse_modal_operator(bpy.types.Operator):
    bl_idname = "timelapse.start_modal_operator"
    bl_description = "Start or Stop the timelapse recording"
    bl_label = "Timelapse Modal Operator"

    registered_timer_func = None

    def __init__(self):
        self.report({'INFO'}, "Starting Timelapse")

    def modal(self, context, event):
        tl = context.scene.tl

        if not tl.is_running:
            return {'FINISHED'}
            
        tl.is_running = True

        if event.type in events:
            if tl.screenshot_is_due:
                self.report(
                    {"INFO"}, ("Taking {}th screenshot".format(tl.num_screenshots)))
                abs_path = bpy.path.abspath(tl.dir_path)
                if not os.path.isdir(abs_path):
                    self.report({"INFO"}, ("{} does not exist, creating folder".format(abs_path)))
                    try:
                        os.mkdir(abs_path)
                    except PermissionError as err:
                        self.report({"ERROR"}, err)
                        bpy.ops.timelapse.end_modal_operator()
                        return {'FINISHED'}
                try:
                    bpy.ops.screen.screenshot(
                        filepath="{}{}-{}.{}".format(tl.dir_path, tl.output_name, str(tl.num_screenshots), tl.file_format))
                except RuntimeError:
                    self.report({"ERROR"}, abs_path + " is invalid! Check your permissions")
                    bpy.ops.timelapse.end_modal_operator()
                    return {'FINISHED'}
                tl.num_screenshots += 1
                tl.screenshot_is_due = False

        return {'PASS_THROUGH'}

    def execute(self, context):
        if not bpy.data.is_saved:
            self.report({"ERROR"}, "File hasn't been saved yet, please save and try again")
            return {"FINISHED"}
        tl = context.scene.tl

        if tl.is_running:
            self.report({"INFO"}, "Timelapse already started!")
            return {'PASS_THROUGH'}

        start_modal_cls = Timelapse_OT_start_timelapse_modal_operator

        tl.is_running = True
        self.report({"INFO"}, "Timelapse started")

        
        if start_modal_cls.registered_timer_func is not None and bpy.app.timers.is_registered(start_modal_cls.registered_timer_func):
            bpy.app.timers.unregister(
                start_modal_cls.registered_timer_func)

        start_modal_cls.registered_timer_func = functools.partial(
            screenshot_timer, tl, tl.seconds_per_frame)

        bpy.app.timers.register(
            start_modal_cls.registered_timer_func)

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


class Timelapse_OT_end_timelapse_modal_operator(bpy.types.Operator):
    bl_idname = "timelapse.end_modal_operator"
    bl_description = "Start or Stop the timelapse recording"
    bl_label = "Timelapse Modal Operator"

    registered_timer_func = None

    def __init__(self):
        self.report({'INFO'}, "Ending Timelapse")


    def execute(self, context):
        tl = context.scene.tl

        start_modal_cls = Timelapse_OT_start_timelapse_modal_operator
        
        if start_modal_cls.registered_timer_func is not None and bpy.app.timers.is_registered(start_modal_cls.registered_timer_func):
            bpy.app.timers.unregister(
                start_modal_cls.registered_timer_func)

        if tl.is_running:
            tl.is_running = False
            self.report({"INFO"}, "Timelapse cancelled")
            return {'FINISHED'}
                
        self.report({'WARNING'}, "No timelapse is being recorded.")
        return {'FINISHED'}


classes = [Timelapse_OT_start_timelapse_modal_operator,
           Timelapse_OT_end_timelapse_modal_operator]



def register():
    registration.register_classes(classes)


def unregister():
    registration.unregister_classes(classes)
