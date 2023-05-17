import datetime

from PIL import Image
from enum import Enum
from fluent.helpers import get_font
from fluent.views import Row, View, Text
from fluent.constants import HoloMDL2IconMap, SegoeMDL2IconMap


class TaskBar(View):
    def __init__(self, width: int, opaque=True, has_notification=False):
        super().__init__()

        self.left = Row(spacing=1)
        self.color = (16, 16, 16, 255)
        self.opaque = opaque
        self.width = width
        self.height = 40

        self.left.add_child(self.TaskBarIconApp(HoloMDL2IconMap.WINDOWS))
        self.left.add_child(self.TaskBarIconApp(SegoeMDL2IconMap.SEARCH))
        self.left.add_child(self.TaskBarIconApp(SegoeMDL2IconMap.TASK_VIEW))

        self.action_center = self.TaskBarActionCenterIcon(has_notification=has_notification)
        self.action_center.parent = self

        self.time_and_date = self.TaskBarTimeAndDate()
        self.time_and_date.parent = self

    def get_size(self) -> tuple[int, int] | tuple[float, float]:
        return self.width, self.height

    def paint(self) -> Image.Image:
        size = self.get_size()
        image = Image.new("RGBA", size)

        if self.opaque:
            image.paste(self.color, (0, 0, size[0], size[1]))

        left_row = self.left.paint()
        image.alpha_composite(left_row, (0, 0))

        # right row is way more complex, so let's jump into it
        show_desktop_width = 5
        show_desktop_gap = 8
        image.alpha_composite(Image.new("RGBA", (1, 40), color=(128, 128, 128, 192)), (size[0] - show_desktop_width, 0))
        action_center_pos = (size[0] - show_desktop_width - show_desktop_gap - 40, 0)
        image.alpha_composite(self.action_center.paint(), action_center_pos)
        time_and_date = self.time_and_date.paint()
        time_and_date_pos = (action_center_pos[0] - time_and_date.size[0], 0)
        image.alpha_composite(time_and_date, time_and_date_pos)

        return image

    class TaskBarIconApp(View):
        def __init__(self, icon: Enum):
            super().__init__()
            self.is_holo = isinstance(icon, HoloMDL2IconMap)
            self.icon = Text(icon.value, font=get_font("holomdl2" if self.is_holo else "segmdl2", size=16))

        def get_size(self) -> tuple[int, int] | tuple[float, float]:
            return 48, 40

        def paint(self) -> Image.Image:
            image = Image.new("RGBA", self.get_size())

            # draw icon
            icon = self.icon.paint()
            image.alpha_composite(icon, (16, 12))

            return image

    class TaskBarActionCenterIcon(View):
        def __init__(self, has_notification=False):
            super().__init__()
            self.icon = Text(
                SegoeMDL2IconMap.ACTION_CENTER.value if not has_notification
                else SegoeMDL2IconMap.ACTION_CENTER_NOTIFICATION.value,
                font=get_font("segmdl2", size=16)
            )
            self.has_notification = has_notification

        def get_size(self) -> tuple[int, int] | tuple[float, float]:
            return 40, 40

        def paint(self) -> Image.Image:
            image = Image.new("RGBA", self.get_size())

            # draw icon
            icon = self.icon.paint()
            image.alpha_composite(icon, (12, 12))

            return image

    class TaskBarTimeAndDate(View):
        def __init__(self, time=datetime.datetime.now()):
            super().__init__()
            font = get_font("seguisb", 12)
            self.time = Text(time.strftime("%I:%M %p"), font=font)
            self.date = Text(time.strftime("%m/%d/%Y").lstrip('0'), font=font)
            self.padding = 6

        def get_size(self) -> tuple[int, int]:
            return self.date.get_size()[0] + 1 + self.padding * 2, 40

        def paint(self) -> Image.Image:
            size = self.get_size()
            image = Image.new("RGBA", size)

            # draw text
            time = self.time.paint()
            date = self.date.paint()
            # get centers
            time_pos = (round((size[0] - time.size[0]) / 2), self.padding)
            date_pos = (round((size[0] - date.size[0]) / 2), size[1] - date.size[1] - self.padding)
            # composite
            image.alpha_composite(time, time_pos)
            image.alpha_composite(date, date_pos)

            return image
