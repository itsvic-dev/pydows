from pydows.views import Column, View, Image, Text, Row
from pydows.helpers import get_font
from PIL import Image as PILImage


class Notification(View):
    def __init__(self, header: tuple[str, str] | None = None, title: str = "", body: str = "", subtext: str = "",
                 image: str = "", opaque=True):
        super().__init__()
        self.column = Column(spacing=16, padding=(16, 16))
        self.column.parent = self
        self.opaque = opaque

        if header:
            # construct app header
            header_img = Image(header[0], size=(16, 16))
            header_text = Text(header[1], font=get_font("segoeui", 13), fill=(255, 255, 255), anchor="lt")

            header_row = Row(spacing=8, alignment=Row.Alignment.CENTER)
            header_row.add_child(header_img)
            header_row.add_child(header_text)

            self.column.add_child(header_row)

        toast_body = Column(spacing=2)
        if title:
            toast_body.add_child(Text(title, font=get_font("seguisb", 15), fill=(255, 255, 255)))
        if body:
            toast_body.add_child(Text(body, font=get_font("segoeui", 15), fill=(192, 192, 192, 192)))
        if subtext:
            toast_body.add_child(Text(subtext, font=get_font("segoeui", 13), fill=(192, 192, 192, 192)))

        if image:
            toast_body_new = Row(spacing=16)
            toast_body_new.add_child(Image(image, (48, 48)))
            toast_body_new.add_child(toast_body)
            toast_body = toast_body_new

        self.column.add_child(toast_body)

        self._close = Text("\ue711", font=get_font("segmdl2", size=12), fill=(255, 255, 255, 192))
        self._close.parent = self

    def get_size(self) -> tuple[int, int] | tuple[float, float]:
        column_size = self.column.get_size()
        return max(364, column_size[0]), column_size[1] + 8

    def paint(self) -> PILImage.Image:
        image = PILImage.new("RGBA", self.get_size())
        if self.opaque:
            image.paste((31, 31, 31, 255), (0, 0, image.size[0], image.size[1]))

        image.alpha_composite(self.column.paint(), (0, 2))

        close_img = self._close.paint()
        xy = (
            image.size[0] - close_img.size[0] - 22,
            21,
        )
        image.alpha_composite(close_img, xy)

        return image
