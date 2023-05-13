from tiny_2d_rig_tools.rig_control import ops, ui, props


def register():
    ops.register()
    ui.register()
    props.register()


def unregister():
    ops.unregister()
    ui.unregister()
    props.unregister()
