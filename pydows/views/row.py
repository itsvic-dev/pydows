import enum

from PIL import Image
from .view import ViewWithChildren


class Row(ViewWithChildren):
    class Alignment(enum.Enum):
        TOP = 0
        CENTER = 1
        BOTTOM = 2

    def __init__(self, padding=(0, 0), spacing=0, alignment: Alignment = Alignment.TOP):
        super().__init__()
        self.padding = padding
        self.spacing = spacing
        self.alignment = alignment

    def get_size(self) -> tuple[int, int] | tuple[float, float]:
        width = sum([child.get_size()[0] for child in self.children]) + self.padding[0] * 2 \
                + self.spacing * (len(self.children) - 1)
        height = max([child.get_size()[1] for child in self.children]) + self.padding[1] * 2
        return width, height

    def paint(self) -> Image.Image:
        image = Image.new("RGBA", self.get_size())

        # draw children
        x_offset = self.padding[0]
        y_offset = self.padding[1]
        for child in self.children:
            child_size = child.get_size()
            child_y_offset = y_offset

            if self.alignment == self.Alignment.CENTER:
                # center-align the child
                child_y_offset = round((image.size[1] - child_size[1]) / 2)
            elif self.alignment == self.Alignment.BOTTOM:
                # bottom-align the child
                child_y_offset = image.size[1] - child_size[1]

            # paint the child
            image.alpha_composite(child.paint(), (x_offset, child_y_offset))
            # move X offset
            x_offset += child_size[0] + self.spacing

        return image
