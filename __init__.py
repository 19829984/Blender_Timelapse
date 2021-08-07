# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
from . import properties, ui, timelapse, preferences, video
import bpy
from bpy.app.handlers import persistent

bl_info = {
    "name": "Time_Lapse_Alpha",
    "author": "Bowen Wu",
    "description": "Alpha version of addon to automatically record a timelapse of your project",
    "blender": (2, 90, 0),
    "version": (0, 0, 1),
    "location": "",
    "warning": "",
    "category": "User"
}


modules = {properties, timelapse, ui, preferences, video}

@persistent
def check_timelapse_is_running_and_prompt(dummy):
    for scene in bpy.data.scenes:
        tl = scene.get('tl', None)
        print(tl.keys())
        if tl is not None:
            if tl.get('is_running') == True:
                print("Timelapse already running")

                if tl.get('remind_resume') is not None:
                    print("Checking reminder")
                    if tl.get('remind_resume'):
                        bpy.ops.wm.timelapse_remind("INVOKE_DEFAULT")
                        break
                    else:
                        if tl.get('auto_resume') is not None:
                            bpy.ops.timelapse.end_modal_operator() #So that the modal will run if needed
                            if tl.get('auto_resume'):
                                print("Autoresume detected")
                                bpy.ops.timelapse.start_modal_operator()
                            break
                else:
                    bpy.ops.wm.timelapse_remind("INVOKE_DEFAULT")
                    break



def register():
    for module in modules:
        module.register()
    bpy.app.handlers.load_post.append(check_timelapse_is_running_and_prompt)


def unregister():
    bpy.ops.timelapse.end_modal_operator()
    for module in modules:
        module.unregister()
    bpy.app.handlers.load_post.remove(check_timelapse_is_running_and_prompt)
