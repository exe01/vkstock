from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import random
import string


class ImageBuilder:
    def build(self, read_path, text, write_path=None):
        if write_path is None:
            write_path = str(Path(read_path).parent.absolute()) + '/' + self.get_random_name() + '.jpg'

        img = Image.open(read_path)

        xsize, ysize = img.size
        offset = 100

        img_with_white_box = Image.new('RGB', (xsize, ysize+offset), color="white")
        img_with_white_box.paste(img, (0, offset))

        img_driwer = ImageDraw.Draw(img_with_white_box)
        font = ImageFont.truetype("fonts/tahoma.ttf", 40)
        img_driwer.text((10, 10), text, fill=(0, 0, 0), font=font)

        img_with_white_box.save(write_path)

        return Path(write_path).name

    def get_random_name(self, length=32):
        letters_and_digits = string.ascii_letters + string.digits
        return ''.join((random.choice(letters_and_digits) for _ in range(length)))
