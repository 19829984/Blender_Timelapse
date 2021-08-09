import bpy
import copy
import os
import bpy.utils.previews
from typing import Optional
from bpy.types import STATUSBAR_HT_header
from .timelapse import Timelapse_OT_start_timelapse_modal_operator as timelapse_ot_start
from .timelapse import Timelapse_OT_pause_timelapse_modal_operator as timelapse_ot_pause
from .timelapse import Timelapse_OT_end_timelapse_modal_operator as timelapse_ot_end
from .video import TIMELAPSE_OT_create_timelapse_clip as create_timelapse
from .utils import registration

original_status_bar_draw = copy.deepcopy(bpy.types.STATUSBAR_HT_header.draw)
custom_icons: Optional[bpy.utils.previews.ImagePreviewCollection] = None


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
        row.operator(timelapse_ot_start.bl_idname, text="Start Timelapse")
        row.operator(timelapse_ot_pause.bl_idname, text="Pause Timelapse")
        row.operator(timelapse_ot_end.bl_idname, text="End Timelapse")

        row = layout.row()
        box = row.box()
        box.alignment="LEFT"
        box.label(text="#Screenshots so far: {}".format(tl.num_screenshots))

        col = row.column()
        col.alignment="RIGHT"
        col.separator(factor=0.5)
        col.operator(create_timelapse.bl_idname, text="Create Timelapse Clip")
        row.enabled = not tl.is_running

class OUTPUT_PT_timelapse_settings_panel(bpy.types.Panel):
    bl_idname = "OUTPUT_PT_timelapse_settings_panel"
    bl_parent_id = "OUTPUT_PT_timelapse_panel"
    bl_label = "Timelapse Settings"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "output"

    def draw(self, context):
        layout = self.layout
        tl = context.scene.tl

        row = layout.row(align=True)
        row.label(text="Path to timelapse output:")
        row.prop(tl, "dir_path")
        row.enabled = not tl.is_running

        row = layout.row(align=True)
        row.prop(tl, "output_name")
        row.enabled = not tl.is_running

        row = layout.row(align=True)
        row.prop(tl, "file_format", icon="FILE_IMAGE")
        row.enabled = not tl.is_running

        row = layout.row(align=True)
        row.label(text="Seconds per Frame")
        row.prop(tl, 'seconds_per_frame')
        row.enabled = not tl.is_running



class WM_OT_If_Timelapse_On_Remind(bpy.types.Operator):
    bl_label = "Resume timelapse recording from previous session?"
    bl_idname = "wm.timelapse_remind"

    resume_timelapse: bpy.props.BoolProperty(
        name="Resume Timelapse", default=False)
    dont_remind_me: bpy.props.BoolProperty(
        name="Remember my choice and don't remind me again", default=False)

    def execute(self, context):
        tl = context.scene.tl
        if self.resume_timelapse:
            bpy.ops.timelapse.pause_modal_operator()
            bpy.ops.timelapse.start_modal_operator()
            
        if self.dont_remind_me:
            tl.auto_resume = self.resume_timelapse
        
        tl.remind_resume = not self.dont_remind_me

        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout

        row = layout.row(align=True)
        row.prop(data=self, property="resume_timelapse")

        row = layout.row(align=True)
        row.prop(data=self, property="dont_remind_me")

    def invoke(self, context, event):
        if context.scene.tl.is_running:
            bpy.ops.timelapse.pause_modal_operator()
            return context.window_manager.invoke_props_dialog(self)
        return {'FINISHED'}


def draw_timelapse_indicator(self, context):
    global custom_icons
    layout = self.layout
    tl = context.scene.tl

    row = layout.row()

    if tl.is_running:
        row.label(text='Timelapse ON',
                  icon_value=custom_icons['timelapse_icon_on'].icon_id)
    else:
        row.label(text='Timelapse OFF',
                  icon_value=custom_icons['timelapse_icon_off'].icon_id)

classes = [OUTPUT_PT_timelapse_panel, OUTPUT_PT_timelapse_settings_panel, WM_OT_If_Timelapse_On_Remind]

def register():
    # Icon
    register_icon()
    # UI
    registration.register_classes(classes)
    STATUSBAR_HT_header.prepend(draw_timelapse_indicator)


def unregister():
    # UI
    STATUSBAR_HT_header.draw = original_status_bar_draw
    registration.unregister_classes(classes)
    # Icon
    unregister_icon()


def register_icon():
    global custom_icons
    custom_icons = bpy.utils.previews.new()
    icons_dir = os.path.join(os.path.dirname(__file__), "icons")
    # On icon
    custom_icons.load("timelapse_icon_on", os.path.join(
        icons_dir, "timelapse_icon_on.png"), 'IMAGE')
    # Off icon
    custom_icons.load("timelapse_icon_off", os.path.join(
        icons_dir, "timelapse_icon_off.png"), 'IMAGE')


def unregister_icon():
    global custom_icons
    bpy.utils.previews.remove(custom_icons)
