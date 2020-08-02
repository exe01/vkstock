from PIL import Image, ImageDraw, ImageFont
from backend.stock_api.utils.censor import PartialCensor
from backend.stock_api.constants import *
from backend.stock_api.models import (
    Post,
    Comment,
    RenderedPost,
    RenderedImage,
)

from django.core.files import File

import io
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


class TextFormatter:
    def format_text(self, text, ref_text='', wrapper='*'):
        text = text.capitalize()
        ref_text = ref_text.capitalize()

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
                                        u"\U00002500-\U00002BEF"  # chinese char
                                        u"\U00002702-\U000027B0"
                                        u"\U00002702-\U000027B0"
                                        u"\U000024C2-\U0001F251"
                                        u"\U0001f926-\U0001f937"
                                        u"\U00010000-\U0010ffff"
                                        u"\u2640-\u2642" 
                                        u"\u2600-\u2B55"
                                        u"\u200d"
                                        u"\u23cf"
                                        u"\u23e9"
                                        u"\u231a"
                                        u"\ufe0f"  # dingbats
                                        u"\u3030"
                                       "]+", flags=re.UNICODE)
            return emoji_pattern.sub(r'', text)
        except:
            return text

    def censor(self, text, replace='*'):
        return PartialCensor.censor(text, repl=replace)


class PostTypeIsNotDefined(Exception):
    pass


class PostCreator:
    image_builder = ImageBuilder()
    text_builder = TextFormatter()

    def create(self, post_config):
        """Create a new post. Take info from post config

        :param post_config: Configuration for building of post
        :return: Rendered post
        """
        if post_config[POST_TYPE] == POST_TYPE_ORIGINAL:
            post = Post.objects.get(id=post_config[POST_ID])
            original_post = post
        elif post_config[POST_TYPE] == POST_TYPE_RENDERED:
            post = RenderedPost.objects.get(id=post_config[POST_ID])
            original_post = post.post_id
        else:
            raise PostTypeIsNotDefined()

        project = original_post.source_id.project_id

        if post_config[POST_TYPE] == POST_TYPE_RENDERED and post_config[REPLACE] == 1:
            rendered_post = post
            rendered_post.images.all().delete()
        else:
            rendered_post = RenderedPost(
                post_id=original_post,
                project_id=project,
            )

        if post_config[AS_ORIGINAL]:
            self._create_post_as_original(rendered_post, original_post)
            return rendered_post

        # Build text for image
        if post_config[IMG] == 1:
            if post_config[IMG_COUNT] > 1:
                rendered_post.save()
                self._add_original_images(rendered_post, original_post, IMG_COUNT)
                return rendered_post

            width = post_config[IMG_WIDTH]

            original_text = original_post.text
            original_text = self.text_builder.delete_emoji(original_text)
            comment_text, comment = self._build_comment_text(original_post, post_config)
            comment_text = self.text_builder.delete_emoji(comment_text)

            post_img = original_post.get_pillow_first_image()
            comment_img = comment.get_pillow_image() if comment else None

            if post_config[AUTO] and post_img is None and comment_img is None:
                width = 1000

            self.image_builder.reset(width=width)

            if post_config[IMG_WITH_ORIGINAL_TEXT]:
                censored_original_text = self.text_builder.censor(original_text)
                self.image_builder.add_text(censored_original_text)

            if post_config[IMG_WITH_POST_IMG]:
                self.image_builder.add_image(post_img)

            if post_config[IMG_WITH_COMMENT] and post_config[IMG_WITH_COMMENT_TEXT]:
                censored_comment_text = self.text_builder.censor(comment_text)
                self.image_builder.add_text(censored_comment_text)

            if post_config[IMG_WITH_COMMENT] and post_config[IMG_COMMENT_WITH_IMG]:
                self.image_builder.add_image(comment_img, width=600)

            # Add watermark
            self.image_builder.add_text(project.name, location='right', text_margin=5, points=30)

            rendered_img = self.image_builder.build()

            img_reader = io.BytesIO()
            rendered_img.save(img_reader, format=rendered_img.format)

            rendered_post.rating = self._calculate_rating(original_post, comment)
            rendered_post.save()

            img_of_rendered_post = RenderedImage(
                rendered_post_id=rendered_post
            )
            img_of_rendered_post.image.save(
                self.text_builder.get_random_name(format=rendered_img.format),
                File(img_reader)
            )
            img_of_rendered_post.save()

            return rendered_post
        else:
            rendered_post.save()
            return rendered_post

    def _calculate_rating(self, original_post, comment):
        comment_likes = 0
        if comment:
            comment_likes = comment.likes

        post_likes = 0
        if original_post:
            post_likes = original_post.likes

        count_of_source_members = 0
        if original_post and original_post.source_id:
            count_of_source_members = original_post.source_id.members

        if count_of_source_members == 0:
            return 0

        rating = (post_likes + comment_likes) / count_of_source_members
        return rating

    def _build_comment_text(self, original_post, post_config):
        image_text = ''
        comment = None
        if post_config[IMG_COMMENT_ID] is not None:
            comment_id = post_config[IMG_COMMENT_ID]
            comment = Comment.objects.get(id=comment_id)
        else:
            original_comments = original_post.comments.all().order_by('-likes')
            if len(original_comments) > 0:
                comment = original_comments[0]

        if comment:
            if post_config[IMG_COMMENT_TEXT_WITH_REF]:
                image_text = self.text_builder.format_text(comment.text, comment.ref_text)
            else:
                image_text = self.text_builder.format_text(comment.text)

        return image_text, comment

    def _create_post_as_original(self, rendered_post, original_post):
        rendered_post.text = original_post.text
        rendered_post.images.all().delete()
        rendered_post.save()

        self._add_original_images(rendered_post, original_post)

    def _add_original_images(self, rendered_post, original_post, count=-1):
        for num, img in enumerate(original_post.images.all()):
            if num == count:
                break

            rendered_img = RenderedImage(
                rendered_post_id=rendered_post
            )
            rendered_img.image = img.image
            rendered_img.save()
