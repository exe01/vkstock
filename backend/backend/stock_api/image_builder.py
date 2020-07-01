from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import random
import string
import textwrap


class ImageBuilder:
    def build(self, original_img, text):
        lines = textwrap.wrap(text, width=40)
        text = '\n'.join(lines)

        font = ImageFont.truetype("fonts/tahoma.ttf", 40)
        test_img = Image.new('RGB', (10, 10), color="white")
        test_img_driwer = ImageDraw.Draw(test_img)
        max_width, max_height = test_img_driwer.multiline_textsize(text, font=font)

        xsize, ysize = original_img.size

        if max_width > xsize:
            xsize = max_width

        offset = max_height + 40

        img_with_white_box = Image.new('RGB', (xsize, ysize+offset), color="white")
        img_with_white_box.paste(original_img, (0, offset))

        img_driwer = ImageDraw.Draw(img_with_white_box)

        img_driwer.multiline_text((10, 10), text, fill=(0, 0, 0), font=font, align='left')

        return img_with_white_box

    def get_random_name(self, length=32, format=None):
        letters_and_digits = string.ascii_letters + string.digits
        random_name = ''.join((random.choice(letters_and_digits) for _ in range(length)))

        if format:
            random_name += '.'+format.lower()

        return random_name
