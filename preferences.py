import bpy
from bpy.types import AddonPreferences


class TimelapsePreferences(AddonPreferences):
    bl_idname= __package__


    def draw(self, context):
        tl = context.scene.tl
        layout = self.layout
        row=layout.row()

        row.prop(tl, "auto_resume", text="Auto resume timelapse on loading file")
        row=layout.row()
        row.prop(tl, "remind_resume", text="Reminder timelapse is on when loading file")
        row.enabled = not tl.auto_resume
            

def register():
    bpy.utils.register_class(TimelapsePreferences)

def unregister():
    bpy.utils.unregister_class(TimelapsePreferences)
