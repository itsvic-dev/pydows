from fluent.views import Image, CachedView, Acrylic
from fluent.components import Notification, TaskBar
from fluent.video import Scene, easing


offset = None


def spawn_notification(bg: Image, scene: Scene, notification: Acrylic, frame_offset=0):
    global offset
    if offset is None:
        offset = bg.get_size()[1] - 40
    end_pos = (
        bg.get_size()[0] - notification.get_size()[0] - 16,
        offset - notification.get_size()[1] - 12,
    )
    start_pos = (
        bg.get_size()[0],
        end_pos[1],
    )

    notif_time = round(0.8 * 60)

    scene.play_audio("fluent/assets/sounds/notify.mp3", after_n_frames=frame_offset)
    scene.add_child(notification, keyframes=easing.do_ease(start_pos, end_pos, notif_time, easing.ease_out_expo),
                    duration=0, after_n_frames=frame_offset, is_async=True)

    offset = end_pos[1] - 12


if __name__ == "__main__":
    bg = Image("img0.jpg", (1920, 1080))
    scene = Scene(bg)
    taskbar = Acrylic(TaskBar(bg.get_size()[0], opaque=False), color=(31, 31, 31, 160))
    scene.add_child(taskbar, position=(0, bg.get_size()[1] - 40), is_async=True)

    notification = Acrylic(CachedView(Notification(
        opaque=False,
        title="testing",
        body="don't mind me lololol"
    )))

    scene.wait_n_frames(30)

    for i in range(10):
        spawn_notification(bg, scene, notification, frame_offset=i * 10)

    scene.wait_n_frames(100 + 90)

    scene.render("test.mp4")
