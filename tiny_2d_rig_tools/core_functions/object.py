import bpy


def check_object_type(obj: bpy.types.Object, type: str) -> bool:
    if obj.type == type:
        return True


def get_consts_on_obj(obj: bpy.types.Object, type: str) -> list:
    return [constraint for constraint in obj.constraints if constraint.type == type]

def get_gp_modifier(obj, name, type):
    mod = obj.grease_pencil_modifiers.get(name)
    if mod is None:
        mod = obj.grease_pencil_modifiers.new(name= name, type=type)
    return mod

def get_vertex_group(object, name):
    group = object.vertex_groups.get(f'{name}')
    if not group:
        object.vertex_groups.new(name=f'{name}')
        group = object.vertex_groups.get(f'{name}')
    return group