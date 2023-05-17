from .view import View
from PIL import Image


class CachedView(View):
    def __init__(self, view: View):
        super().__init__()
        self.view = view
        self._cached_size = None
        self._cached_paint = None

    def get_size(self) -> tuple[int, int] | tuple[float, float]:
        if not self._cached_size:
            self._cached_size = self.view.get_size()
        return self._cached_size

    def paint(self) -> Image.Image:
        if not self._cached_paint:
            self.view.parent = self.parent
            self._cached_paint = self.view.paint()
        return self._cached_paint
