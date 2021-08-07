import bpy
from bpy.types import AddonPreferences
from .utils import registration



class TimelapsePreferences(AddonPreferences):
    bl_idname= __package__


    def draw(self, context):
        tl = context.scene.tl
        layout = self.layout
        row=layout.row(align=True)
        row.prop(tl, "auto_resume", text="Auto resume timelapse on loading file")

        row=layout.row(align=True)
        row.prop(tl, "remind_resume", text="Reminder timelapse is on when loading file")
        row.enabled = not tl.auto_resume
        
        row=layout.row(align=True)
        row.prop(tl, "num_screenshots", text="Change the screenshot counter (used in output suffix)")
            
classes = [TimelapsePreferences]

def register():
    registration.register_classes(classes)

def unregister():
    registration.unregister_classes(classes)
