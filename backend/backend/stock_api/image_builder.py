from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import random
import string


class ImageBuilder:
    def build(self, original_img, text):
        xsize, ysize = original_img.size
        offset = 100

        img_with_white_box = Image.new('RGB', (xsize, ysize+offset), color="white")
        img_with_white_box.paste(original_img, (0, offset))

        img_driwer = ImageDraw.Draw(img_with_white_box)
        font = ImageFont.truetype("fonts/tahoma.ttf", 40)
        img_driwer.text((10, 10), text, fill=(0, 0, 0), font=font)

        return img_with_white_box

    def get_random_name(self, length=32, format=None):
        letters_and_digits = string.ascii_letters + string.digits
        random_name = ''.join((random.choice(letters_and_digits) for _ in range(length)))

        if format:
            random_name += '.'+format.lower()

        return random_name
