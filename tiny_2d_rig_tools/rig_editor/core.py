import bpy
import math
from tiny_2d_rig_tools.core_functions.bone import get_consts_on_bone
from tiny_2d_rig_tools.core_functions.drivers import add_driver
from tiny_2d_rig_tools.core_functions.object import get_consts_on_obj
from tiny_2d_rig_tools.rig_editor.prefs import bone_side_prefix_get, bone_limb_get


def get_rig_prefs():
    """Returns Grpup of Properties from addon Preferences"""
    return bpy.context.window_manager.tiny_rig_prefs


# Action Constraints
def get_action_offset_bones(
    bones: list[bpy.types.PoseBone],
) -> list[bpy.types.ActionConstraint]:
    action_constraints = []
    for bone in bones:
        for const in get_consts_on_bone(bone, "ACTION"):
            action_constraints.append(const)
    return action_constraints


def set_modifier_and_constraint_viewport(
    obj: bpy.types.Object, enable_status: bool
) -> bool:
    for mod in obj.grease_pencil_modifiers:
        mod.show_viewport = enable_status
    for const in obj.constraints:
        const.enabled = enable_status


def check_modifier_and_constraint_viewport(obj: bpy.types.Object) -> bool:
    for mod in obj.grease_pencil_modifiers:
        if mod.show_viewport == False:
            return mod.show_viewport
    for const in obj.constraints:
        if const.enabled == False:
            return const.enabled

    return True


def get_grease_pencil_modifiers(
    obj: bpy.types.Object, type
) -> list[bpy.types.Constraint]:
    return [mod for mod in obj.grease_pencil_modifiers if mod.type == type]


def gpencil_fix_offset_show_viewport(obj: bpy.types.Object, enable: bool):
    mods = get_grease_pencil_modifiers(obj, "GP_TIME")
    for mod in [mod for mod in mods if mod.mode == "FIX"]:
        mod.show_viewport = enable


def get_armature_constraint(obj: bpy.types.Object) -> bpy.types.Constraint:
    constraints = get_consts_on_obj(obj, "ARMATURE")
    if len(constraints) == 1:
        return constraints[0]


def enable_lattice_mod(obj: bpy.types.Object, show_viewport: bool):
    for mod in get_grease_pencil_modifiers(obj, "GP_LATTICE"):
        mod.show_viewport = show_viewport


def enable_gpencil_armature_modifier(mod: bpy.types.Modifier, enable: bool):
    rig = mod.object
    rig.data.pose_position = "POSE" if enable else "REST"
    mod.show_viewport = enable


def enable_armature_constraint(const: bpy.types.Constraint, enable: bool):
    const.enabled = enable
    rig = const.targets[0].target
    rig.data.pose_position = "POSE" if enable else "REST"
    return True


def enable_cont_rig_gpencil(obj: bpy.types.Object, enable: bool):
    armature_constraint = get_armature_constraint(obj)
    # Reset Rig
    enable_armature_constraint(armature_constraint, enable)
    # Disable Time Offset Modifiers
    gpencil_fix_offset_show_viewport(obj, enable)
    enable_lattice_mod(obj, enable)


def enable_mod_rig_gpencil(obj: bpy.types.Object, enable: bool):
    armature_mod = get_grease_pencil_modifiers(obj, "GP_ARMATURE")
    # Reset Rig
    enable_gpencil_armature_modifier(armature_mod, enable)
    # Disable Time Offset Modifiers
    gpencil_fix_offset_show_viewport(obj, enable)
    enable_lattice_mod(obj, enable)
    return True


def hide_grease_pencil_editor(obj: bpy.types.Object, enable: bool):
    armature_mod = get_grease_pencil_modifiers(obj, "GP_ARMATURE")
    if armature_mod:
        return enable_mod_rig_gpencil(obj, enable)
    armature_constraint = get_armature_constraint(obj)
    if armature_constraint:
        return enable_cont_rig_gpencil(obj, enable)


def armature_bones_rename(armature: bpy.types.Armature, bone_legend: dict) -> str:
    """bone_legend must be in {'old_name': 'new_name',} format"""
    updated_bones = ""
    for bone in armature.bones:
        if bone.name in bone_legend:
            updated_bones += f"{bone.name},"
            bone.name = bone_legend[bone.name]

    return f"Bones Renamed: {updated_bones} \n"


def custom_int_create_timeoffset(
    target: bpy.types.PoseBone, name: str, value: int, min: int, max: int
):
    custom_int_create(target, name, value, min, max)
    target.id_data.tiny_rig.user_props += name


def custom_int_create(
    target: bpy.types.PoseBone, name: str, value: int, min: int, max: int
) -> str:
    target[name] = value
    id_props = target.id_properties_ui(name)
    id_props.update(
        min=min,
        max=max,
        default=1,
    )
    target.property_overridable_library_set(f'["{name}"]', True)
    return target[name]


def bone_create_group(obj: bpy.types.Object, bone_group_name: str, color: str) -> bool:
    """bone_groups must be in {'name': color_set',} format"""
    status = False
    try:
        obj.pose.bone_groups[bone_group_name]
    except KeyError:
        group = obj.pose.bone_groups.new(name=bone_group_name)
        group.color_set = color
        status = True
    return status


def bone_assign_group(bone: bpy.types.PoseBone, bone_group_name: str):
    """bone_assignments must be in {'bone_name': group_name',} format"""
    obj = bone.id_data
    bone.bone_group = obj.pose.bone_groups[bone_group_name]
    obj.data.show_group_colors = True


def bone_transform_mirror_add(bone: bpy.types.PoseBone, name="FLIP_BONE"):
    """bone must be hand or foot bone"""
    rig_prefs = get_rig_prefs()
    prefix = bone_side_prefix_get(bone.name, rig_prefs)
    limb = bone_limb_get(bone.name, rig_prefs)
    new = bone.constraints.new("TRANSFORM")
    new.name = name
    new.target = bone.id_data
    new.subtarget = f"{bone.name.split('.')[0]}_Nudge"
    new.target_space = "LOCAL_WITH_PARENT"
    new.owner_space = "LOCAL_WITH_PARENT"
    new.map_to = "ROTATION"
    new.to_min_y_rot = 3.1415927410125732
    add_driver(
        bone.id_data,
        bone.id_data,
        f"{prefix}{limb}{rig_prefs.flip}",
        f'pose.bones["{bone.name}"].constraints["{new.name}"].influence',
        f'pose.bones["{bone.id_data.tiny_rig.pose_data_name}"]["{prefix}{limb}{rig_prefs.flip}"]',
    )


def bone_transform_nudge_add(
    bone: bpy.types.PoseBone, name="HAND_NUDGE"
) -> bpy.types.Constraint:
    """Bone must be a hand or Foot"""
    rig_prefs = get_rig_prefs()
    prefix = bone_side_prefix_get(bone.name, rig_prefs)
    limb = bone_limb_get(bone.name, rig_prefs)
    constraint = bone.constraints.new("TRANSFORM")
    constraint.target = bone.id_data
    constraint.subtarget = f"{prefix}{limb}{rig_prefs.nudge}"
    constraint.target_space = "LOCAL"
    constraint.owner_space = "LOCAL"
    constraint.to_min_z = -0.05
    constraint.name = name
    add_driver(
        bone.id_data,
        bone.id_data,
        f'{prefix}{rig_prefs.hand}{rig_prefs.nudge}',
        f'pose.bones["{bone.name}"].constraints["{constraint.name}"].influence',
        f'pose.bones["{bone.id_data.tiny_rig.pose_data_name}"]["{prefix}{rig_prefs.hand}{rig_prefs.nudge}"]',
    )
    return constraint


def bone_copy_location_limb(
    context, bone, driver=True, name="COPY_LIMB_LOC"
) -> bpy.types.Constraint:
    """Copy location of Lw bone to IK Target bone"""
    rig_prefs = get_rig_prefs()
    prefix = bone_side_prefix_get(bone.name, rig_prefs)
    limb = bone_limb_get(bone.name, rig_prefs)
    mod_type = "COPY_LOCATION"
    constraint = bone.constraints.new(mod_type)
    constraint.name = name
    constraint.target = bone.id_data
    constraint.subtarget = f"{prefix}{limb}{rig_prefs.limb_lw}"
    constraint.target_space = "POSE"
    constraint.owner_space = "POSE"
    constraint.head_tail = 1.0
    constraint.use_bbone_shape = False
    constraint.use_x = True
    constraint.use_y = False
    constraint.use_z = True

    if driver:
        expression = f"{bone.name} == 0"
        add_driver(
            bone.id_data,
            bone.id_data,
            bone.name,
            f'pose.bones["{bone.name}"].constraints["{constraint.name}"].influence',
            f'pose.bones["{context.scene.property_bone_name}"]["{bone.name}"]',
            -1,
            expression,
        )
    return constraint


def add_ik_flip_to_pole(
    bone: bpy.types.PoseBone, nudge_bone_name, name="IK_FLIP"
) -> bpy.types.Constraint:
    constraint = bone.constraints.new("TRANSFORM")
    constraint.name = name
    constraint.target = bone.id_data
    constraint.subtarget = nudge_bone_name
    constraint.target_space = "LOCAL"
    constraint.owner_space = "LOCAL"
    constraint.to_min_y = -4.5
    return constraint


def get_nudge_bone_name(bone):
    rig_prefs = get_rig_prefs()
    prefix = bone_side_prefix_get(bone.name, rig_prefs)
    limb = bone_limb_get(bone.name, rig_prefs)
    return f"{prefix}{limb}{rig_prefs.nudge}"


def copy_ik_rotation(bone: bpy.types.PoseBone, target_name, name="COPY_IK_ROT"):
    mod_type = "COPY_ROTATION"
    constraint = bone.constraints.new(mod_type)
    constraint.name = name
    constraint.target = bone.id_data

    constraint.subtarget = target_name


def bone_copy_location_nudge(
    bone: bpy.types.PoseBone, space="POSE", offset=False, name="COPY_NUDGE_LOC"
) -> bpy.types.Constraint:
    """Copy Location from Limb's 'Nudge' Bone"""
    nudge_bone_name = get_nudge_bone_name(bone)
    mod_type = "COPY_LOCATION"
    constraint = bone.constraints.new(mod_type)
    constraint.name = name
    constraint.target = bone.id_data
    constraint.subtarget = nudge_bone_name
    constraint.target_space = space
    constraint.owner_space = space
    constraint.head_tail = 0.0
    constraint.use_bbone_shape = False
    constraint.use_x = False
    constraint.use_y = True
    constraint.use_z = False
    constraint.use_offset = offset
    return constraint


def bone_ik_driver_add(
    bone: bpy.types.PoseBone,
    constraint: bpy.types.Constraint,
    propbone: bpy.types.PoseBone,
    ik_prop_name: str,
):
    """Add Driver to IK's Influence"""
    custom_int_create(propbone, ik_prop_name, 1, 0, 1)
    add_driver(
        bone.id_data,
        bone.id_data,
        ik_prop_name,
        f'pose.bones["{bone.name}"].constraints["{constraint.name}"].influence',
        f'pose.bones["{propbone.name}"]["{ik_prop_name}"]',
        -1,
    )
    return


def bone_ik_constraint_add(
    bone: bpy.types.PoseBone, prefix: str, limb: str, rig_prefs: bpy.types.PropertyGroup
):
    """Add IK Constrain on Lw Bone, with Target + Pole"""
    # angle = (0 if bone.name(".").split[0] else 180)
    constraint = bone.constraints.new("IK")
    constraint.target = bone.id_data
    constraint.subtarget = f"{prefix}{limb}{rig_prefs.ik}"
    constraint.pole_target = bone.id_data
    constraint.pole_subtarget = f"{prefix}{limb}{rig_prefs.pole}"
    # constraint.pole_angle = angle
    constraint.chain_count = 2
    constraint.use_tail = True
    return constraint


def bone_position_limits_add(
    bone: bpy.types.PoseBone, name="Nudge - Limit Location"
) -> bpy.types.Constraint:
    """Position Limits on Limb's 'Nudge' Bone"""
    constraint = bone.constraints.new("LIMIT_LOCATION")
    constraint.owner_space = "LOCAL"
    constraint.use_min_z = True
    constraint.use_max_z = True
    constraint.min_z = -0.1
    constraint.max_z = 0.1
    constraint.name = name
    return constraint


def bone_check_constraint(bone: bpy.types.PoseBone, name: str) -> bool:
    constraint_names = [item.name for item in bone.constraints]
    return bool(name in constraint_names)


def bone_new(
    edit_bones,
    name: str,
    head,
    tail,
    global_y=0,
):
    bone = edit_bones.new(name)
    # a new bone will have zero length and not be kept
    # move the head/tail to keep the bone
    bone.head = (head[0], global_y, head[1])
    bone.tail = (tail[0], global_y, tail[1])
    return bone


def child_bone_new(
    parent_bone: bpy.types.EditBone,
    name: str,
    head,
    tail,
):
    bone = bone_new(parent_bone.id_data.edit_bones, name, head, tail)
    bone.parent = parent_bone
    return bone


def child_bone_connected_new(
    parent_bone: bpy.types.EditBone,
    name: str,
    tail,
):
    head = parent_bone.tail.xz
    bone = bone_new(parent_bone.id_data.edit_bones, name, head, tail)
    bone.parent = parent_bone
    bone.use_connect = True
    return bone


def make_nudge(parent_bone, prefix, limb, up_limb_head):
    rig_prefs = get_rig_prefs()
    new_head = (up_limb_head[0], up_limb_head[1] + 0.1)
    tail = (new_head[0] - 0.1, new_head[1])
    return child_bone_new(
        parent_bone, f'{prefix}{limb}{rig_prefs.nudge}', new_head, tail
    )


def make_limb(
    parent_bone: bpy.types.EditBone,
    prefix: str,
    limb: str,
    origin,
    angle: int,
    appendage_angle: int,
):
    rig_prefs = get_rig_prefs()
    limb_up = child_bone_new(
        parent_bone,
        f'{prefix}{limb}{rig_prefs.limb_up}',
        origin,
        calculate_bone_vector(0.6, origin, angle),
    )
    limb_lw = child_bone_connected_new(
        limb_up,
        f'{prefix}{limb}{rig_prefs.limb_lw}',
        calculate_bone_vector(0.7, limb_up.tail.xz, angle * 0.98),
    )
    limb_appendage = child_bone_connected_new(
        limb_lw,
        f'{prefix}{limb}.{get_appendage_name(limb)}',
        calculate_bone_vector(0.2, limb_lw.tail.xz, appendage_angle),
    )
    return [limb_up, limb_lw, limb_appendage]


def calculate_bone_vector(length, origin, angle=0):
    x = length * math.sin(math.radians(angle)) + origin[0]
    y = length * math.cos(math.radians(angle)) + origin[1]
    return (x, y)


def calculate_bone_angle(p2, p1):
    return math.degrees(math.atan2((p2[0] - p1[0]), (p2[1] - p1[1])))


def make_nudge_bone(
    nudge_parent,
    prefix: str,
    limb: str,
    origin,
):
    rig_prefs = get_rig_prefs()
    new_head = (origin[0], origin[1] + 0.1)
    tail = (new_head[0] - 0.1, new_head[1])
    return child_bone_new(
        nudge_parent, f'{prefix}{limb}{rig_prefs.nudge}', new_head, tail
    )


def get_appendage_name(limb):
    rig_prefs = get_rig_prefs()
    if limb == rig_prefs.leg:
        return rig_prefs.foot
    if limb == rig_prefs.arm:
        return rig_prefs.hand


def make_limb_chain(
    parent_bone: bpy.types.EditBone,
    prefix: str,
    limb: str,
    origin,
    angle: int,
    appendage_angle: int,
    use_make_nudge=True,
    use_make_iks=True,
    use_mirror=False,
):
    angle_mirror = 1
    if use_mirror:
        angle_mirror = -1
    angle = angle * angle_mirror
    appendage_angle = appendage_angle * angle_mirror

    if use_make_nudge:
        parent_bone = make_nudge_bone(parent_bone, prefix, limb, origin)
    limbs = make_limb(parent_bone, prefix, limb, origin, angle, appendage_angle)
    return limbs


def make_limb_set(
    parent,
    limb,
    origin,
    angle: int,
    appendage_angle: int,
    use_make_nudge=True,
    make_ik_bones=True,
):
    rig_prefs = get_rig_prefs()
    l_limbs = make_limb_chain(
        parent_bone=parent,
        prefix=rig_prefs.l_side,
        limb=limb,
        origin=origin,
        angle=angle,
        appendage_angle=appendage_angle,
        use_make_nudge=use_make_nudge,
        use_make_iks=make_ik_bones,
        use_mirror=False,
    )
    r_limbs = make_limb_chain(
        parent_bone=parent,
        prefix=rig_prefs.r_side,
        limb=limb,
        origin=[-origin[0], origin[1]],
        angle=angle,
        appendage_angle=appendage_angle,
        use_make_nudge=use_make_nudge,
        use_make_iks=make_ik_bones,
        use_mirror=True,
    )


def create_bones_ik(
    parent_bone: bpy.types.PoseBone, limb_bone: bpy.types.PoseBone, use_mirror=False
):
    rig_prefs = get_rig_prefs()
    prefix = bone_side_prefix_get(limb_bone.name, rig_prefs)
    limb = bone_limb_get(limb_bone.name, rig_prefs)
    root_bone = parent_bone
    mirror_mult = 1 if prefix == rig_prefs.r_side else -1
    if limb == rig_prefs.leg:
        root_bone = parent_bone.id_data.edit_bones[0]

    limb_angle = calculate_bone_angle(
        (limb_bone.tail.xz[0], limb_bone.tail.xz[1]),
        (limb_bone.head.xz[0], limb_bone.head.xz[1]),
    )

    ik_offset = calculate_bone_vector(
        1, (limb_bone.head.xz[0], limb_bone.head.xz[1]), (limb_angle)
    )

    ik_bone = child_bone_new(
        root_bone,
        f"{prefix}{limb}{rig_prefs.ik}",
        ik_offset,
        calculate_bone_vector(0.2, ik_offset, limb_angle),
    )

    pole_offset = calculate_bone_vector(
        2,
        (limb_bone.head.xz[0], limb_bone.head.xz[1]),
        (limb_angle + (90 * mirror_mult)),
    )
    pole_bone = child_bone_new(
        parent_bone,
        f"{prefix}{limb}{rig_prefs.pole}",
        pole_offset,
        calculate_bone_vector(0.2, pole_offset, (limb_angle + (90 * mirror_mult))),
    )
    return [ik_bone, pole_bone]
