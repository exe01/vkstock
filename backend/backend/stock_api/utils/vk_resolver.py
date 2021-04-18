from urllib.parse import urlsplit
import requests


class IdentificatorNotFound(Exception):
    pass


class VKRequestError(Exception):
    pass


class VKResolver:
    @staticmethod
    def get_public_page_info_by_url(vk_url, token, v='5.52'):
        """

        :param vk_url: url address of public page
        :param token: service/user token
        :param v: version of vk api
        :return: public page model
        """
        identificator = VKResolver.get_identificator_from_url(vk_url)

        resp = requests.get('https://api.vk.com/method/groups.getById',
                            params={
                                'group_id': identificator,
                                'access_token': token,
                                'v': v
                            })

        json_resp = resp.json()
        if 'response' in json_resp:
            return json_resp['response'][0]
        else:
            raise VKRequestError(str(json_resp))

    @staticmethod
    def get_identificator_from_url(vk_url):
        splitted_url = urlsplit(vk_url)
        identificator = splitted_url.path

        if identificator == '':
            raise IdentificatorNotFound()
        else:
            identificator = identificator[1:]
            if identificator == '':
                raise IdentificatorNotFound()

        return identificator
