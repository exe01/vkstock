from urllib.parse import urlsplit
import requests


class IdentificatorNotFound(Exception):
    pass


class VKRequestError(Exception):
    pass


class VKResolver:
    GROUP_FIELDS = (
        'members_count',
    )

    @staticmethod
    def get_public_page_info_by_url(vk_url, *args, **kwargs):
        """
        :param vk_url: url address of public page
        :param token: service/user token
        :param v: version of vk api
        :param fields: additional field that will return
        :return: public page model
        """
        identificator = VKResolver.get_identificator_from_url(vk_url)
        return VKResolver.get_public_page_info(identificator, *args, **kwargs)

    @staticmethod
    def get_public_page_info(group_id, token, v='5.52', fields=None):
        """
        :param group_id: identificator of public page
        :param token: service/user token
        :param v: version of vk api
        :param fields: additional field that will return
        :return: public page model
        """
        additional_fields = VKResolver.GROUP_FIELDS
        if fields is not None:
            additional_fields = additional_fields + tuple(fields)

        resp = requests.get('https://api.vk.com/method/groups.getById',
                            params={
                                'fields': additional_fields,
                                'group_id': group_id,
                                'access_token': token,
                                'v': v,
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
