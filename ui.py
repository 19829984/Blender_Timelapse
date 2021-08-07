import bpy
import copy
import os
import bpy.utils.previews
from typing import Optional
from bpy.types import STATUSBAR_HT_header
from .timelapse import Timelapse_OT_start_timelapse_modal_operator as timelapse_ot_start
from .timelapse import Timelapse_OT_end_timelapse_modal_operator as timelapse_ot_end

original_status_bar_draw = copy.deepcopy(bpy.types.STATUSBAR_HT_header.draw)
custom_icons: Optional[bpy.utils.previews.ImagePreviewCollection] = None


class OUTPUT_PT_timelapse_panel(bpy.types.Panel):
    bl_idname = "OUTPUT_PT_timelapse_panel"
    bl_label = "Timelapse Panel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "output"

    def draw(self, context):
        layout = self.layout
        tl = context.scene.tl

        row = layout.row(align=True)
        row.label(text="Path to timelapse output:")
        row.label(text="#Screenshots so far: {}".format(tl.num_screenshots))
        row = layout.row(align=True)
        row.prop(tl, "dir_path")

        row = layout.row(align=True)
        row.label(text="Seconds per Frame")
        row.prop(tl, 'seconds_per_frame')

        row = layout.row(align=True)
        row.operator(timelapse_ot_start.bl_idname, text="Start Timelapse")
        row.operator(timelapse_ot_end.bl_idname, text="End Timelapse")


class WM_OT_If_Timelapse_On_Remind(bpy.types.Operator):
    bl_label = "Resume timelapse recording from previous session?"
    bl_idname = "wm.timelapse_remind"

    resume_timelapse: bpy.props.BoolProperty(
        name="Resume Timelapse", default=False)
    dont_remind_me: bpy.props.BoolProperty(
        name="Remember my choice and don't remind me again", default=False)

    def execute(self, context):
        if self.resume_timelapse:
            bpy.ops.timelapse.start_modal_operator()
        if self.dont_remind_me:
            if self.resume_timelapse:
                context.scene.tl.remembered_choice = "auto_resume"
            else:
                context.scene.tl.remembered_choice = "do_not_resume"

        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout

        row = layout.row(align=True)
        row.prop(data=self, property="resume_timelapse")

        row = layout.row(align=True)
        row.prop(data=self, property="dont_remind_me")

    def invoke(self, context, event):
        if context.scene.tl.is_running:
            bpy.ops.timelapse.end_modal_operator()
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


def register():
    # Icon
    register_icon()
    STATUSBAR_HT_header.prepend(draw_timelapse_indicator)
    # UI
    bpy.utils.register_class(OUTPUT_PT_timelapse_panel)
    bpy.utils.register_class(WM_OT_If_Timelapse_On_Remind)


def unregister():
    # UI
    bpy.utils.unregister_class(WM_OT_If_Timelapse_On_Remind)
    bpy.utils.unregister_class(OUTPUT_PT_timelapse_panel)
    STATUSBAR_HT_header.draw = original_status_bar_draw
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
