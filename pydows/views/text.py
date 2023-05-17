from PIL import Image, ImageDraw, ImageFont
from .view import View
from typing import Literal


class Text(View):
    def __init__(self, text: str, font: ImageFont.ImageFont | ImageFont.FreeTypeFont | None = None,
                 fill=(255, 255, 255), align: Literal["left", "center", "right"] = "left", anchor: str | None = None):
        super().__init__()
        self.text = text
        self.font = font
        self.fill = fill
        self.align = align
        self.anchor = anchor

    def get_size(self) -> tuple[int, int]:
        image = Image.new("RGB", (1, 1))
        draw = ImageDraw.Draw(image)
        bbox = draw.textbbox((0, 0), self.text, font=self.font, align=self.align, anchor=self.anchor)
        return round(bbox[2]), round(bbox[3])

    def paint(self) -> Image.Image:
        image = Image.new("RGBA", self.get_size())
        draw = ImageDraw.Draw(image)
        draw.text((0, 0), self.text, font=self.font, fill=self.fill, align=self.align, anchor=self.anchor)
        return image
