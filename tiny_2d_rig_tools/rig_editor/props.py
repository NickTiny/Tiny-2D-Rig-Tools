import bpy


def get_bone_groups(self, context):
    bone_groups = context.scene.target_armature.pose.bone_groups
    items = []
    for bone_group in bone_groups:
          items.append((bone_group.name, bone_group.name, ""))
    items.append(("All_Bones", "All Bones", ""))
    return items


def get_user_propertys(self, context):
    items = []
    obj = context.scene.target_armature
    bone = obj.pose.bones[context.scene.property_bone_name]
    for x in bone.keys():
        if (x in obj.tiny_rig.user_props):
            items.append((f'{x}', f'{x}', f'{x}'))
    return items


def get_pose_bones(self, context):
    return context.scene.target_armature.pose.bones


def get_obj_type_armature(self, object):
    return object.type == "ARMATURE"


def register():
    bpy.types.Scene.target_armature = bpy.props.PointerProperty(
        name="Target Armature", type=bpy.types.Object, poll=get_obj_type_armature, description="Target Armature for Rig Editor. Armature must match naming conventions defined in addon preferences")
    bpy.types.Scene.property_bone_name = bpy.props.StringProperty(name="Property Bone", description="Bone that will contain custom properties, used by Rig Controller")
    bpy.types.WindowManager.offset_editor_active = bpy.props.BoolProperty(
        name="Offset Editor is Active", default=False
    )
    bpy.types.WindowManager.gpencil_editor = bpy.props.PointerProperty(
        type=bpy.types.Object, name="Active Object", description="Name of Active Grease Pencil Object"
    )

    bpy.types.Scene.target_bone_group = bpy.props.EnumProperty(
        name="Bone Group", items=get_bone_groups,)
    bpy.types.Scene.target_user_prop = bpy.props.EnumProperty(
        name="User Properties", items=get_user_propertys)
    bpy.types.Scene.operator_property_bone_name = bpy.props.StringProperty()
    


def unregister():
    del bpy.types.Scene.target_armature
    del bpy.types.Scene.property_bone_name
    del bpy.types.WindowManager.offset_editor_active 
    del bpy.types.WindowManager.gpencil_editor
    del bpy.types.Scene.target_bone_group 
    del bpy.types.Scene.target_user_prop 
    del bpy.types.Scene.operator_property_bone_name
