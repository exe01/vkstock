from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import random
import string
import textwrap
import re


class ImageBuilder:
    FONT_POINTS = 40
    SYMBOL_WIDTH = 22

    _image = None

    def reset(self, width=800):
        self._image = Image.new('RGB', (width, 1), color="white")

    def build(self, format='jpeg'):
        self._image.format = format
        return self._image

    def add_text(self, text, text_margin=30, font_name='anonymouspro.ttf', align='left', location='center', points=None):
        if text == '':
            return

        points = points if points else self.FONT_POINTS

        font = ImageFont.truetype('fonts/' + font_name, points)
        text_width = self._image.width - 2 * text_margin
        symbols_per_line = text_width / self.SYMBOL_WIDTH
        text = self._separate_text_by_lines(text, symbols_per_line)
        real_width, real_height = self._textsize(text, font)
        full_text_block_height = real_height + 2 * text_margin

        background_of_text = Image.new('RGB', (real_width, real_height), color="white")
        background_of_text_drawer = ImageDraw.Draw(background_of_text)
        background_of_text_drawer.multiline_text(
            (0, 0),
            text,
            fill=(0, 0, 0),
            font=font,
            align=align
        )

        background_of_text = self._locate(location,
                                          background_of_text,
                                          self._image.width,
                                          margin_left=text_margin,
                                          margin_top=text_margin,
                                          margin_bot=text_margin,
                                          margin_right=text_margin)

        self.vertically_concatenate_image(background_of_text)

    def add_image(self, image, width=800, location='center', margin=30):
        if image is None:
            return

        resized_img = self._resize_img_by_width(image, width)
        resized_img = self._locate(location,
                                   resized_img,
                                   self._image.width,
                                   margin_left=margin,
                                   margin_top=margin,
                                   margin_bot=margin,
                                   margin_right=margin)

        self.vertically_concatenate_image(resized_img)

    def vertically_concatenate_image(self, img):
        result_img = Image.new(
            'RGB',
            (self._image.width, self._image.height + img.height),
            color="white",
        )
        result_img.paste(
            self._image,
            (0, 0)
        )
        result_img.paste(
            img,
            (0, self._image.height)
        )
        self._image = result_img

    def _resize_img_by_width(self, img, width: int):
        orig_width, orig_height = img.size
        scale_factor = orig_width / width
        height = int(orig_height / scale_factor)
        resized_img = img.resize((width, height))
        return resized_img

    def _textsize(self, text, font):
        test_img = Image.new('RGB', (1, 1), color="white")
        test_img_driwer = ImageDraw.Draw(test_img)
        width, height = test_img_driwer.multiline_textsize(text, font=font)
        height += 10 # serif
        return width, height

    def _separate_text_by_lines(self, text, symbols_per_line):
        paragraphs = text.split('\n')
        new_paragraphs = []

        for paragraph in paragraphs:
            paragraph_lines = textwrap.wrap(paragraph, width=symbols_per_line)
            new_paragraph = '\n'.join(paragraph_lines)
            new_paragraphs.append(new_paragraph)

        return '\n'.join(new_paragraphs)

    def _locate(self, location, *args, **kwargs):
        if location == 'center':
            return self._center(*args, **kwargs)
        elif location == 'left':
            return self._left(*args, **kwargs)
        elif location == 'right':
            return self._right(*args, **kwargs)

        return self._left(*args, **kwargs)

    def _center(self, img, width, margin_top=0, margin_bot=0, margin_left=0, margin_right=0):
        centered_img = Image.new('RGB', (width, img.height + margin_bot + margin_top), color="white")
        img_x = (width - img.width) / 2
        img_x = int(img_x)

        if img_x < 0:
            centered_img.paste(img, (0, margin_top))
        else:
            centered_img.paste(img, (img_x, margin_top))

        return centered_img

    def _left(self, img, width, margin_top=0, margin_bot=0, margin_left=0, margin_right=0):
        left_img = Image.new('RGB', (width, img.height + margin_bot + margin_top), color="white")
        left_img.paste(img, (margin_left, margin_top))
        return left_img

    def _right(self, img, width, margin_top=0, margin_bot=0, margin_left=0, margin_right=0):
        right_img = Image.new('RGB', (width, img.height + margin_bot + margin_top), color="white")

        img_x = (width - img.width - margin_right)
        img_x = int(img_x)

        if img_x < 0:
            right_img.paste(img, (0, margin_top))
        else:
            right_img.paste(img, (img_x, margin_top))

        return right_img


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

    def delete_emoji(self, text):
        try:
            emoji_pattern = re.compile("["
                                       u"\U0001F600-\U0001F64F"  # emoticons
                                       u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                       u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                       u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                       u"\U00002702-\U000027B0"
                                       u"\U000024C2-\U0001F251"
                                       "]+", flags=re.UNICODE)
            return emoji_pattern.sub(r'', text)
        except:
            return text
