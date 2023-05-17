import random
from PIL import Image, ImageFilter
from .view import View


noise_cache = {}


def get_noise(size=(128, 128), intensity=32, seed=12345):
    if size in noise_cache:
        return noise_cache[size]
    data = []
    pre_seed = random.getstate()
    random.seed(seed)
    for y in range(size[1]):
        for x in range(size[0]):
            val = random.randint(0, intensity)
            data.append(val)
    random.setstate(pre_seed)
    img = Image.frombytes("L", size, bytes(data))
    noise_cache[size] = img
    return img


class Acrylic(View):
    class NoParentError(Exception):
        pass

    class InvalidParentError(Exception):
        pass

    def __init__(self, view: View, color=(15, 15, 15, 128), blur=64, noise=16):
        super().__init__()
        self.child = view
        view.parent = self
        self.color = color
        self.blur = blur
        self.noise = noise

    def get_size(self) -> tuple[int, int] | tuple[float, float]:
        return self.child.get_size()

    def paint(self) -> Image.Image:
        # before we do any renders, get required props from our parent
        if self.parent is None:
            raise self.NoParentError("Acrylic view requires a parent")
        try:
            bg_image: Image.Image = self.parent.get_custom_property("raw_image")
            our_pos: tuple[int, int] = self.parent.get_custom_property("raw_child")["xy"]
        except NotImplementedError:
            raise self.InvalidParentError(
                "Acrylic view requires a parent with custom properties `raw_image` and `raw_child`"
            )

        child_image = self.child.paint()
        noise_layer = get_noise(child_image.size, intensity=self.noise)

        # bg blur
        crop = (our_pos[0], our_pos[1], child_image.size[0] + our_pos[0], child_image.size[1] + our_pos[1])
        image = bg_image.crop(crop).filter(ImageFilter.GaussianBlur(radius=self.blur)).convert("RGBA")
        # noise
        image.paste(Image.new("L", image.size, color=0), (0, 0), noise_layer)
        # final fill
        image.alpha_composite(Image.new("RGBA", image.size, color=self.color), (0, 0))

        # child time
        image.alpha_composite(child_image, (0, 0))

        return image
