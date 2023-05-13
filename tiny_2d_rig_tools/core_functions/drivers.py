import bpy


def get_driver_ob_obj(obj: bpy.types.Object) -> list[bpy.types.Driver]:
    if obj.animation_data:
        if obj.animation_data.drivers:
            return obj.animation_data.drivers


def add_driver(source, target, name, prop, dataPath, index=-1, func=""):
    """Add driver to source prop (at index), driven by target dataPath"""

    if index != -1:
        d = source.driver_add(prop, index).driver
    else:
        d = source.driver_add(prop).driver

    for variable in d.variables:
        d.variables.remove(variable)

    v = d.variables.new()
    v.name = name
    v.targets[0].id = target
    v.targets[0].data_path = dataPath

    if func == "":
        d.type = "AVERAGE"
        return
    d.expression = func
    return
