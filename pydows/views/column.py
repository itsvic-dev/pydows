import enum

from PIL import Image
from .view import ViewWithChildren


class Column(ViewWithChildren):
    class Alignment(enum.Enum):
        LEFT = 0
        CENTER = 1
        RIGHT = 2

    def __init__(self, padding=(0, 0), spacing=0, alignment: Alignment = Alignment.LEFT):
        super().__init__()
        self.padding = padding
        self.spacing = spacing
        self.alignment = alignment

    def get_size(self) -> tuple[int, int] | tuple[float, float]:
        width = max([child.get_size()[0] for child in self.children]) + self.padding[0] * 2
        height = sum([child.get_size()[1] for child in self.children]) + self.padding[1] * 2 \
            + self.spacing * (len(self.children) - 1)
        return width, height

    def paint(self) -> Image.Image:
        image = Image.new("RGBA", self.get_size())

        # draw children
        x_offset = self.padding[0]
        y_offset = self.padding[1]
        for child in self.children:
            child_size = child.get_size()
            child_x_offset = x_offset

            if self.alignment == self.Alignment.CENTER:
                # center-align the child
                child_x_offset = round((image.size[0] - child_size[0]) / 2)
            elif self.alignment == self.Alignment.RIGHT:
                # right-align the child
                child_x_offset = image.size[0] - child_size[0]

            # paint the child
            image.alpha_composite(child.paint(), (child_x_offset, y_offset))
            # move Y offset
            y_offset += child_size[1] + self.spacing

        return image
