from ..views import View
from PIL import Image


class VideoView(View):
    def __init__(self, video_file: str):
        super().__init__()
        self._image = Image.open(video_file)

    def get_size(self) -> tuple[int, int] | tuple[float, float]:
        return self._image.size

    def paint(self):
        frame = self.parent.get_custom_property("current_frame")
        self._image.seek(frame % self._image.n_frames)
        return self._image.copy()
