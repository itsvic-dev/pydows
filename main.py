from fluent.views import Image, Acrylic, LayeredView
from fluent.components import Notification

if __name__ == "__main__":
    notification = Notification(
        header=("omame.png", "omame"),
        title="i love drugs",
        body="patryk is fake",
        opaque=False,
    )
    acrylic = Acrylic(notification, color=(15, 15, 15, 128))

    bg_size = (1366, 768)
    notif_size = notification.get_size()
    notif_pos = (bg_size[0] - notif_size[0] - 16, bg_size[1] - notif_size[1] - 12)

    bg = Image("img0.jpg", bg_size)
    view = LayeredView()
    view.add_child(bg, is_main=True)
    view.add_child(acrylic, xy=notif_pos)

    view.paint().show()
