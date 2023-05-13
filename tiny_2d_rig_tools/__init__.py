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

bl_info = {
    "name": "Tiny 2D Rig Tools",
    "author": "Nick Alberelli",
    "description": "Tools to Create and Rig 2D Cut-Out style characters with Grease Pencil Objects.",
    "blender": (3, 3, 0),
    "version": (0, 0, 1),
    "location": "3D View> Sidebar > Tiny Rig",
    "warning": "",
    "category": "Animation",
}

from tiny_2d_rig_tools import rig_control, rig_editor


def register():
    rig_control.register()
    rig_editor.register()


def unregister():
    rig_control.unregister()
    rig_editor.unregister()
