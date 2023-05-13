import bpy


# TODO create a simple dict that will return the assembled names for all bones and props
# instead of constructing the name in multiple places.
def get_ik_control_bools(rig_pref):
    return [
        f'{rig_pref.l_side}{rig_pref.arm}{rig_pref.flip}{rig_pref.ik}',
        f'{rig_pref.l_side}{rig_pref.arm}{rig_pref.ik}',
        f'{rig_pref.l_side}{rig_pref.hand}{rig_pref.nudge}',
        f'{rig_pref.l_side}{rig_pref.leg}{rig_pref.flip}{rig_pref.ik}',
        f'{rig_pref.l_side}{rig_pref.leg}{rig_pref.ik}',
        f'{rig_pref.r_side}{rig_pref.arm}{rig_pref.flip}{rig_pref.ik}',
        f'{rig_pref.r_side}{rig_pref.arm}{rig_pref.ik}',
        f'{rig_pref.r_side}{rig_pref.arm}{rig_pref.ik}{rig_pref.flip}',
        f'{rig_pref.r_side}{rig_pref.arm}_{rig_pref.leg}{rig_pref.ik}',
        f'{rig_pref.r_side}{rig_pref.hand}{rig_pref.nudge}',
        f'{rig_pref.r_side}{rig_pref.leg}{rig_pref.flip}{rig_pref.ik}',
        f'{rig_pref.r_side}{rig_pref.leg}{rig_pref.ik}',
    ]


def bone_side_prefix_get(bone_name, rig_prefs):
    if rig_prefs.r_side == bone_name[0 : len(rig_prefs.r_side)]:
        return rig_prefs.r_side

    if rig_prefs.l_side == bone_name[0 : len(rig_prefs.r_side)]:
        return rig_prefs.l_side


def bone_limb_get(bone_name, rig_prefs):
    if rig_prefs.arm in bone_name:
        return rig_prefs.arm

    if rig_prefs.leg in bone_name:
        return rig_prefs.leg


def get_ik_mod_bones(rig_pref):
    return [
        f"{rig_pref.r_side}{rig_pref.arm}{rig_pref.limb_lw}",
        f"{rig_pref.l_side}{rig_pref.arm}{rig_pref.limb_lw}",
        f"{rig_pref.r_side}{rig_pref.leg}{rig_pref.limb_lw}",
        f"{rig_pref.l_side}{rig_pref.leg}{rig_pref.limb_lw}",
    ]


def get_appendage_bones(rig_pref):
    return [
        f"{rig_pref.r_side}{rig_pref.arm}{rig_pref.hand}",
        f"{rig_pref.l_side}{rig_pref.arm}{rig_pref.hand}",
        f"{rig_pref.r_side}{rig_pref.leg}{rig_pref.foot}",
        f"{rig_pref.l_side}{rig_pref.leg}{rig_pref.foot}",
    ]


class TINY2DRIG_Addon_Preferences(bpy.types.AddonPreferences):
    """
    Addon preferences to kitsu. Holds variables that are important for authentication and configuring
    how some of the operators work.
    """

    bl_idname = "tiny_2d_rig_tools"
    show_advanced: bpy.props.BoolProperty(
        name="Set Custom Naming Conventions", default=False
    )

    def draw_box(self, layout, prefs, items, name=None, icon=None):
        box = layout.box()
        box = box.column(align=True)
        if name is not None and icon is None:
            box.label(text=name)
        if (name and icon) is not None:
            box.label(text=name, icon=icon)
        for item in items:
            box.prop(prefs, item)

    def draw(self, context: bpy.types.Context) -> None:
        self.layout.prop(self, "show_advanced")
        if not self.show_advanced:
            return
        layout = self.layout.box()
        prefs = context.window_manager.tiny_rig_prefs

        sides = ["r_side", "l_side"]

        spine_bones = [
            "spine_lower",
            "spine_upper",
            "spine_neck",
        ]

        bone_strings = [
            "limb_lw",
            "limb_up",
            "hand",
            "foot",
            "arm",
            "leg",
            "ik",
            "pole",
            "nudge",
            "flip",
        ]

        pose_properties = ["pose_body", "pose_head"]

        bone_groups = ["left_bone_group", "right_bone_group", "spine_bone_group"]
        self.draw_box(layout, prefs, sides, "Side Prefixes", "MOD_MIRROR")
        self.draw_box(layout, prefs, spine_bones, "Spine Bones", "BONE_DATA")
        self.draw_box(layout, prefs, bone_strings, "Bone Prefixes", "BONE_DATA")
        self.draw_box(layout, prefs, pose_properties, "Turnaround Properties", "ACTION")
        self.draw_box(layout, prefs, bone_groups, "Bone Group Names", "GROUP_BONE")


class TINY2DRIG_Rig_Preferences(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="", default="")

    # Prefix
    r_side: bpy.props.StringProperty(
        name="Right Side", default="R_", description="Prefix for Right Side"
    )
    l_side: bpy.props.StringProperty(
        name="Left Side", default="L_", description="Prefix for LEft Side"
    )

    master_bone: bpy.props.StringProperty(
        name="Master Bone", default="Master", description="Root Bone's Full Name"
    )
    spine_root: bpy.props.StringProperty(
        name="Spine Root", default="Root", description="Root Spine Bone's Full Name"
    )
    spine_lower: bpy.props.StringProperty(
        name="Spine Lower", default="Lower", description="Lower Spine Bone's Full Name"
    )
    spine_upper: bpy.props.StringProperty(
        name="Spine Upper", default="Upper", description="Upper Spine Bone's Full Name"
    )
    spine_neck: bpy.props.StringProperty(
        name="Spine Neck", default="Neck", description="Neck Spine Bone's Full Name"
    )

    # Bone Strings
    limb_lw: bpy.props.StringProperty(
        name="Lower Limb", default=".Lw", description="Suffix for Lower Limbs"
    )
    limb_up: bpy.props.StringProperty(
        name="Upper limb", default=".Up", description="Suffix for Upper Limbs"
    )
    hand: bpy.props.StringProperty(
        name="Hand",
        default="Hand",
        description="Suffix for Hand Bones. Periods are not included in driver names",
    )
    foot: bpy.props.StringProperty(
        name="Foot",
        default="Foot",
        description="Suffix for Lower Limbs. Periods are not included in driver names",
    )
    arm: bpy.props.StringProperty(
        name="Arm", default="Arm", description="Suffix for Arm Limbs"
    )
    leg: bpy.props.StringProperty(
        name="Leg", default="Leg", description="Suffix for Leg Limbs"
    )
    ik: bpy.props.StringProperty(
        name="IK", default="_IK", description="Suffix for IK Bones"
    )
    pole: bpy.props.StringProperty(
        name="Pole", default="_Pole", description="Suffix for Pole Bones"
    )
    nudge: bpy.props.StringProperty(
        name="Nudge", default="_Nudge", description="Suffix for Nudge Bones"
    )
    flip: bpy.props.StringProperty(
        name="Flip", default="_Flip", description="Suffix for Flip/Mirror drivers"
    )

    # Turnaround
    pose_body: bpy.props.StringProperty(
        name="Body Pose",
        default="Pose",
        description="Control 'Turnaround' position/frame for body bones",
    )
    pose_head: bpy.props.StringProperty(
        name="Head Pose",
        default="Pose Head",
        description="Control 'Turnaround' position/frame for head bones",
    )

    # Bone Groups
    left_bone_group: bpy.props.StringProperty(
        name="Left Bones",
        default="Left Side",
        description="Color left side bones Green with THEME03",
    )
    right_bone_group: bpy.props.StringProperty(
        name="Right Bones",
        default="Right Side",
        description="Color right side bones Green with THEME01",
    )
    spine_bone_group: bpy.props.StringProperty(
        name="Spine Bones",
        default="Spine Bones",
        description="Color of spine bones Yellow with THEME09",
    )


classes = (TINY2DRIG_Addon_Preferences, TINY2DRIG_Rig_Preferences)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.WindowManager.tiny_rig_prefs = bpy.props.PointerProperty(
        type=TINY2DRIG_Rig_Preferences
    )


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
