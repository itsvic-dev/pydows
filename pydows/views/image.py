from PIL import Image as PILImage
from .view import View


class Image(View):
    def __init__(self, filename: str, size: tuple[int, int] | None = None):
        super().__init__()
        self._filename = filename
        self._image = PILImage.open(filename)
        if size is not None:
            self._resize(self._image.size, size)

    def get_size(self) -> tuple[int, int]:
        return self._image.size

    def set_size(self, size: tuple[int, int]):
        self._image = PILImage.open(self._filename)
        self._resize(self._image.size, size)

    def _resize(self, old_size: tuple[int, int], new_size: tuple[int, int]):
        ratio = max(new_size[0] / old_size[0], new_size[1] / old_size[1])
        size_pre_crop = (round(old_size[0] * ratio), round(old_size[1] * ratio))
        pre_crop = self._image.resize(size_pre_crop)
        # get middle for new_size
        if new_size[0] >= size_pre_crop[0]:
            # new size is wider, center height
            new_y = round((size_pre_crop[1] - new_size[1]) / 2)
            crop = (0, new_y, new_size[0], new_size[1] + new_y)
        else:
            # new size is taller, center width
            new_x = round((size_pre_crop[0] - new_size[0]) / 2)
            crop = (new_x, 0, new_size[0] + new_x, new_size[1])
        self._image = pre_crop.crop(crop)

    def paint(self) -> PILImage.Image:
        return self._image
