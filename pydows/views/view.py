from PIL import Image


class View:
    def __init__(self):
        self.parent: View | None = None

    def get_size(self) -> tuple[int, int] | tuple[float, float]:
        raise NotImplementedError(f"Class {self.__class__.__name__} hasn't implemented method `get_size`.")

    def paint(self) -> Image.Image:
        raise NotImplementedError(f"Class {self.__class__.__name__} hasn't implemented method `paint`.")

    def get_custom_property(self, prop: str):
        if self.parent:
            return self.parent.get_custom_property(prop)
        raise NotImplementedError(f"Class {self.__class__.__name__} hasn't implemented method `get_custom_property`.")


class ViewWithChildren(View):
    def __init__(self):
        super().__init__()
        self.children: list[View] = []

    def add_child(self, view: View):
        view.parent = self
        self.children.append(view)
