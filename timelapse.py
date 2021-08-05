import bpy
import functools
from .events import events

def screenshot_timer(tl, seconds):
    tl.screenshot_is_due = True
    print("Screenshot time")
    return seconds


class Timelapse_OT_start_timelapse_modal_operator(bpy.types.Operator):
    bl_idname = "timelapse.start_modal_operator"
    bl_description = "Start or Stop the timelapse recording"
    bl_label = "Timelapse Modal Operator"

    registered_timer_func = None

    def __init__(self):
        self.report({'INFO'}, "Starting Timelapse")

    def __del__(self):
        self.report({'INFO'}, "Timelapse Started")

    def modal(self, context, event):
        tl = context.scene.tl

        if not tl.is_running:
            if Timelapse_OT_start_timelapse_modal_operator.registered_timer_func is not None:
                print("Unregistered timer")
                bpy.app.timers.unregister(
                    Timelapse_OT_start_timelapse_modal_operator.registered_timer_func)
            return {'FINISHED'}
            
        tl.is_running = True

        if event.type in events:
            if tl.screenshot_is_due:
                self.report(
                    {"INFO"}, ("Taking {}th screenshot".format(tl.num_screenshots)))
                bpy.ops.screen.screenshot(
                    filepath="{}test-{}.png".format(tl.dir_path, str(tl.num_screenshots)))
                tl.num_screenshots += 1
                tl.screenshot_is_due = False

        return {'PASS_THROUGH'}

    def execute(self, context):
        tl = context.scene.tl

        if tl.is_running:
            self.report({"INFO"}, "Timelapse already started!")
            return {'PASS_THROUGH'}

        start_timelapse_cls = Timelapse_OT_start_timelapse_modal_operator

        tl.is_running = True
        self.report({"INFO"}, "Timelapse started")

        
        print("Registering timer with: " + str(tl.seconds_per_frame))
        start_timelapse_cls.registered_timer_func = functools.partial(
            screenshot_timer, tl, tl.seconds_per_frame)

        bpy.app.timers.register(
            start_timelapse_cls.registered_timer_func)

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


class Timelapse_OT_end_timelapse_modal_operator(bpy.types.Operator):
    bl_idname = "timelapse.end_modal_operator"
    bl_description = "Start or Stop the timelapse recording"
    bl_label = "Timelapse Modal Operator"

    registered_timer_func = None

    def __init__(self):
        self.report({'INFO'}, "Ending Timelapse")

    def __del__(self):
        self.report({'INFO'}, "Timelapse Ended")

    def execute(self, context):
        tl = context.scene.tl

        if tl.is_running:
            tl.is_running = False
            self.report({"INFO"}, "Timelapse cancelled")
            return {'FINISHED'}

        self.report({'WARNING'}, "No timelapse is being recorded.")
        return {'FINISHED'}


classes = [Timelapse_OT_start_timelapse_modal_operator,
           Timelapse_OT_end_timelapse_modal_operator]



def register():
    print("Registering timelapse")
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
