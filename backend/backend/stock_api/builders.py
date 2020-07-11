from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import random
import string
import textwrap


class ImageBuilder:
    FONT_POINTS = 40
    SYMBOL_WIDTH = 22

    def build(self, original_img, text, width=800, text_margin=30, text_location='top', font_name='anonymouspro.ttf'):
        resized_img = self.resize_img_by_width(original_img, width)

        if len(text) == 0:
            return resized_img

        # 40 points ~ 22px of width by 1 symbol
        font = ImageFont.truetype('fonts/'+font_name, self.FONT_POINTS)

        xsize, ysize = resized_img.size

        text_width = xsize - 2*text_margin
        symbols_per_line = text_width / self.SYMBOL_WIDTH
        text = self.separate_text_by_lines(text, symbols_per_line)
        _, text_height = self.textsize(text, font)

        full_text_block_height = text_height+2*text_margin
        full_image_height = ysize + full_text_block_height

        rendered_img = Image.new('RGB', (xsize, full_image_height), color="white")
        img_drawer = ImageDraw.Draw(rendered_img)

        if text_location == 'top':
            rendered_img.paste(resized_img, (0, full_text_block_height))
            img_drawer.multiline_text((text_margin, text_margin), text, fill=(0, 0, 0), font=font)
        elif text_location == 'bottom':
            rendered_img.paste(resized_img, (0, 0))
            img_drawer.multiline_text((text_margin, text_margin+ysize), text, fill=(0, 0, 0), font=font)

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

class TextBuilder:
    def format_text(self, text, ref_text='', wrapper='*'):
        text = self.up_first_letter(text)
        ref_text = self.up_first_letter(ref_text)

        if len(text) == 0 and len(ref_text) == 0:
            return ''

        if len(text) != 0 and len(ref_text) == 0:
            return text

        if len(text) == 0 and len(ref_text) != 0:
            return ref_text

        if len(text) != 0 and len(ref_text) != 0:
            text = self.wrap_text(text, wrapper)
            ref_text = self.wrap_text(ref_text, wrapper)
            return '{}\n\n{}'.format(ref_text, text)

        return ''

    def up_first_letter(self, text=''):
        if len(text) > 0:
            return text[0].upper() + text[1:]

        return text

    def wrap_text(self, text, wrapper=''):
        return '{}{}{}'.format(wrapper, text, wrapper)
