from PIL import Image as PILImage
from .view import View


class Image(View):
    def __init__(self, filename: str, size: tuple[int, int] | None = None):
        super().__init__()
        self._filename = filename
        self._image = PILImage.open(filename)
        if size is not None:
            self._image.thumbnail(size)

    def get_size(self) -> tuple[int, int]:
        return self._image.size

    def set_size(self, size: tuple[int, int]):
        self._image = PILImage.open(self._filename)
        self._image.thumbnail(size)

    def paint(self) -> PILImage.Image:
        return self._image
