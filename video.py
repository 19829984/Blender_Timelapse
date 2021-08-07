import bpy
import os
from .utils import registration

class TIMELAPSE_OT_create_timelapse_clip(bpy.types.Operator):
    bl_idname = "timelapse.create_timelapse_clip"
    bl_description = "Create a clip from the recorded timelapse in Blender's Video Editor"
    bl_label = "Create Timelapse Clip"

    def execute(self, context):
        tl = context.scene.tl

        if "Video Editing" in bpy.data.workspaces.keys():
            context.window.workspace = bpy.data.workspaces['Video Editing']
        elif context.workspace.name != "Video Editing":
            video_editor_ws_path = next(bpy.utils.app_template_paths()) + '/Video_Editing' + '/startup.blend'
            bpy.ops.workspace.append_activate(idname="Video Editing", filepath=str(video_editor_ws_path))
            
        screenshots = set(os.listdir(tl.dir_path))

        timelapse_strip = context.scene.sequence_editor.sequences.new_image(
            name="Timelapse Sequence",
            filepath="{}{}-{}.{}".format(tl.dir_path, tl.output_name, 0, tl.file_format),
            channel=1,
            frame_start=0,
            fit_method='ORIGINAL'
            )

        for i in range(1, tl.num_screenshots):
            name = "{}-{}.{}".format(tl.output_name, i, tl.file_format)
            if name in screenshots:
                timelapse_strip.elements.append(name)

        return {'FINISHED'}

classes = [TIMELAPSE_OT_create_timelapse_clip]

def register():
    registration.register_classes(classes)

def unregister():
    registration.unregister_classes(classes)
