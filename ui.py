import bpy
from .timelapse import Timelapse_OT_start_timelapse_modal_operator as timelapse_ot_start
from .timelapse import Timelapse_OT_end_timelapse_modal_operator as timelapse_ot_end


class OUTPUT_PT_timelapse_panel(bpy.types.Panel):
    bl_idname = "OUTPUT_PT_timelapse_panel"
    bl_label = "Timelapse"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "output"

    def draw(self, context):
        layout = self.layout
        tl = context.scene.tl

        row = layout.row(align=True)
        row.label(text="Path to timelapse output:")
        row = layout.row(align=True)
        row.prop(tl, "dir_path")

        row = layout.row(align=True)
        row.label(text="Seconds per Frame")
        row.prop(tl, 'seconds_per_frame')

        row = layout.row(align=True)
        row.operator(timelapse_ot_start.bl_idname, text="Start Timelapse")
        row.operator(timelapse_ot_end.bl_idname, text="End Timelapse")


def register():
    # Properties
    bpy.utils.register_class(OUTPUT_PT_timelapse_panel)


def unregister():
    # Properties
    bpy.utils.unregister_class(OUTPUT_PT_timelapse_panel)
