def offset_current_frame(scene, int):
    return scene.frame_set(scene.frame_current + int)


def refresh_current_frame(scene):
    offset_current_frame(scene, +1)
    offset_current_frame(scene, -1)
    return
