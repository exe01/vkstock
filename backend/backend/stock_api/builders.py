from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import random
import string
import textwrap


class ImageBuilder:
    FONT_POINTS = 40
    SYMBOL_WIDTH = 22

    def build(self, original_img,
              text='', width=800,
              text_margin=30, text_location='top',
              font_name='anonymouspro.ttf', comment_img=None):

        resized_original_img = self.resize_img_by_width(original_img, width)
        main_img_width, main_img_height = resized_original_img.size

        if len(text) == 0 and comment_img is None:
            return resized_original_img

        comment_back = Image.new('RGB', (main_img_width, 1), color="white")

        if len(text) != 0:
            comment_back = self._add_text_to_pattern(comment_back, text, font_name, text_margin)

        if comment_img is not None:
            comment_back = self._add_img_to_pattern(comment_back, comment_img)

        if text_location == 'top':
            result_img = self.vertically_concatenate_images(comment_back, resized_original_img)
        else:
            # 'bottom'
            result_img = self.vertically_concatenate_images(resized_original_img, comment_back)

        return result_img

    def resize_img_by_width(self, img, width: int):
        orig_width, orig_height = img.size
        scale_factor = orig_width / width
        height = int(orig_height / scale_factor)
        resized_img = img.resize((width, height))
        return resized_img

    def _add_text_to_pattern(self, comment_back, text, font_name, text_margin):
        font = ImageFont.truetype('fonts/' + font_name, self.FONT_POINTS)
        text_width = comment_back.width - 2 * text_margin
        symbols_per_line = text_width / self.SYMBOL_WIDTH
        text = self.separate_text_by_lines(text, symbols_per_line)
        _, text_height = self.textsize(text, font)

        full_text_block_height = text_height + 2 * text_margin

        background_of_text = Image.new('RGB', (comment_back.width, full_text_block_height), color="white")
        background_of_text_drawer = ImageDraw.Draw(background_of_text)

        background_of_text_drawer.multiline_text(
            (text_margin, text_margin),
            text,
            fill=(0, 0, 0),
            font=font,
        )

        return self.vertically_concatenate_images(comment_back, background_of_text)

    def _add_img_to_pattern(self, comment_back, img):
        img_width = int(comment_back.width / 1.5)
        resized_img = self.resize_img_by_width(img, img_width)

        background_of_img = Image.new('RGB', (comment_back.width, resized_img.height), color="white")
        imx_x = (comment_back.width - resized_img.width) / 2
        imx_x = int(imx_x)

        background_of_img.paste(resized_img, (imx_x, 0))
        return self.vertically_concatenate_images(comment_back, background_of_img)

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

    def vertically_concatenate_images(self, img1, img2):
        result_img = Image.new(
            'RGB',
            (img1.width, img1.height+img2.height),
            color="white",
        )
        result_img.paste(
            img1,
            (0, 0)
        )
        result_img.paste(
            img2,
            (0, img1.height)
        )

        return result_img

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

    def get_random_name(self, length=32, format=None):
        letters_and_digits = string.ascii_letters + string.digits
        random_name = ''.join((random.choice(letters_and_digits) for _ in range(length)))

        if format:
            random_name += '.'+format.lower()

        return random_name
