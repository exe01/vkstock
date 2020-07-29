import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
import django
django.setup()

from backend.stock_api.utils.vk_resolver import VKResolver, IdentificatorNotFound, VKRequestError
import unittest


class TestVKResolver(unittest.TestCase):
    def test_get_identificator(self):
        vk_url = "https://vk.com/abstract_humor"
        identificator = VKResolver.get_identificator_from_url(vk_url)
        self.assertEqual(identificator, 'abstract_humor')

        self.assertRaises(
            IdentificatorNotFound,
            VKResolver.get_identificator_from_url,
            'https://vk.com/',
        )

    def test_resolve_by_url(self):
        vk_url = 'https://vk.com/abstract_humor'
        group_id = 197230410
        token = '125433e8125433e8125433e8b91226a08111254125433e84cb77682426af7c6780f2899'

        vk_group = VKResolver.get_public_page_info_by_url(vk_url, token=token)
        self.assertEqual(vk_group['id'], group_id)

        self.assertRaises(
            VKRequestError,
            VKResolver.get_public_page_info_by_url,
            vk_url,
            'null_token'
        )


if __name__ == '__main__':
    unittest.main()
