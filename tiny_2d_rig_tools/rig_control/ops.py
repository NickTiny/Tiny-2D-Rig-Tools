import bpy


from tiny_2d_rig_tools.rig_control.core import (
    nudge_bone,
    change_pose,
)

class TINY2DRIG_bone_nudge_backward(bpy.types.Operator):
    bl_idname = "tiny2drig.bone_nudge_backward"
    bl_label = "Nudge Bone Backward"
    bl_description = "Nudge Limb chain backward in space"

    bone_name : bpy.props.StringProperty()

    def execute(self, context):
        return nudge_bone(self, context.active_object.pose.bones[self.bone_name], True)


class TINY2DRIG_bone_nudge_forward(bpy.types.Operator):
    bl_idname = "tiny2drig.bone_nudge_forward"
    bl_label = "Nudge Bone Forward"
    bl_description = "Nudge Limb chain forward in space"

    bone_name : bpy.props.StringProperty()

    def execute(self, context): 
        return nudge_bone(self, context.active_object.pose.bones[self.bone_name], False)
    
class TINY2DRIG_set_turnaround(bpy.types.Operator):
    bl_idname = "tiny2drig.set_turnaround"
    bl_label = "Change Turaround"
    bl_description = "+/- current head turnaround value for Body & Head"

    values : bpy.props.IntVectorProperty(size=2)

    def execute(self, context):
        return change_pose(self, context, self.values)



classes = (
    TINY2DRIG_bone_nudge_backward,
    TINY2DRIG_bone_nudge_forward,
    TINY2DRIG_set_turnaround,
    
    
)


def register():
    for i in classes:
        bpy.utils.register_class(i)


def unregister():
    for i in classes:
        bpy.utils.unregister_class(i)
