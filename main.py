from fluent.views import Image, Acrylic, LayeredView
from fluent.components import Notification
from fluent.components.task_bar import TaskBar

if __name__ == "__main__":
    notification = Notification(
        header=("omame.png", "omame"),
        title="this isn't windows",
        body="or is it? :thinking:",
        opaque=False,
    )
    acrylic = Acrylic(notification)

    bg_size = (1366, 768)
    notif_size = notification.get_size()
    notif_pos = (bg_size[0] - notif_size[0] - 16, bg_size[1] - notif_size[1] - 12 - 40)

    taskbar = Acrylic(TaskBar(bg_size[0], opaque=False, has_notification=True), color=(15, 15, 15, 160))

    bg = Image("img0.jpg", bg_size)
    view = LayeredView()
    view.add_child(bg, is_main=True)
    view.add_child(taskbar, xy=(0, bg_size[1] - 40))
    view.add_child(acrylic, xy=notif_pos)

    view.paint().show()
