from .view import View
from PIL import Image, ImageFilter


class Shadow(View):
    def __init__(self, view: View, color=(0, 0, 0, 128), radius=16, y_offset=0):
        super().__init__()
        self.view = view
        self.view.parent = self
        self.color = color
        self.radius = radius
        self.y_offset = y_offset

    def get_size(self) -> tuple[int, int] | tuple[float, float]:
        size = self.view.get_size()
        return size[0] + self.radius * 4, size[1] + self.y_offset + self.radius * 4

    def paint(self) -> Image.Image:
        size = self.get_size()
        image = Image.new("RGBA", size)

        view = self.view.paint()

        offset = (
            round((size[0] - view.size[0]) / 2),
            round((size[1] - view.size[1] - self.y_offset) / 2),
        )
        shadow_offset = (
            offset[0],
            offset[1] + self.y_offset,
        )
        image.paste(Image.new("RGBA", view.size, self.color), shadow_offset)
        image = image.filter(ImageFilter.GaussianBlur(self.radius))
        image.alpha_composite(view, offset)

        return image
