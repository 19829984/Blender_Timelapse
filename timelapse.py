import bpy


class Timelapse_OT_timelapse_operator(bpy.types.Operator):
    bl_idname = "timelapse.modal_operator"
    bl_description = "Start or Stop the timelapse recording"
    bl_label = "Timelapse Modal Operator"

    def __init__(self):
        self.report({'INFO'}, "Beginning timelapse")

    def __del__(self):
        self.report({'INFO'}, "Timelapse Finished")

    def execute(self, context):
        tl = context.scene.tl
        tl.is_running = True #Reminder: this works
        self.report({"INFO"}, "Starting Timelapse.")
        return {'FINISHED'}

    def cancel(self, context):
        pass


def register():
    print("Registering timelapse")
    bpy.utils.register_class(Timelapse_OT_timelapse_operator)


def unregister():
    bpy.utils.unregister_class(Timelapse_OT_timelapse_operator)
