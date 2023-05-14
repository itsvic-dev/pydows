import random
from PIL import Image, ImageFilter


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


def pos_size_to_xy(pos: tuple[int, int], size: tuple[int, int]) -> tuple[int, int, int, int]:
    return (
        pos[0], pos[1],
        pos[0] + size[0],
        pos[1] + size[1]
    )


def create_acrylic(bg: Image.Image, size: tuple[int, int], offset=(0, 0), color=(0, 0, 0, 192), blur_radius=32,
                   noise_intensity=32) -> Image.Image:
    """
    Create an acrylic-blurred image.
    :param bg: Background image.
    :param size: Size of new image.
    :param offset: Background offset.
    :param color: Color of new image's fill.
    :param blur_radius: Blur intensity.
    :param noise_intensity: Noise intensity.
    :return: A PIL Image.
    """
    xy = pos_size_to_xy(offset, size)
    # bg blur
    image = bg.crop(xy).filter(ImageFilter.GaussianBlur(radius=blur_radius)).convert("RGBA")
    # noise
    image.paste(Image.new("L", size, color=0), (0, 0), get_noise(size, intensity=noise_intensity))
    # final fill
    image.alpha_composite(Image.new("RGBA", size, color=color), (0, 0))
    return image


def create_mica(bg: Image.Image, size: tuple[int, int], offset=(0, 0), color=(32, 32, 32, 192), blur_radius=128,
                noise_intensity=8) -> Image.Image:
    """
    Create a mica-blurred image.

    Wrapper for `create_acrylic` with different defaults.
    :param bg: Background image.
    :param size: Size of new image.
    :param offset: Background offset.
    :param color: Color of new image's fill.
    :param blur_radius: Blur intensity.
    :param noise_intensity: Noise intensity.
    :return: A PIL Image.
    """
    return create_acrylic(bg, size, offset=offset, color=color, blur_radius=blur_radius,
                          noise_intensity=noise_intensity)


if __name__ == "__main__":
    bg = Image.open("../test.png")
    w1, h1 = size = (768, 512)
    w2, h2 = bg.size
    center_x = round((w2 - w1) / 2)
    center_y = round((h2 - h1) / 2)
    offset = (center_x, center_y)

    acrylic = create_acrylic(bg, size, offset=offset)
    mica = create_mica(bg, size, offset=offset)

    acrylic_img = bg.copy()
    acrylic_img.paste(acrylic, offset)
    acrylic_img.show()

    mica_img = bg.copy()
    mica_img.paste(mica, offset)
    mica_img.show()
