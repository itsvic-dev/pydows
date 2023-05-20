from PIL import Image
from .view import ViewWithChildren, View


class LayeredView(ViewWithChildren):
    def __init__(self):
        super().__init__()
        self.children: list[dict[str, View | tuple[int, int]]] = []
        self.main_view: View | None = None
        self._image: Image.Image | None = None
        self._raw_child: dict[str, View | tuple[int, int]] | None = None

    def add_child(self, view: View, xy=(0, 0), is_main=False):
        view.parent = self
        if is_main:
            self.main_view = view
        else:
            self.children.append({"xy": xy, "view": view})

    def get_size(self) -> tuple[int, int] | tuple[float, float]:
        if self.main_view:
            return self.get_size()
        else:
            width = max([child["view"].get_size()[0] + child["xy"][0] for child in self.children])
            height = max([child["view"].get_size()[1] + child["xy"][1] for child in self.children])
            return width, height

    def paint(self) -> Image.Image:
        if self.main_view:
            image = self.main_view.paint().convert("RGBA")
        else:
            image = Image.new("RGBA", self.get_size())

        self._image = image

        for child in self.children:
            self._raw_child = child
            image.alpha_composite(child["view"].paint().convert("RGBA"), child["xy"])

        self._image = None

        return image

    def get_custom_property(self, prop: str):
        if prop == "raw_image":
            return self._image
        if prop == "raw_child":
            return self._raw_child
        if self.parent:
            return self.parent.get_custom_property(prop)
        raise NotImplementedError(f"Unknown property {prop}")
