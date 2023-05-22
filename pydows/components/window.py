from pydows.views import View, Text, Image, Row
from pydows.constants import Font, SegoeMDL2IconMap
from PIL import Image as PILImage


class Window(View):
    def __init__(self, content: View, title: str, icon: str = "", popup=False):
        super().__init__()
        self.content = content
        self.title_bar = self.TitleBar(title, icon, popup)
        self.title_bar.parent = self

    def get_size(self) -> tuple[int, int] | tuple[float, float]:
        size = self.content.get_size()
        return size[0], size[1] + 29

    def paint(self) -> PILImage.Image:
        image = PILImage.new("RGBA", self.get_size())
        image.alpha_composite(self.title_bar.paint(), (0, 0))
        image.alpha_composite(self.content.paint(), (0, 29))
        return image

    class TitleBar(View):
        def __init__(self, title: str, icon: str = "", popup=False):
            super().__init__()
            if icon:
                self.icon = Image(icon, (16, 16))
            self.title = Text(title, font=Font.SEGOE_UI, size=12, fill=(0, 0, 0))

            self.buttons = Row(spacing=1)
            if not popup:
                self.buttons.add_child(self.Button(SegoeMDL2IconMap.CHROME_MINIMIZE, popup=popup))
                self.buttons.add_child(self.Button(SegoeMDL2IconMap.CHROME_MAXIMIZE, popup=popup))
            self.buttons.add_child(self.Button(SegoeMDL2IconMap.CHROME_CLOSE, popup=popup))

        class Button(View):
            def __init__(self, icon: SegoeMDL2IconMap, popup=False):
                super().__init__()
                self.icon = Text(icon.value, font=Font.SEGOE_MDL2, size=10, fill=(0, 0, 0))
                self.popup = popup

            def get_size(self) -> tuple[int, int] | tuple[float, float]:
                return (45, 29) if not self.popup else (31, 29)

            def paint(self) -> PILImage.Image:
                image = PILImage.new("RGBA", self.get_size())
                icon = self.icon.paint()
                center = (
                    round((image.size[0] - icon.size[0]) / 2),
                    round((image.size[1] - icon.size[1]) / 2),
                )
                image.alpha_composite(icon, center)
                return image

        def get_size(self) -> tuple[int, int] | tuple[float, float]:
            return self.parent.get_size()[0], 29

        def paint(self) -> PILImage.Image:
            image = PILImage.new("RGBA", self.get_size(), color=(255, 255, 255, 255))

            offset = 8
            if self.icon:
                image.alpha_composite(self.icon.paint(), (8, 6))
                offset += 16 + 6
            image.alpha_composite(self.title.paint(), (offset - 1, 6))

            buttons = self.buttons.paint()
            image.alpha_composite(buttons, (image.size[0] - buttons.size[0], 0))

            return image
