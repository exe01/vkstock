from django.contrib.auth.models import User, Group
from backend.stock_api.models import (
    Type,
    Project,
    Source,
    Post,
    PostImage,
    Comment,
    RenderedPost,
    RenderedImage,
)
from backend.stock_api.serializers import (
    UserSerializer,
    GroupSerializer,
    TypeSerializer,
    ProjectSerializer,
    SourceSerializer,
    PostSerializer,
    PostImageSerializer,
    CommentSerializer,
    RenderedPostSerializer,
    RenderedImageSerializer,
)
from backend.stock_api.constants import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from backend.stock_api.builders import ImageBuilder, TextBuilder
from django.core.files import File
from PIL import Image
import io


class UserViewSet(viewsets.ModelViewSet):
    """API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class TypeViewSet(viewsets.ModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer
    filter_backends = [DjangoFilterBackend]


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = [DjangoFilterBackend]


class SourceViewSet(viewsets.ModelViewSet):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer
    filterset_fields = ['project_id']
    filter_backends = [DjangoFilterBackend]


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-id')
    serializer_class = PostSerializer
    filterset_fields = ['source_id']
    ordering_fields = ['date', 'rating']
    filter_backends = [DjangoFilterBackend, OrderingFilter]


class PostImageViewSet(viewsets.ModelViewSet):
    queryset = PostImage.objects.all()
    serializer_class = PostImageSerializer
    filter_backends = [DjangoFilterBackend]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [DjangoFilterBackend]


class RenderedPostViewSet(viewsets.ModelViewSet):
    queryset = RenderedPost.objects.all().order_by('-id')
    serializer_class = RenderedPostSerializer
    filterset_fields = ['project_id', 'status']
    filter_backends = [DjangoFilterBackend]


class RenderedImageViewSet(viewsets.ModelViewSet):
    queryset = RenderedImage.objects.all()
    serializer_class = RenderedImageSerializer
    filter_backends = [DjangoFilterBackend]


class NullPostId(Exception):
    pass


class PostTypeIsNotDefined(Exception):
    pass


class RenderPost(APIView):
    image_builder = ImageBuilder()
    text_builder = TextBuilder()

    """
    Render new post from original post.
    """
    def post(self, request, format=None):
        try:
            post_config = self._parse_config(request.data)
            rendered_post = self._create_post(post_config)
            # id = self._save_rendered_post(rendered_post)

            serializer = RenderedPostSerializer(rendered_post)
            response = Response(serializer.data)
        except NullPostId:
            response = Response({
                'exception': 'Id of post is null'
            }, 400)

        return response

    def _parse_config(self, data):
        """Parse client data to post config for building of post.

        Post config:

        =================== ===========================
        Key                 Description
        =================== ===========================
        original_post_id    Id of original post
        rendered_post_id    Id of rendered post
        replace             Replace rendered post
        as_original         Render as original
        =================== ===========================

        :param data: config
        :type data: Request
        :return: Post config
        """
        post_config = {}

        original_post_id = data.get(ORIGINAL_POST_ID)
        rendered_post_id = data.get(RENDERED_POST_ID)

        if original_post_id is None and rendered_post_id is None:
            raise NullPostId()

        if rendered_post_id is None:
            post_config[POST_ID] = original_post_id
            post_config[POST_TYPE] = POST_TYPE_ORIGINAL
        else:
            post_config[POST_ID] = rendered_post_id
            post_config[POST_TYPE] = POST_TYPE_RENDERED
            post_config[REPLACE] = data.get(REPLACE, 0)

        post_config[AS_ORIGINAL] = data.get(AS_ORIGINAL, 0)

        post_config[AUTO] = data.get(AUTO, 1)

        post_config[FONT] = data.get(FONT, 'anonymouspro.ttf')
        post_config[IMG] = data.get(IMG, 1)
        post_config[IMG_WIDTH] = data.get(IMG_WIDTH, 800)
        post_config[IMG_COUNT] = data.get(IMG_COUNT, 1)

        post_config[IMG_WITH_TEXT] = data.get(IMG_WITH_TEXT, 1)

        post_config[IMG_WITH_ORIGINAL_TEXT] = data.get(IMG_WITH_ORIGINAL_TEXT, 1)
        post_config[IMG_WITH_POST_IMG] = data.get(IMG_WITH_POST_IMG, 1)
        post_config[IMG_COMMENT_ID] = data.get(IMG_COMMENT_ID, None)
        post_config[IMG_WITH_COMMENT_TEXT] = data.get(IMG_WITH_COMMENT_TEXT, 1)
        post_config[IMG_COMMENT_TEXT_WITH_REF] = data.get(IMG_COMMENT_TEXT_WITH_REF, 1)
        post_config[IMG_COMMENT_WITH_IMG] = data.get(IMG_COMMENT_WITH_IMG, 1)

        return post_config

    def _create_post(self, post_config):
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
                self.image_builder.add_text(original_text)

            if post_config[IMG_WITH_POST_IMG]:
                self.image_builder.add_image(post_img)

            if post_config[IMG_WITH_COMMENT_TEXT]:
                self.image_builder.add_text(comment_text)

            if post_config[IMG_COMMENT_WITH_IMG]:
                self.image_builder.add_image(comment_img, width=400)

            # Add watermark
            self.image_builder.add_text(project.name, location='right', text_margin=5, points=30)

            rendered_img = self.image_builder.build()

            img_reader = io.BytesIO()
            rendered_img.save(img_reader, format=rendered_img.format)

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

    def _build_comment_text(self, original_post, post_config):
        image_text = ''
        comment = None
        if post_config[IMG_COMMENT_ID] is not None:
            comment_id = post_config[IMG_COMMENT_ID]
            comment = Comment.objects.get(id=comment_id)
        else:
            original_comments = original_post.comments.all().order_by('-rating')
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
