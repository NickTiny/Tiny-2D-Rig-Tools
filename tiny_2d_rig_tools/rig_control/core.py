import bpy


from tiny_2d_rig_tools.core_functions.bone import (
    bake_constraints,
    reset_bones,
    get_consts_on_bone,
    bone_datapath_insert_keyframe,
)
from tiny_2d_rig_tools.core_functions.scene import (
    refresh_current_frame,
    offset_current_frame,
)



def normalize_pose_vals(datapath:str, offset:int, posemax:int):
    if offset == 0:
        return datapath
    pose = datapath + offset
    if pose in range(1, posemax + 1):
        return int(pose)
    if pose == 0 and offset < 0:
        return posemax
    if pose == (posemax + 1) and offset > 0:
        return 1


def change_pose(self, context:bpy.types.Context, values:list[int,int]):
    rig_prefs = bpy.context.window_manager.tiny_rig_prefs
    body_offset = values[0]
    head_offset = values[1]
    obj = context.active_object
    bone = obj.pose.bones[obj.tiny_rig.pose_data_name]
    body_val = normalize_pose_vals(
        bone[rig_prefs.pose_body], body_offset, obj.tiny_rig.pose_length)
    head_val = normalize_pose_vals(
        bone[rig_prefs.pose_head], head_offset, obj.tiny_rig.pose_length
    )
    if body_val is None or head_val is None:
        self.report({"ERROR"}, "Error while changing poses")
        return {"CANCELLED"}
    bone[rig_prefs.pose_body] = body_val
    bone[rig_prefs.pose_head] = head_val
    bone_datapath_insert_keyframe(bone, rig_prefs.pose_body, body_val)
    bone_datapath_insert_keyframe(bone, rig_prefs.pose_head, head_val)
    refresh_current_frame(context.scene)
    return {"FINISHED"}
    


def get_nudge_limits(bone:bpy.types.PoseBone):
    for const in get_consts_on_bone(bone, "LIMIT_LOCATION"):
        if abs(const.min_z) == abs(const.max_z):
            return abs(const.max_z) * -1


def nudge_bone(self, bone:bpy.types.PoseBone, negative:bool):
    val = 0.05
    if negative:
        val = -0.05

    # Check bone is at limits
    limit = get_nudge_limits(bone)
    if limit is not None:
        if negative:
            limit = abs(limit)
        if (bone.location[2] <= limit and not negative) or (
            bone.location[2] >= limit and negative
        ):
            self.report(
                {"ERROR"}, f"'{bone.name}' at Z limit of {round(limit,2)}")
            return {"CANCELLED"}

    bone.location[2] += -val
    bone.keyframe_insert("location")
    return {"FINISHED"}

def save_prev_frame(scene, posebone: bpy.types.PoseBone, datapath: str):
    offset_current_frame(scene, -1)
    posebone.keyframe_insert(f'["{datapath}"]', group=posebone.name)
    offset_current_frame(scene, +1)
    return


def toggle_ik(
    context:bpy.types.Context,
    datapath:str,
):
    rig_prefs = context.window_manager.tiny_rig_prefs
    prefix = datapath.split(rig_prefs.ik)[0]
    bone_names = [f"{prefix}{rig_prefs.limb_lw}",f"{prefix}{rig_prefs.limb_up}"]
    scene = context.scene
    index = int(scene.frame_current)
    obj = context.active_object
    posebone = obj.pose.bones[obj.tiny_rig.pose_data_name]
    ik_bone = obj.pose.bones[datapath]
    bones = [bone for bone in obj.pose.bones if bone.name in bone_names]
    if posebone[f"{datapath}"] == 1:
        save_prev_frame(scene, posebone, datapath)
        bake_constraints(bones, index)
        bone_datapath_insert_keyframe(posebone, datapath, 0)
        refresh_current_frame(scene)
        return {"FINISHED"}
    if posebone[f"{datapath}"] == 0:
        save_prev_frame(scene, posebone, datapath)
        offset_current_frame(scene, -1)
        # keyframe previous bone state
        for bone in bones:
            bone.keyframe_insert("rotation_euler", group=bone.name),
            bone.keyframe_insert("rotation_quaternion", group=bone.name)
        bake_constraints((ik_bone,), index)
        bone_matrix = ik_bone.matrix
        ik_bone.keyframe_insert("location", group=ik_bone.name)
        ik_bone.keyframe_insert("rotation_euler", group=ik_bone.name)
        offset_current_frame(scene, +1)
        reset_bones(bones)
        for bone in bones:
            bone.keyframe_insert("rotation_euler", group=bone.name)
            bone.keyframe_insert("rotation_quaternion", group=bone.name)
        bone_datapath_insert_keyframe(posebone, datapath, 1)
        refresh_current_frame(scene)
        ik_bone.matrix = bone_matrix
        ik_bone.keyframe_insert("location", group=ik_bone.name)
        ik_bone.keyframe_insert("rotation_euler", group=ik_bone.name)
        return {"FINISHED"}

