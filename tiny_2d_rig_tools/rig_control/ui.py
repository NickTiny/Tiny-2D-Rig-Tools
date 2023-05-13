import bpy


class TINY2DRIG_PT_rig_control(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_idname = "TINY2DRIG_PT_rig_control"
    bl_label = "Tiny Rig Controller"
    bl_category = "Tiny Rig Control"

    rig_prefs = bpy.props.PointerProperty(type=bpy.types.PropertyGroup)
    prop_bone: bpy.props.PointerProperty(type=bpy.types.PoseBone)

    def draw_nudge_row(self, col, pref_side, limb, nudge_suffix):
        side_str = pref_side.replace('_', '')
        col.label(text=f"{side_str} {limb}")
        nudge_row = col.row(align=True)
        nudge_row.operator(
            "tiny2drig.bone_nudge_backward",
            icon="REMOVE",
            text=f"{side_str} Back",
        ).bone_name = f"{pref_side}{limb}{nudge_suffix}"
        nudge_row.operator(
            "tiny2drig.bone_nudge_forward",
            icon="ADD",
            text=f"{side_str} Forward",
        ).bone_name = f"{pref_side}{limb}{nudge_suffix}"

    def draw_ik_row(self, col, pref_side, limb):
        ik_row = col.row(align=True)
        rig_prefs = self.rig_prefs
        ik_row.prop(
            bpy.context.window_manager.tiny_rig_ui,
            f"{pref_side}{limb}{rig_prefs.ik}",
            icon="CON_KINEMATIC",
            text=f"{pref_side.replace('_','')} {limb} IK",
        )
        ik_row.prop(
            bpy.context.window_manager.tiny_rig_ui,
            f"{pref_side}{limb}{rig_prefs.flip}{rig_prefs.ik}",
            icon="CON_ROTLIKE",
            text="",
        )

    def draw_limb_column(self, col, side):
        bone = self.prop_bone
        rig_prefs = bpy.context.window_manager.tiny_rig_prefs
        # Draw Arm
        arm = rig_prefs.arm
        hand = rig_prefs.hand
        nudge = rig_prefs.nudge
        if bone.id_data.tiny_rig.is_ik:
            self.draw_nudge_row(col, side, arm, nudge)
            self.draw_ik_row(
                col,
                side,
                arm,
            )
        col.separator()
        hand_row = col.row(align=True)
        if bone.id_data.tiny_rig.is_ik:
            hand_row.prop(
                bpy.context.window_manager.tiny_rig_ui,
                f"{side}{hand}{nudge}",
                icon="SORT_DESC",
                text="",
            )
        hand_row.prop(bone, f'["{side}{hand}"]', text=f"{side.replace('_','')} {hand}")
        # Name of UI Props for Mirror are hard coded
        mirror_prop_name = "R_Hand_Flip" if side == rig_prefs.r_side else "L_Hand_Flip"
        hand_row.prop(
            bpy.context.window_manager.tiny_rig_ui,
            mirror_prop_name,
            icon="MOD_MIRROR",
            text="",
        )

        # Draw Leg
        leg = rig_prefs.leg
        if bone.id_data.tiny_rig.is_ik:
            self.draw_nudge_row(col, side, leg, nudge)
            self.draw_ik_row(
                col,
                side,
                leg,
            )
        # Name of UI Props for Mirror are hard coded
        mirror_prop_name = "R_Foot_Flip" if side == rig_prefs.r_side else "L_Foot_Flip"
        col.prop(
            bpy.context.window_manager.tiny_rig_ui,
            mirror_prop_name,
            icon="MOD_MIRROR",
            text=f"Mirror {side.replace('_','')} {rig_prefs.foot}",
        )

    def draw_pose_row(self, layout, name):
        bone = self.prop_bone
        body_offset = 1 if name == self.rig_prefs.pose_body else 0
        pose_row = layout.row(align=True)
        pose_row.operator("tiny2drig.set_turnaround", icon="BACK", text="").values = (
            body_offset * -1,
            -1,
        )
        pose_row.prop(bone, f'["{name}"]')
        pose_row.operator(
            "tiny2drig.set_turnaround", icon="FORWARD", text=""
        ).values = (body_offset, 1)

    def draw(self, context):
        obj = context.active_object
        if not (obj or obj.tiny_rig.get("is_rig")):
            layout.label(text="Rig not Found", icon="ERROR")
            return
        layout = self.layout
        self.prop_bone = obj.pose.bones[obj.tiny_rig.pose_data_name]
        self.rig_prefs = context.window_manager.tiny_rig_prefs
        bone = self.prop_bone

        if bone.get("A. Brow L") and bone.get("A. Brow R"):
            brow_row = layout.row(align=False)
            brow_row.prop(bone, '["A. Brow L"]', text="Left Brow")
            brow_row.prop(bone, '["A. Brow R"]', text="Right Brow")

        layout.separator()

        if bone.id_data.tiny_rig.is_turnaround:
            self.draw_pose_row(layout, self.rig_prefs.pose_head)
            self.draw_pose_row(layout, self.rig_prefs.pose_body)

        for x in bone.keys():
            if x in obj.tiny_rig.user_props:
                layout.prop(bone, f'["{x}"]')

        layout.separator()

        col = layout.column()
        row = col.row()
        split = row.split(factor=0.5)
        left_col = split.column(align=True)
        self.draw_limb_column(left_col, self.rig_prefs.l_side)
        right_col = split.split()
        right_col = right_col.column(align=True)
        self.draw_limb_column(right_col, self.rig_prefs.r_side)


classes = (TINY2DRIG_PT_rig_control,)


def register():
    for i in classes:
        bpy.utils.register_class(i)


def unregister():
    for i in classes:
        bpy.utils.unregister_class(i)
