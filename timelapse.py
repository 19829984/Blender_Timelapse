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

    def modal(self, context, event):
        tl = context.scene.tl

        if not tl.is_running:
            return {'FINISHED'}
            
        tl.is_running = True

        if event.type in events:
            if tl.screenshot_is_due:
                self.report(
                    {"INFO"}, ("Taking {}th screenshot".format(tl.num_screenshots)))
                try:
                    bpy.ops.screen.screenshot(
                        filepath="{}test-{}.png".format(tl.dir_path, str(tl.num_screenshots)))
                except RuntimeError:
                    self.report({"ERROR"}, tl.dir_path + " is invalid!")
                    bpy.ops.timelapse.end_modal_operator()
                    return {'FINISHED'}
                tl.num_screenshots += 1
                tl.screenshot_is_due = False

        return {'PASS_THROUGH'}

    def execute(self, context):
        tl = context.scene.tl

        if tl.is_running:
            self.report({"INFO"}, "Timelapse already started!")
            return {'PASS_THROUGH'}

        start_modal_cls = Timelapse_OT_start_timelapse_modal_operator

        tl.is_running = True
        self.report({"INFO"}, "Timelapse started")

        
        print("Registering timer with: " + str(tl.seconds_per_frame))
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
            print("Unregistered timer")
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
    print("Registering timelapse")
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
