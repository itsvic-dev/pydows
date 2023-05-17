import datetime

from PIL import Image
from enum import Enum
from pydows.helpers import get_font
from pydows.views import Row, View, Text
from pydows.constants import HoloMDL2IconMap, SegoeMDL2IconMap, Font


class TaskBar(View):
    def __init__(self, width: int, opaque=True, notif_slide=0):
        super().__init__()

        self.color = (16, 16, 16, 255)
        self.opaque = opaque
        self.width = width
        self.height = 40

        self.apps = Row(spacing=1)
        self.apps.parent = self

        self.apps.add_child(self.IconApp(HoloMDL2IconMap.WINDOWS))
        self.apps.add_child(self.IconApp(SegoeMDL2IconMap.SEARCH))
        self.apps.add_child(self.IconApp(SegoeMDL2IconMap.TASK_VIEW))

        self.action_center = self.ActionCenterIcon()
        self.action_center.parent = self

        self.time_and_date = self.TimeAndDate()
        self.time_and_date.parent = self

        self.tray = Row(spacing=2, padding=(1, 1))
        self.tray.parent = self

        self.tray.add_child(self.TrayIcon(SegoeMDL2IconMap.ETHERNET))
        self.tray.add_child(self.TrayIcon(SegoeMDL2IconMap.VOLUME_3))

        self.tray_more = self.TrayMore()
        self.tray_more.parent = self

        self.notif_slide = notif_slide

    def get_size(self) -> tuple[int, int] | tuple[float, float]:
        return self.width, self.height

    def paint(self) -> Image.Image:
        size = self.get_size()
        image = Image.new("RGBA", size)

        if self.opaque:
            image.paste(self.color, (0, 0, size[0], size[1]))

        apps_row = self.apps.paint()
        image.alpha_composite(apps_row, (0, 0))

        # right row is way more complex, so let's jump into it
        show_desktop_width = 5
        show_desktop_gap = 8
        x_offset = size[0] - show_desktop_width
        image.alpha_composite(Image.new("RGBA", (1, 40), color=(128, 128, 128, 192)), (x_offset, 0))
        x_offset -= show_desktop_gap

        self.action_center.notif_slide = self.notif_slide
        action_center = self.action_center.paint()
        x_offset -= action_center.size[0]
        image.alpha_composite(action_center, (x_offset, 0))

        time_and_date = self.time_and_date.paint()
        x_offset -= time_and_date.size[0]
        image.alpha_composite(time_and_date, (x_offset, 0))

        tray = self.tray.paint()
        x_offset -= tray.size[0]
        image.alpha_composite(tray, (x_offset, 0))

        tray_more = self.tray_more.paint()
        x_offset -= tray_more.size[0]
        image.alpha_composite(tray_more, (x_offset, 0))

        return image

    class IconApp(View):
        def __init__(self, icon: Enum):
            super().__init__()
            self.is_holo = isinstance(icon, HoloMDL2IconMap)
            self.icon = Text(icon.value,
                             font=get_font(Font.HOLOLENS_MDL2 if self.is_holo else Font.SEGOE_MDL2, size=16)
                             )

        def get_size(self) -> tuple[int, int] | tuple[float, float]:
            return 48, 40

        def paint(self) -> Image.Image:
            image = Image.new("RGBA", self.get_size())

            # draw icon
            icon = self.icon.paint()
            image.alpha_composite(icon, (16, 12))

            return image

    class ActionCenterIcon(View):
        def __init__(self):
            super().__init__()
            self.notif_slide = 0
            self.icon = Text(
                SegoeMDL2IconMap.ACTION_CENTER.value,
                font=get_font(Font.SEGOE_MDL2, size=16)
            )
            self.icon_notif = Text(
                SegoeMDL2IconMap.ACTION_CENTER_NOTIFICATION.value,
                font=get_font(Font.SEGOE_MDL2, size=16)
            )

        def get_size(self) -> tuple[int, int] | tuple[float, float]:
            return 40, 40

        def paint(self) -> Image.Image:
            image = Image.new("RGBA", self.get_size())

            # draw icon
            icon = self.icon.paint()
            image.alpha_composite(icon, (12, 12))
            if self.notif_slide != 0:
                # now draw the notification slide
                slide_width = round(16 * self.notif_slide)
                slide = self.icon_notif.paint().crop((16 - slide_width, 0, 16, 16))
                image.alpha_composite(slide, (12 + (16 - slide_width), 12))

            return image

    class TimeAndDate(View):
        def __init__(self, time=datetime.datetime.now()):
            super().__init__()
            font = get_font(Font.SEGOE_UI, 12)
            self.text = Text(time.strftime("%I:%M %p").lstrip('0') + "\n" +
                             time.strftime("%m/%d/%Y").lstrip('0'), font=font, align="center")
            self.padding = 6

        def get_size(self) -> tuple[int, int]:
            return self.text.get_size()[0] + 1 + self.padding * 2, 40

        def paint(self) -> Image.Image:
            size = self.get_size()
            image = Image.new("RGBA", size)

            # draw text
            text = self.text.paint()
            # cut text in half into time and date pieces
            width = text.size[0]
            height = round(text.size[1] / 2)
            time = text.crop((0, 0, width, height))
            date = text.crop((0, height, width, height * 2))
            # center
            center_x = round((size[0] - text.size[0]) / 2)
            # composite
            image.alpha_composite(time, (center_x, self.padding - 4))
            image.alpha_composite(date, (center_x, size[1] - height - self.padding + 1))

            return image

    class TrayIcon(View):
        def __init__(self, icon: SegoeMDL2IconMap):
            super().__init__()
            self.icon = Text(icon.value, font=get_font(Font.SEGOE_MDL2, 16))

        def get_size(self) -> tuple[int, int] | tuple[float, float]:
            return 22, 38

        def paint(self) -> Image.Image:
            size = self.get_size()
            image = Image.new("RGBA", size)
            icon = self.icon.paint()
            print(icon.size)
            image.alpha_composite(icon, (3, 11))
            return image

    class TrayMore(View):
        def __init__(self):
            super().__init__()
            self.icon = Text(SegoeMDL2IconMap.CHEVRON_UP_MED.value, font=get_font(Font.SEGOE_MDL2, 12))

        def get_size(self) -> tuple[int, int] | tuple[float, float]:
            return 24, 40

        def paint(self) -> Image.Image:
            size = self.get_size()
            image = Image.new("RGBA", size)
            image.alpha_composite(self.icon.paint(), (6, 14))
            return image
