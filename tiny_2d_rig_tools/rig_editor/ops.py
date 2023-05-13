from tiny_2d_rig_tools.rig_editor.prefs import (
    get_ik_control_bools,
    get_ik_mod_bones,
    get_appendage_bones,
    bone_side_prefix_get,
    bone_limb_get,
)

from tiny_2d_rig_tools.core_functions.label import split_lines

from tiny_2d_rig_tools.core_functions.drivers import add_driver, get_driver_ob_obj
from tiny_2d_rig_tools.rig_editor.core import (
    get_action_offset_bones,
    set_modifier_and_constraint_viewport,
    bone_create_group,
    bone_assign_group,
    bone_ik_driver_add,
    bone_transform_mirror_add,
    bone_transform_nudge_add,
    bone_copy_location_nudge,
    bone_copy_location_limb,
    bone_ik_constraint_add,
    bone_position_limits_add,
    bone_check_constraint,
    add_ik_flip_to_pole,
    get_nudge_bone_name,
    copy_ik_rotation,
    custom_int_create,
    custom_int_create_timeoffset,
    bone_new,
    child_bone_new,
    child_bone_connected_new,
    calculate_bone_vector,
    make_limb_set,
    create_bones_ik,
)
from tiny_2d_rig_tools.core_functions.bone import (
    get_consts_on_bone,
    reset_bones,
    show_hide_constraints,
)
from tiny_2d_rig_tools.core_functions.object import get_gp_modifier, get_vertex_group
import bpy


# Imports data that should be read from a JSON file or other imported text format.


class TINY2DRIG_rig_edit_base_class(bpy.types.Operator):
    """Base Class for all Rig Edit Operations"""

    @classmethod
    def poll(cls, context):
        if context.active_object is None:
            return cls.poll_message_set("No Object is Active")
        obj = context.active_object
        res = not (obj.library or obj.override_library)
        if not res:
            cls.poll_message_set("Cannot Edit Reference Objects")
        return res


class TINY2DRIG_rig_gp_base_class(bpy.types.Operator):
    """Base Class for all Rig Edit Operations"""

    @classmethod
    def poll(cls, context):
        if not context.view_layer.objects.active:
            return cls.poll_message_set("No Object is Active")
        obj = context.view_layer.objects.active
        if not context.scene.target_armature:
            return cls.poll_message_set("Target Armature is not active")
        if not context.scene.property_bone_name:
            return cls.poll_message_set("Property Bone is not set")
        if not (obj.type == "GPENCIL"):
            return cls.poll_message_set("Active object is not Grease Pencil")
        return True


class TINY2DRIG_turnaround_base_class(bpy.types.Operator):
    """Base Class for all Rig Edit Operations"""

    @classmethod
    def poll(cls, context):
        if not context.active_object:
            return cls.poll_message_set("Object must be active")
        if context.active_object.mode != "POSE":
            return cls.poll_message_set("Mode is not POSE")
        if not context.scene.target_armature:
            return cls.poll_message_set("Target Armature is not active")
        if not context.scene.target_armature.offset_action:
            return cls.poll_message_set("Offset Action is not active")
        if context.scene.property_bone_name == "":
            return cls.poll_message_set("Property Bone is not set")
        if context.active_object != context.scene.target_armature:
            return cls.poll_message_set(
                f"{context.scene.target_armature.name} is not active Object"
            )

        else:
            return True


class TINY2DRIG_gp_set_mod_const(bpy.types.Operator):
    bl_idname = "tiny2drig.enable_gp_mod_const"
    bl_label = "Toggle Visability of All Modifiers & Constraints"
    bl_description = "Enable/Disable visablitiy of modifiers and constraints on grease pencil active object"
    bl_options = {"REGISTER", "UNDO"}

    enabled: bpy.props.BoolProperty(name="Enabled")

    @classmethod
    def poll(cls, context):
        if (
            len(context.active_object.grease_pencil_modifiers) == 0
            and len(context.active_object.constraints) == 0
        ):
            cls.poll_message_set("Object has no Modifiers or Constraints")
            return False
        return True

    def execute(self, context):
        set_modifier_and_constraint_viewport(context.active_object, self.enabled)
        self.report({"INFO"}, f"All Modifiers and Constraints are {self.enabled}!")
        return {"FINISHED"}


class TINY2DRIG_gp_set_mod_const_all(bpy.types.Operator):
    bl_idname = "tiny2drig.enable_all_gp_mod_const_all"
    bl_label = "Unhide all Modifers & Constraints"
    bl_description = "Ensure Modifers and Constraints are visable/enabled on all grease pencil objects"
    bl_options = {"REGISTER", "UNDO"}

    enabled: bpy.props.BoolProperty(name="Enabled")

    def execute(self, context):
        for obj in [obj for obj in context.scene.objects if obj.type == "GPENCIL"]:
            set_modifier_and_constraint_viewport(obj, True)
        self.report({"INFO"}, f"Modifiers and Constraints on all objects are enabled")
        return {"FINISHED"}


class TINY2DRIG_OT_create_armatue(bpy.types.Operator):
    bl_idname = "tiny2drig.create_2d_armature"
    bl_label = "Create Armature"
    bl_description = "Create a new base armature object, matching conventions set in armature preferences."
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if context.scene.target_armature:
            return cls.poll_message_set("Target Armature already Set")
        return True

    def execute(self, context):
        rig_prefs = context.window_manager.tiny_rig_prefs
        bpy.ops.object.armature_add(enter_editmode=True)
        # must be in edit mode to add bones
        arm_obj = context.active_object

        edit_bones = arm_obj.data.edit_bones

        # Clear Existing Bone
        for bone in edit_bones:
            edit_bones.remove(bone)

        # Create root bones
        master_bone = bone_new(
            edit_bones, rig_prefs.master_bone, (-0.3, -0.5), (0.3, -0.5)
        )
        # Create Spine Bones
        spine_root = (0, 0.8)
        spine_root = child_bone_new(
            master_bone,
            rig_prefs.spine_root,
            spine_root,
            calculate_bone_vector(0.3, spine_root),
        )
        lower_offset = (spine_root.tail.xz[0], (spine_root.tail.xz[1] + 0.1))
        lower = child_bone_new(
            spine_root,
            rig_prefs.spine_lower,
            lower_offset,
            calculate_bone_vector(0.7, lower_offset),
        )
        upper = child_bone_connected_new(
            lower, rig_prefs.spine_upper, calculate_bone_vector(0.7, lower.tail.xz)
        )
        neck = child_bone_new(
            upper,
            rig_prefs.spine_neck,
            upper.tail.xz,
            calculate_bone_vector(0.2, upper.tail.xz),
        )

        make_limb_set(
            parent=upper,
            limb=rig_prefs.arm,
            origin=(0.5, 2.5),
            angle=130,
            appendage_angle=130,
            use_make_nudge=True,
            make_ik_bones=True,
        )
        make_limb_set(
            parent=lower,
            limb=rig_prefs.leg,
            origin=(0.2, 1.4),
            angle=180,
            appendage_angle=180 - 45,
            use_make_nudge=True,
            make_ik_bones=True,
        )

        # Select all bones to recalculate roll
        for bone in edit_bones:
            bone.select = True
        bpy.ops.armature.calculate_roll(
            type='GLOBAL_POS_Y', axis_flip=False, axis_only=False
        )
        bpy.ops.object.mode_set(mode='POSE')
        context.scene.target_armature = arm_obj

        self.report({"INFO"}, "Created Armature")
        return {"FINISHED"}


class TINY2DRIG_initialize_rig(bpy.types.Operator):
    bl_idname = "tiny2drig.initialize_rig"
    bl_label = "Initialize Armature"
    bl_description = "Create Drivers and Custom Properties on current Armature for use in Tiny Rig Control panel"
    bl_options = {"REGISTER", "UNDO"}

    pose_length_set: bpy.props.IntProperty(name="Turnaround Length", default=3)
    update_face_constraints: bpy.props.BoolProperty(
        name="Add Face Constraints", default=False
    )
    set_turnaround: bpy.props.BoolProperty(
        name="Turnaround",
        default=False,
        description="Set Length of Pose Turnaround. Drives Body and Head position for action constraints and time offset modifiers",
    )
    create_limb_iks: bpy.props.BoolProperty(
        name="Create IK & Pole Bones",
        default=True,
        description="Create IK and Pole Bones based on current limb positions",
    )

    set_ik_modifiers: bpy.props.BoolProperty(
        name="Setup IK Constraints & Drivers",
        default=True,
        description="Set Modifiers & Drivers for Rig's Inverse Kinematics",
    )
    set_base_time_offset_props: bpy.props.BoolProperty(
        name="Setup Basic Time Offset Properties",
        default=True,
        description="Create Standard Mouth and Hand Time Offset Modifiers",
    )
    set_appendage_flip: bpy.props.BoolProperty(
        name="Setup Mirror for Hands & Feet",
        default=True,
        description="Set Modifier and Driver to Mirror/Flip Hand/Foot bones",
    )
    set_bone_groups: bpy.props.BoolProperty(
        name="Setup Bone Groups",
        default=True,
        description="Setup Bone Groups based on naming conventions",
    )
    set_bone_rotation_locks: bpy.props.BoolProperty(
        name="Lock Bone Rotation",
        default=True,
        description="Set Rotations to Euler 'XYZ' with only 'Z' Axis unlocked",
    )
    set_bone_roll: bpy.props.BoolProperty(
        name="Set Bone Roll",
        default=True,
        description="Set Bone Roll for all bones to 'GLOBAL_POS_Y'",
    )

    def create_sub_box(self, layout, bool):
        if bool:
            return layout.box()
        else:
            return layout

    @classmethod
    def poll(cls, context):
        if not context.scene.property_bone_name:
            cls.poll_message_set("Set a Property Bone before Intilization")
        return context.scene.property_bone_name

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self, context):
        split_lines(
            context,
            "This can break animation track compatibility.",
            self.layout,
            0.056,
            icon="ERROR",
        )
        box = self.layout.box()
        col = box.column(align=False)
        col.prop(self, "set_base_time_offset_props")
        col.prop(self, "set_appendage_flip")
        col.prop(self, "set_bone_groups")
        col.prop(self, "set_bone_rotation_locks")
        col.prop(self, "set_bone_roll")
        col.prop(self, "set_ik_modifiers")
        col.prop(self, "create_limb_iks")

        turnaround_box = self.create_sub_box(col, self.set_turnaround)
        turnaround_box.prop(self, "set_turnaround")
        if self.set_turnaround:
            turnaround_box.prop(self, "pose_length_set", text="Turnaround Length")
        col = self.layout.column(align=True)

        col.label(text="Use 'ESC' to cancel")

    def execute(self, context):
        # TODO Make safe to re-run (collect related bones clear and reset)
        obj = context.active_object
        if context.scene.property_bone_name is None:
            self.report({"ERROR"}, f"Set Property Bone")
            return {"CANCELLED"}
        propbone = obj.pose.bones[context.scene.property_bone_name]
        obj.tiny_rig.is_rig = True
        obj.tiny_rig.pose_data_name = context.scene.property_bone_name

        # LISTS
        rig_prefs = context.window_manager.tiny_rig_prefs
        appendage_bones = get_appendage_bones(rig_prefs)

        if self.set_base_time_offset_props:
            custom_int_create_timeoffset(propbone, "Mouth", 1, 1, 100)
            custom_int_create(propbone, f"{rig_prefs.r_side}{rig_prefs.hand}", 1, 1, 50)
            custom_int_create(propbone, f"{rig_prefs.l_side}{rig_prefs.hand}", 1, 1, 50)

        if self.set_appendage_flip:
            for property in (
                f'{rig_prefs.r_side}{rig_prefs.hand}{rig_prefs.flip}',
                f'{rig_prefs.l_side}{rig_prefs.hand}{rig_prefs.flip}',
                f'{rig_prefs.r_side}{rig_prefs.foot}{rig_prefs.flip}',
                f'{rig_prefs.l_side}{rig_prefs.foot}{rig_prefs.flip}',
            ):
                prop = custom_int_create(propbone, property, 1, 0, 1)

        if self.create_limb_iks:
            obj.tiny_rig.is_ik = True
            ik_control_bools = get_ik_control_bools(
                context.window_manager.tiny_rig_prefs
            )
            for index, item in enumerate(ik_control_bools):
                custom_int_create(propbone, ik_control_bools[index], 1, 0, 1)

            # TODO only clear constraitns for needed bones
            for bone in [bone for bone in obj.pose.bones if bone.constraints]:
                for constraint in bone.constraints:
                    bone.constraints.remove(constraint)

            bpy.ops.object.mode_set(mode='EDIT')

            for hand_bone in [
                bone for bone in obj.data.edit_bones if bone.name in appendage_bones
            ]:
                hand_bone.parent = None
                hand_bone.select = True

            for bone in [
                bone
                for bone in obj.data.edit_bones
                if bone.name in get_ik_mod_bones(context.window_manager.tiny_rig_prefs)
            ]:
                prefix = bone_side_prefix_get(bone.name, rig_prefs)
                limb = bone_limb_get(bone.name, rig_prefs)
                create_bones_ik(
                    obj.data.edit_bones[f"{prefix}{limb}{rig_prefs.nudge}"],
                    bone,
                    rig_prefs,
                )

            bpy.ops.object.mode_set(mode='POSE')

        if self.set_turnaround:
            custom_int_create(propbone, rig_prefs.pose_body, 1, 1, self.pose_length_set)
            custom_int_create(propbone, rig_prefs.pose_head, 1, 1, self.pose_length_set)
            obj.tiny_rig.pose_length = self.pose_length_set
            obj.tiny_rig.is_turnaround = True

        if self.set_bone_groups:
            bone_create_group(obj, rig_prefs.right_bone_group, 'THEME01')
            bone_create_group(obj, rig_prefs.left_bone_group, 'THEME03')
            bone_create_group(obj, rig_prefs.spine_bone_group, 'THEME09')
            for bone in obj.pose.bones:
                prefix = bone_side_prefix_get(bone.name, rig_prefs)
                if prefix == rig_prefs.l_side:
                    bone_assign_group(bone, rig_prefs.left_bone_group)
                if prefix == rig_prefs.r_side:
                    bone_assign_group(bone, rig_prefs.right_bone_group)
                if bone.name in [
                    rig_prefs.spine_lower,
                    rig_prefs.spine_upper,
                    rig_prefs.spine_neck,
                ]:
                    bone_assign_group(bone, rig_prefs.spine_bone_group)

        if self.set_bone_rotation_locks:
            for bone in obj.pose.bones:
                bone.rotation_mode = 'XYZ'
                bone.lock_rotation[0] = True
                bone.lock_rotation[1] = True
                bone.lock_rotation[2] = False
                bone.rotation_mode = 'XYZ'
                bone.lock_rotation[0] = False
                bone.lock_rotation[1] = False
                bone.lock_location[2] = True

        lw_bones = get_ik_mod_bones(context.window_manager.tiny_rig_prefs)
        if self.set_ik_modifiers:
            # Add IK Constraints
            ik_bones = [bone for bone in obj.pose.bones if bone.name in lw_bones]
            for bone in ik_bones:
                prefix = bone_side_prefix_get(bone.name, rig_prefs)
                limb = bone_limb_get(bone.name, rig_prefs)
                if not get_consts_on_bone(bone, "IK"):
                    bone_ik_constraint_add(bone, prefix, limb, rig_prefs)
                constraint = get_consts_on_bone(bone, "IK")[0]
                # Add IK Drivers

                bone_ik_driver_add(
                    bone, constraint, propbone, f"{prefix}{limb}{rig_prefs.ik}"
                )

            # Add IK_Flip to Poles
            for bone in [bone for bone in obj.pose.bones if "Pole" in bone.name]:
                # If nudge pass the corrisponding nudge bone, else pass master bone
                nudge_bone_name = get_nudge_bone_name(bone)
                prefix = bone_side_prefix_get(bone.name, rig_prefs)
                limb = bone_limb_get(bone.name, rig_prefs)
                ik_prop_name = f"{prefix}{limb}{rig_prefs.flip}{rig_prefs.ik}"

                constraint = add_ik_flip_to_pole(bone, nudge_bone_name)
                add_driver(
                    bone.id_data,
                    bone.id_data,
                    ik_prop_name,
                    f'pose.bones["{bone.name}"].constraints["{constraint.name}"].influence',
                    f'pose.bones["{propbone.name}"]["{ik_prop_name}"]',
                    -1,
                )

            # Add Mirror to Hand/Foot Bones
            for bone in [
                bone for bone in obj.pose.bones if bone.name in appendage_bones
            ]:
                bone_copy_location_nudge(bone, 'POSE', True)
                bone_copy_location_limb(context, bone, False)
                prefix = bone_side_prefix_get(bone.name, rig_prefs)
                limb = bone_limb_get(bone.name, rig_prefs)
                target_name = f"{prefix}{limb}{rig_prefs.ik}"
                copy_ik_rotation(bone, target_name)

            # Add Hand Nudge
            for bone in [bone for bone in obj.pose.bones if "Hand" in bone.name]:
                if not bone_check_constraint(bone, "HAND_NUDGE"):
                    bone_transform_nudge_add(bone)

            # Add Position Limits
            for bone in [bone for bone in obj.pose.bones if "Nudge" in bone.name]:
                if not bone_check_constraint(bone, "Nudge - Limit Location"):
                    bone_position_limits_add(bone)

            # IK Ctrl Copy Transforms
            for bone in [bone for bone in obj.pose.bones if "IK" in bone.name]:
                if not bone_check_constraint(bone, "Copy Arm Location"):
                    bone_copy_location_limb(context, bone)
                if not bone_check_constraint(bone, "Copy Nudge Location"):
                    bone_copy_location_nudge(bone)

        if self.set_appendage_flip:
            for bone in [
                bone for bone in obj.pose.bones if bone.name in appendage_bones
            ]:
                bone_transform_mirror_add(bone)

        # add turnaround action
        if obj.offset_action is None and self.set_turnaround:
            action = bpy.data.actions.new(f'{obj.name}_TURNAROUND')
            obj.offset_action = action

        if self.set_bone_roll:
            bpy.ops.object.mode_set(mode='EDIT')
            for bone in obj.data.edit_bones:
                bone.select = True
            bpy.ops.armature.calculate_roll(
                type='GLOBAL_POS_Y', axis_flip=False, axis_only=False
            )
            bpy.ops.object.mode_set(mode='POSE')

        self.report({"INFO"}, f"Initilizaton Completed!")
        return {"FINISHED"}


old_action = None


class TINY2DRIG_toggle_enable_action(TINY2DRIG_turnaround_base_class):
    bl_idname = "tiny2drig.enable_offset_action"
    bl_label = "Edit Turnaround Action"
    bl_description = "Set turnaround action from target armature as the active action and hide all action constraints to allow easy editing of turnaround"
    bl_options = {"REGISTER", "UNDO"}

    enable: bpy.props.BoolProperty(name="Enable Turnaround Action Editor")

    def execute(self, context):
        obj = context.active_object
        offset_action = obj.offset_action
        if not offset_action:
            self.report({"ERROR"}, "Turnaround Action not Set")
            return {"CANCELLED"}
        if obj.mode != "POSE":
            self.report({"ERROR"}, "Must be in POSE Mode")
            return {"CANCELLED"}
        global old_action

        if self.enable == True:
            old_action = obj.animation_data.action
            obj.animation_data.action = None
            reset_bones(obj.pose.bones)
            constraints = get_action_offset_bones(obj.pose.bones)
            show_hide_constraints(constraints, False)
            obj.animation_data.action = offset_action
            context.window_manager.offset_editor_active = True
            self.report({"INFO"}, "Turnaround Editing Enabled!")
        else:
            obj = context.active_object
            offset_action = obj.offset_action
            if not offset_action:
                self.report({"ERROR"}, "Turnaround Action not Set")
                return {"CANCELLED"}
            if not obj.animation_data.action == offset_action:
                self.report({"ERROR"}, "Turnaround Action not Enabled")
                return {"CANCELLED"}
            obj.animation_data.action = None
            reset_bones(obj.pose.bones)
            constraints = get_action_offset_bones(obj.pose.bones)
            show_hide_constraints(constraints, True)
            context.window_manager.offset_editor_active = False
            if old_action is not None:
                obj.animation_data.action = old_action
            self.report({"INFO"}, "Turnaround Editing Disabled!")
        return {"FINISHED"}


class TINY2DRIG_load_action(TINY2DRIG_turnaround_base_class):
    bl_idname = "tiny2drig.load_action"
    bl_label = "Refresh Offset Action"
    bl_description = "Get Action data-block from target armature's constraints"
    bl_options = {"UNDO"}

    def execute(self, context):
        actions = []
        for bone in context.active_object.pose.bones:
            for const in get_consts_on_bone(bone, "ACTION"):
                if const.action not in actions:
                    actions.append(const.action)
        # There should only be one action on action constraints for tiny rigs
        if len(actions) != 1:
            self.report(
                {"ERROR"},
                f"Found '{len(actions)}' Actions on action constraints in armature. Expected only one.",
            )
            return {"CANCELLED"}
        context.active_object.offset_action = actions[0]
        return {"FINISHED"}


class TINY2DRIG_add_action_const_to_bone(TINY2DRIG_turnaround_base_class):
    bl_idname = "tiny2drig.add_action_const_to_bone"
    bl_label = "Add Offset to Selected Bones"
    bl_description = """If a bone is included in the active_object's 'Offset Action' add constraint to move bone via action constraint. This will also add a driver back to the Body/Head Poses"""
    bl_options = {"UNDO"}

    is_head: bpy.props.BoolProperty(
        name="Use Head Pose",
        description="Set selected bone(s) as Head Turnaround and create a Head Pose Action Offset. Else Body Action Offset",
    )

    @classmethod
    def poll(cls, context):
        if not context.active_pose_bone:
            return cls.poll_message_set("Pose Bone is not selected")
        if context.window_manager.offset_editor_active == True:
            return cls.poll_message_set(
                "Cannot Edit while Offsetting Turnaround Action"
            )
        return True

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self, context):
        row = self.layout.row(align=True)
        row.label(text="Offset Driver Source:")
        row.prop(
            self,
            "is_head",
            toggle=True,
            text=("Use Pose" if self.is_head else "Use Head Pose"),
        )

    def execute(self, context):
        rig_prefs = context.window_manager.tiny_rig_prefs
        if self.is_head:
            data_path = rig_prefs.pose_head
        else:
            data_path = rig_prefs.pose_head

        action_length = int(context.active_object.offset_action.frame_range[1])
        for bone in context.selected_pose_bones:
            if not get_consts_on_bone(bone, "ACTION"):
                new = bone.constraints.new("ACTION")
                new.action = bone.id_data.offset_action
                new.use_eval_time = True
                add_driver(
                    bone.id_data,
                    bone.id_data,
                    "Pose_Head",
                    f'pose.bones["{bone.name}"].constraints["{new.name}"].eval_time',
                    f'pose.bones["{bone.id_data.tiny_rig.pose_data_name}"]["{data_path}"]',
                    -1,
                    f"Pose_Head/{action_length}",
                )
                new.frame_end = action_length
        return {"FINISHED"}


class TINY2DRIG_add_custom_prop(TINY2DRIG_rig_edit_base_class):
    bl_idname = "tiny2drig.add_custom_prop"
    bl_label = "Add Custom Property"
    bl_description = """Create a Custom Integer Property. This Property can be used to control a driver on modifiers like Time Offset"""
    bl_options = {"UNDO"}

    name: bpy.props.StringProperty(name="Name")
    default: bpy.props.IntProperty(name="Default", default=1)
    min: bpy.props.IntProperty(name="Min", default=1)
    max: bpy.props.IntProperty(name="Max", default=50)

    @classmethod
    def poll(cls, context):
        if not context.scene.target_armature:
            return cls.poll_message_set("Target Armature is not active")
        if context.scene.property_bone_name == "":
            return cls.poll_message_set("Property Bone is not set")
        return True

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self, context):
        self.layout.prop(self, "name")
        self.layout.prop(self, "default")
        self.layout.prop(self, "min")
        self.layout.prop(self, "max")

    def execute(self, context):
        obj = context.scene.target_armature
        prop_bone = obj.pose.bones[context.scene.property_bone_name]
        custom_int_create_timeoffset(
            prop_bone, self.name, self.default, self.min, self.max
        )
        return {"FINISHED"}


class TINY2DRIG_gp_constraint_armature(TINY2DRIG_rig_gp_base_class):
    bl_idname = "tiny2drig.gp_constraint_armature"
    bl_label = "Parent with Armature Contraint"
    bl_description = """Rig the entire active grease pencil object, with an object contraint: Armature"""
    bl_options = {"UNDO"}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self, context):
        self.layout.prop_search(
            context.scene,
            "operator_property_bone_name",
            context.scene.target_armature.id_data.pose,
            "bones",
            text="Bone",
        )

    def execute(self, context):
        obj = context.active_object
        const = obj.constraints.new("ARMATURE")
        const.name = "ARMATURE_CONST"
        obj.parent = context.scene.target_armature
        const.targets.new()
        target_entry = const.targets[-1]
        target_entry.target = context.scene.target_armature
        target_entry.subtarget = context.scene.operator_property_bone_name
        return {"FINISHED"}


class TINY2DRIG_gp_vertex_by_layer(TINY2DRIG_rig_gp_base_class):
    bl_idname = "tiny2drig.gp_vertex_by_layer"
    bl_label = "Parent with Armature Deform"
    bl_description = """Rig Grease Pencil with Armature Modifier. Optionally create empty groups from pose bones in target armature. Optionally assign all strokes (from all frames) in active GP layer to selectd bone"""
    bl_options = {"UNDO"}

    assign_all_vertex_groups: bpy.props.BoolProperty(
        name="Create Empty Groups",
        description="Assign Empty Vertex Groups for all Bones in Armature",
    )
    assign_active_layer: bpy.props.BoolProperty(
        name="Assign Active Grease Pencil to Bone",
        description="Assign all strokes in all frames of Active Grease Pencil Layer to selected Bone",
    )

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self, context):
        self.layout.prop(self, "assign_all_vertex_groups")
        if self.assign_active_layer:
            box = self.layout.box()
        else:
            box = self.layout
        box.prop(self, "assign_active_layer")
        if self.assign_active_layer:
            box.prop_search(
                context.scene,
                "operator_property_bone_name",
                context.scene.target_armature.id_data.pose,
                "bones",
                text="Bone",
            )

    def get_frames(self, context, gp_layer):
        return [frame.frame_number for frame in gp_layer.frames]

    def execute(self, context):
        armature = context.scene.target_armature
        obj = context.active_object
        layer = obj.data.layers.active
        mod = get_gp_modifier(obj, "ARMATURE_MOD", "GP_ARMATURE")
        obj.parent = armature
        mod.object = armature
        user_mode = context.mode
        bpy.ops.object.mode_set(mode='EDIT_GPENCIL')
        bone = context.scene.target_armature.pose.bones[
            context.scene.operator_property_bone_name
        ]
        if self.assign_all_vertex_groups:
            for posebone in armature.pose.bones:
                get_vertex_group(obj, posebone.name)
        if self.assign_active_layer:
            for frame in self.get_frames(context, layer):
                context.scene.frame_set(frame)
                context.scene.tool_settings.gpencil_selectmode_edit = 'POINT'

                vertex_group = get_vertex_group(obj, bone.name)
                obj.vertex_groups.active_index = vertex_group.index
                for other_layer in [
                    pther_layer
                    for pther_layer in obj.data.layers
                    if pther_layer.info != layer.info
                ]:
                    other_layer.lock = True
                layer.lock = False
                bpy.ops.gpencil.select_all(action='SELECT')
                bpy.ops.gpencil.vertex_group_assign()
                bpy.ops.gpencil.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode=user_mode)
        return {"FINISHED"}


class TINY2DRIG_gp_rig_via_lattice(TINY2DRIG_rig_gp_base_class):
    bl_idname = "tiny2drig.gp_rig_via_lattice"
    bl_label = "Parent Object with Lattice Modifier"
    bl_description = """Rig Active Object by Creating Lattice, and adding Vertex Groups from Selected Bone Group. Lattice is deformed with Armature Modifier. Vertex Group/Weights are created but not assigned"""
    bl_options = {"UNDO"}

    def get_bone_group(self, context, armature):
        if context.scene.target_bone_group == "All_Bones":
            return armature.pose.bones
        bone_group = armature.pose.bone_groups[context.scene.target_bone_group]
        return [bone for bone in armature.pose.bones if bone.bone_group == bone_group]

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self, context):
        split_lines(
            context,
            "Add Empty Groups to lattice from bones in group",
            self.layout.column(align=True),
            0.056,
        )
        self.layout.prop(context.scene, "target_bone_group")

    def execute(self, context):
        # Make lattice
        obj = context.active_object
        if obj is None:
            self.report({"ERROR"}, f"Active Object must be a grease pencil")
            return {"CANCELLED"}
        armature = context.scene.target_armature
        obj.parent = armature
        obj.matrix_parent_inverse = armature.matrix_world.inverted()
        lattice = bpy.data.lattices.new("Lattice")
        lattice_ob = bpy.data.objects.new("Lattice", lattice)
        context.collection.objects.link(lattice_ob)
        lattice_ob.data.points_u = 64
        lattice_ob.data.points_v = 1
        lattice_ob.data.points_w = 64
        lattice_ob.parent = obj
        lattice_ob.matrix_parent_inverse = obj.matrix_parent_inverse

        obj_scale = max(obj.dimensions.xyz.to_tuple()) * 1.1
        lattice_ob.scale[0] = obj_scale
        lattice_ob.scale[1] = obj_scale
        lattice_ob.scale[2] = obj_scale
        mod = get_gp_modifier(obj, "LATTICE_MOD", "GP_LATTICE")
        mod.object = lattice_ob
        amr_mod = lattice_ob.modifiers.new(name="ARMATURE_MOD", type="ARMATURE")
        amr_mod.object = armature
        bone_group = self.get_bone_group(context, armature)
        for bone in bone_group:
            get_vertex_group(lattice_ob, bone.name)
        context.view_layer.objects.active = lattice_ob
        self.report({"INFO"}, f"Ready to assign Vetex Groups for {lattice_ob.name}")
        return {"FINISHED"}


class TINY2DRIG_gp_add_time_offset_with_driver(TINY2DRIG_rig_gp_base_class):
    bl_idname = "tiny2drig.gp_add_time_offset_with_driver"
    bl_label = "Add Time Offset with Driver"
    bl_description = """Add Time Offset modifier with Driver from Rig Properties"""
    bl_options = {"UNDO"}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout.column(align=True)
        split_lines(
            context,
            "Add Time Offset Modifier with user property as Driver",
            layout,
            0.056,
        )
        self.layout.prop(context.scene, "target_user_prop", text="Property")

    def execute(self, context):
        # From selected IK Bone
        prop_bone = context.scene.target_armature.pose.bones[
            context.scene.property_bone_name
        ]
        obj = context.active_object
        mod = get_gp_modifier(obj, "GP_TIME", "GP_TIME")
        mod.mode = 'FIX'

        add_driver(
            obj,
            prop_bone.id_data,
            context.scene.target_user_prop,
            f'grease_pencil_modifiers["{mod.name}"].offset',
            f'pose.bones["{context.scene.property_bone_name}"]["{context.scene.target_user_prop}"]',
            -1,
        )
        return {"FINISHED"}


classes = (
    TINY2DRIG_OT_create_armatue,
    TINY2DRIG_add_action_const_to_bone,
    TINY2DRIG_toggle_enable_action,
    TINY2DRIG_load_action,
    TINY2DRIG_initialize_rig,
    TINY2DRIG_gp_set_mod_const,
    TINY2DRIG_gp_set_mod_const_all,
    TINY2DRIG_add_custom_prop,
    TINY2DRIG_gp_constraint_armature,
    TINY2DRIG_gp_vertex_by_layer,
    TINY2DRIG_gp_rig_via_lattice,
    TINY2DRIG_gp_add_time_offset_with_driver,
)


def register():
    for i in classes:
        bpy.utils.register_class(i)


def unregister():
    for i in classes:
        bpy.utils.unregister_class(i)
