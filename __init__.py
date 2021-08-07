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
from . import properties, ui, timelapse
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


modules = {properties, timelapse, ui}

@persistent
def check_timelapse_is_running_and_prompt(dummy):
    for scene in bpy.data.scenes:
        tl = scene.get('tl', None)
        print(tl.keys())
        if tl is not None:
            if tl.get('is_running') == True:
                print("Timelapse already running")
                if tl.get('remembered_choice') is not None:
                    print("Choice", tl.get('remembered_choice'))
                    if tl['remembered_choice'] == 1: #auto_resume
                        print("Autoresume detected")
                        tl['is_running'] = False #So that the modal will run
                        bpy.ops.timelapse.start_modal_operator()
                    elif tl['remembered_choice'] == 0: #no memory
                        print("No memory")
                        bpy.ops.wm.timelapse_remind("INVOKE_DEFAULT")
                    break
                else:
                    print("No memory")
                    bpy.ops.wm.timelapse_remind("INVOKE_DEFAULT")
                    break




def register():
    for module in modules:
        module.register()
    bpy.app.handlers.load_post.append(check_timelapse_is_running_and_prompt)


def unregister():
    for module in modules:
        module.unregister()
    bpy.app.handlers.load_post.remove(check_timelapse_is_running_and_prompt)
