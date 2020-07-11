from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import random
import string
import textwrap


class ImageBuilder:
    def build(self, original_img, text, width=800):
        resized_img = self.resize_img_by_width(original_img, width)

        if len(text) == 0:
            return resized_img

        # 40 points ~ 22px of width by 1 symbol
        font = ImageFont.truetype("fonts/anonymouspro.ttf", 40)

        # Margin of text block
        margin = 20

        xsize, ysize = resized_img.size

        text_width = xsize - 2*margin

        symbols_per_line = text_width / 22

        text = self.separate_text_by_lines(text, symbols_per_line)

        _, text_height = self.textsize(text, font)

        full_text_block_height = text_height+2*margin
        full_image_height = ysize + full_text_block_height

        rendered_img = Image.new('RGB', (xsize, full_image_height), color="white")
        rendered_img.paste(resized_img, (0, full_text_block_height))
        img_driwer = ImageDraw.Draw(rendered_img)
        img_driwer.multiline_text((margin, margin), text, fill=(0, 0, 0), font=font)

        return rendered_img

    def resize_img_by_width(self, img, width: int):
        orig_width, orig_height = img.size
        scale_factor = orig_width / width
        height = int(orig_height / scale_factor)
        resized_img = img.resize((width, height))
        return resized_img

    def textsize(self, text, font):
        """
        :param text:
        :param font:
        :return: max width, max_height
        """
        test_img = Image.new('RGB', (10, 10), color="white")
        test_img_driwer = ImageDraw.Draw(test_img)
        return test_img_driwer.multiline_textsize(text, font=font)

    def separate_text_by_lines(self, text, symbols_per_line):
        paragraphs = text.split('\n')
        new_paragraphs = []

        for paragraph in paragraphs:
            paragraph_lines = textwrap.wrap(paragraph, width=symbols_per_line)
            new_paragraph = '\n'.join(paragraph_lines)
            new_paragraphs.append(new_paragraph)

        return '\n'.join(new_paragraphs)

    def get_random_name(self, length=32, format=None):
        letters_and_digits = string.ascii_letters + string.digits
        random_name = ''.join((random.choice(letters_and_digits) for _ in range(length)))

        if format:
            random_name += '.'+format.lower()

        return random_name
