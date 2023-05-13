import bpy
from tiny_2d_rig_tools.core_functions.scene import refresh_current_frame
from tiny_2d_rig_tools.core_functions.bone import bone_datapath_insert_keyframe
from tiny_2d_rig_tools.rig_control.core import toggle_ik


class RIGCONTROL_settings(bpy.types.PropertyGroup):
    is_rig: bpy.props.BoolProperty(
        name="Tiny Rig Status", description="Is this Rig a Tiny Rig", default=False
    )
    is_turnaround: bpy.props.BoolProperty(name="Rig Has Turnraround", default=False)
    is_ik: bpy.props.BoolProperty(name="Rig has IKs", default=False)
    pose_length: bpy.props.IntProperty(
        name="Turnaround Length",
        description="The number of turnaround poses in this character",
        default=3,
    )

    user_props: bpy.props.StringProperty(name="User Properties")

    pose_data_name: bpy.props.StringProperty(
        name="Pose Data Bone Name", default="PoseData"
    )


def get_obj():
    return bpy.context.active_object


def get_rig_prefs():
    return bpy.context.window_manager.tiny_rig_prefs


def get_prop_as_bool(prop_name):
    obj = bpy.context.active_object
    rig_set = obj.tiny_rig
    return bool(obj.pose.bones[f"{rig_set.pose_data_name}"].get(f"{prop_name}"))


def set_prop_as_bool(prop_name, bool):
    obj = bpy.context.active_object
    rig_set = obj.tiny_rig
    if obj.tiny_rig.is_rig:
        obj.pose.bones[f"{rig_set.pose_data_name}"][f"{prop_name}"] = int(bool)
        bone_datapath_insert_keyframe(
            obj.pose.bones[f"{rig_set.pose_data_name}"],
            prop_name,
            int(bool),
        )
        refresh_current_frame(bpy.context.scene)
    return


class RIGCONTROL_UI(bpy.types.PropertyGroup):
    def get_R_Foot(self):
        rig_prefs = get_rig_prefs()
        return get_prop_as_bool(f"{rig_prefs.r_side}{rig_prefs.foot}{rig_prefs.flip}")

    def set_R_Foot(self, bool):
        rig_prefs = get_rig_prefs()
        set_prop_as_bool(f"{rig_prefs.r_side}{rig_prefs.foot}{rig_prefs.flip}", bool)
        return

    R_Foot_Flip: bpy.props.BoolProperty(
        name="R_Foot Mirror",
        description="Mirror Right Foot drawings",
        get=get_R_Foot,
        set=set_R_Foot,
        options=set(),
        override={"LIBRARY_OVERRIDABLE"},
    )

    def get_L_Foot(self):
        rig_prefs = get_rig_prefs()
        return get_prop_as_bool(f"{rig_prefs.l_side}{rig_prefs.foot}{rig_prefs.flip}")

    def set_L_Foot(self, bool):
        rig_prefs = get_rig_prefs()
        set_prop_as_bool(f"{rig_prefs.l_side}{rig_prefs.foot}{rig_prefs.flip}", bool)
        return

    L_Foot_Flip: bpy.props.BoolProperty(
        name="L_Foot Mirror",
        description="Mirror Left Foot drawings",
        get=get_L_Foot,
        set=set_L_Foot,
        options=set(),
        override={"LIBRARY_OVERRIDABLE"},
    )

    def get_R_Hand(self):
        rig_prefs = get_rig_prefs()
        return get_prop_as_bool(f"{rig_prefs.r_side}{rig_prefs.hand}{rig_prefs.flip}")

    def set_R_Hand(self, bool):
        rig_prefs = get_rig_prefs()
        set_prop_as_bool(f"{rig_prefs.r_side}{rig_prefs.hand}{rig_prefs.flip}", bool)
        return

    R_Hand_Flip: bpy.props.BoolProperty(
        name="R_Hand Mirror",
        description="Mirror Right Hand drawings",
        get=get_R_Hand,
        set=set_R_Hand,
        options=set(),
        override={"LIBRARY_OVERRIDABLE"},
    )

    def get_L_Hand(self):
        rig_prefs = get_rig_prefs()
        return get_prop_as_bool(f"{rig_prefs.l_side}{rig_prefs.hand}{rig_prefs.flip}")

    def set_L_Hand(self, bool):
        rig_prefs = get_rig_prefs()
        set_prop_as_bool(f"{rig_prefs.l_side}{rig_prefs.hand}{rig_prefs.flip}", bool)
        return

    L_Hand_Flip: bpy.props.BoolProperty(
        name="L_Hand Mirror",
        description="Mirror Left Hand drawings",
        get=get_L_Hand,
        set=set_L_Hand,
        options=set(),
        override={"LIBRARY_OVERRIDABLE"},
    )

    def get_R_Arm_IK_Flip(self):
        return get_prop_as_bool("R_Arm_Flip_IK")

    def set_R_Arm_IK_Flip(self, bool):
        set_prop_as_bool("R_Arm_Flip_IK", bool)
        return

    R_Arm_Flip_IK: bpy.props.BoolProperty(
        name="Flip Arm R IK",
        description="Flip Right Arm IK Pole Position",
        get=get_R_Arm_IK_Flip,
        set=set_R_Arm_IK_Flip,
        options=set(),
        override={"LIBRARY_OVERRIDABLE"},
    )

    def get_L_Arm_IK_Flip(self):
        return get_prop_as_bool("L_Arm_Flip_IK")

    def set_L_Arm_IK_Flip(self, bool):
        set_prop_as_bool("L_Arm_Flip_IK", bool)
        return

    L_Arm_Flip_IK: bpy.props.BoolProperty(
        name="Flip Arm L IK Pole",
        description="Flip Left Arm IK Pole Position",
        get=get_L_Arm_IK_Flip,
        set=set_L_Arm_IK_Flip,
        options=set(),
        override={"LIBRARY_OVERRIDABLE"},
    )

    def get_R_Leg_IK_Flip(self):
        return get_prop_as_bool("R_Leg_Flip_IK")

    def set_R_Leg_IK_Flip(self, bool):
        set_prop_as_bool("R_Leg_Flip_IK", bool)
        return

    R_Leg_Flip_IK: bpy.props.BoolProperty(
        name="Flip Leg R IK Pole",
        description="Flip Right Leg IK Pole Position",
        get=get_R_Leg_IK_Flip,
        set=set_R_Leg_IK_Flip,
        options=set(),
        override={"LIBRARY_OVERRIDABLE"},
    )

    def get_L_Leg_IK_Flip(self):
        return get_prop_as_bool("L_Leg_Flip_IK")

    def set_L_Leg_IK_Flip(self, bool):
        set_prop_as_bool("L_Leg_Flip_IK", bool)
        return

    L_Leg_Flip_IK: bpy.props.BoolProperty(
        name="Flip Leg L IK Pole",
        description="Flip Left Leg IK Pole Position",
        get=get_L_Leg_IK_Flip,
        set=set_L_Leg_IK_Flip,
        options=set(),
        override={"LIBRARY_OVERRIDABLE"},
    )

    def get_L_Arm_IK(self):
        return get_prop_as_bool("L_Arm_IK")

    def set_L_Arm_IK(self, bool):
        toggle_ik(bpy.context, "L_Arm_IK")
        return

    L_Arm_IK: bpy.props.BoolProperty(
        name="L Arm IK",
        description="Enabled/Disable Inverse Kinematics for Left Arm",
        get=get_L_Arm_IK,
        set=set_L_Arm_IK,
        options=set(),
        override={"LIBRARY_OVERRIDABLE"},
    )

    def get_R_Arm_IK(self):
        return get_prop_as_bool("R_Arm_IK")

    def set_R_Arm_IK(self, bool):
        toggle_ik(bpy.context, "R_Arm_IK")
        return

    R_Arm_IK: bpy.props.BoolProperty(
        name="L Arm IK",
        description="Enabled/Disable Inverse Kinematics for Left Arm",
        get=get_R_Arm_IK,
        set=set_R_Arm_IK,
        options=set(),
        override={"LIBRARY_OVERRIDABLE"},
    )

    def get_L_Leg_IK(self):
        return get_prop_as_bool("L_Leg_IK")

    def set_L_Leg_IK(self, bool):
        toggle_ik(bpy.context, "L_Leg_IK")
        return

    L_Leg_IK: bpy.props.BoolProperty(
        name="L Leg IK",
        description="Enabled/Disable Inverse Kinematics for Left Leg",
        get=get_L_Leg_IK,
        set=set_L_Leg_IK,
        options=set(),
        override={"LIBRARY_OVERRIDABLE"},
    )

    def get_R_Leg_IK(self):
        return get_prop_as_bool("R_Leg_IK")

    def set_R_Leg_IK(self, bool):
        toggle_ik(bpy.context, "R_Leg_IK")
        return

    R_Leg_IK: bpy.props.BoolProperty(
        name="R Leg IK",
        description="Enabled/Disable Inverse Kinematics for Right Leg",
        get=get_R_Leg_IK,
        set=set_R_Leg_IK,
        options=set(),
        override={"LIBRARY_OVERRIDABLE"},
    )

    def get_R_Hand_Nudge(self):
        return get_prop_as_bool("R_Hand_Nudge")

    def set_R_Hand_Nudge(self, bool):
        set_prop_as_bool("R_Hand_Nudge", bool)
        return

    R_Hand_Nudge: bpy.props.BoolProperty(
        name="R_Hand_Nudge",
        description="Move Right Hand infront of Arm",
        get=get_R_Hand_Nudge,
        set=set_R_Hand_Nudge,
        options=set(),
        override={"LIBRARY_OVERRIDABLE"},
    )

    def get_L_Hand_Nudge(self):
        return get_prop_as_bool("L_Hand_Nudge")

    def set_L_Hand_Nudge(self, bool):
        set_prop_as_bool("L_Hand_Nudge", bool)
        return

    L_Hand_Nudge: bpy.props.BoolProperty(
        name="L_Hand_Nudge",
        description="Move Left Hand infront of Arm",
        get=get_L_Hand_Nudge,
        set=set_L_Hand_Nudge,
        options=set(),
        override={"LIBRARY_OVERRIDABLE"},
    )


classes = (RIGCONTROL_settings, RIGCONTROL_UI)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Object.offset_action = bpy.props.PointerProperty(
        name="Turnaround Action",
        type=bpy.types.Action,
        description="Turnaround action pre-determines the position of a bone via action constraint. Control turnaround with 'POSE' or 'POSE HEAD' property",
    )
    bpy.types.Object.tiny_rig = bpy.props.PointerProperty(type=RIGCONTROL_settings)
    bpy.types.WindowManager.tiny_rig_ui = bpy.props.PointerProperty(type=RIGCONTROL_UI)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Object.offset_action
    del bpy.types.Object.tiny_rig
    del bpy.types.WindowManager.tiny_rig_ui
