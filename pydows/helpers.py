from PIL import ImageFont, Image
from os.path import join, dirname


def get_asset(path: str):
    return join(dirname(__file__), "assets", path)


def get_font(font: str, size: int):
    return ImageFont.truetype(get_asset(font + ".ttf"), size=size)


def crop_and_stretch(img: Image.Image, box: tuple[int, int, int, int]):
    image = img.crop(box)
    width = box[2] - box[0]
    height = box[3] - box[1]
    if box[2] > img.size[0]:
        # image is leaving on the right
        # by how much?
        clip_width = box[2] - img.size[0]
        # get the new crop for the stretched clip
        clip = img.crop((
            img.size[0] - 1,
            box[1],
            img.size[0],
            box[3],
        )).resize((clip_width, height))
        # now paste it into the remaining area
        image.paste(clip, (image.size[0] - clip_width, 0))

    return image
