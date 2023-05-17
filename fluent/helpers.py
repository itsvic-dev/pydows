from PIL import ImageFont
from os.path import join, dirname


def get_font(font: str, size: int):
    return ImageFont.truetype(join(dirname(__file__), "assets", font + ".ttf"), size=size)
