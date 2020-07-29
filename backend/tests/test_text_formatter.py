import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
import django
django.setup()

from backend.stock_api.builders import TextFormatter
import unittest


class TestTextFormatter(unittest.TestCase):
    def setUp(self) -> None:
        self.text_builder = TextFormatter()

    def test_delete_emoji(self):
        text_with_emoji = 'galaxy 😱😍🤔. Omg'
        text_without_emoji = 'galaxy . Omg'

        self.assertEqual(
            self.text_builder.delete_emoji(text_with_emoji),
            text_without_emoji
        )

    def test_format_text(self):
        text = 'first text'
        ref_text = 'ref text'

        self.assertEqual(
            self.text_builder.format_text('', ''),
            ''
        )

        self.assertEqual(
            self.text_builder.format_text(text),
            text.capitalize()
        )

        self.assertEqual(
            self.text_builder.format_text('', ref_text),
            ref_text.capitalize()
        )

        self.assertEqual(
            self.text_builder.format_text(text, ref_text),
            '*{}*\n\n*{}*'.format(ref_text.capitalize(), text.capitalize())
        )

    def test_wrap_text(self):
        text = 'some text'
        wrapper = '***'

        self.assertEqual(
            self.text_builder.wrap_text(text=text, wrapper=wrapper),
            '{}{}{}'.format(wrapper, text, wrapper)
        )

    def test_censor(self):
        text_with_mat = 'Привет хуй я пизда. Да'
        censored_text = 'Привет х*й я п***а. Да'

        self.assertEqual(
            self.text_builder.censor(text_with_mat),
            censored_text
        )

        self.assertEqual(
            self.text_builder.censor(''),
            ''
        )


if __name__ == '__main__':
    unittest.main()
