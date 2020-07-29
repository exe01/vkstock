from backend.stock_api.constants import *


class NullPostId(Exception):
    pass


def parse_post_config(json_data):
    """Parse client data to post config for building of post.

    :param json_data: config
    :type json_data: Request
    :return: Post config
    """
    post_config = {}

    original_post_id = json_data.get(ORIGINAL_POST_ID)
    rendered_post_id = json_data.get(RENDERED_POST_ID)

    if original_post_id is None and rendered_post_id is None:
        raise NullPostId()

    if rendered_post_id is None:
        post_config[POST_ID] = original_post_id
        post_config[POST_TYPE] = POST_TYPE_ORIGINAL
    else:
        post_config[POST_ID] = rendered_post_id
        post_config[POST_TYPE] = POST_TYPE_RENDERED
        post_config[REPLACE] = json_data.get(REPLACE, 0)

    post_config[AS_ORIGINAL] = json_data.get(AS_ORIGINAL, 0)

    post_config[AUTO] = json_data.get(AUTO, 1)

    post_config[FONT] = json_data.get(FONT, 'anonymouspro.ttf')
    post_config[IMG] = json_data.get(IMG, 1)
    post_config[IMG_WIDTH] = json_data.get(IMG_WIDTH, 800)
    post_config[IMG_COUNT] = json_data.get(IMG_COUNT, 1)

    post_config[IMG_WITH_TEXT] = json_data.get(IMG_WITH_TEXT, 1)

    post_config[IMG_WITH_ORIGINAL_TEXT] = json_data.get(IMG_WITH_ORIGINAL_TEXT, 1)
    post_config[IMG_WITH_POST_IMG] = json_data.get(IMG_WITH_POST_IMG, 1)
    post_config[IMG_WITH_COMMENT] = json_data.get(IMG_WITH_COMMENT, 1)
    post_config[IMG_COMMENT_ID] = json_data.get(IMG_COMMENT_ID, None)
    post_config[IMG_WITH_COMMENT_TEXT] = json_data.get(IMG_WITH_COMMENT_TEXT, 1)
    post_config[IMG_COMMENT_TEXT_WITH_REF] = json_data.get(IMG_COMMENT_TEXT_WITH_REF, 1)
    post_config[IMG_COMMENT_WITH_IMG] = json_data.get(IMG_COMMENT_WITH_IMG, 1)

    return post_config

