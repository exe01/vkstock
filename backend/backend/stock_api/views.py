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
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request


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
    filter_backends = [DjangoFilterBackend]


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend]


class PostImageViewSet(viewsets.ModelViewSet):
    queryset = PostImage.objects.all()
    serializer_class = PostImageSerializer
    filter_backends = [DjangoFilterBackend]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [DjangoFilterBackend]


class RenderedPostViewSet(viewsets.ModelViewSet):
    queryset = RenderedPost.objects.all()
    serializer_class = RenderedPostSerializer
    filterset_fields = ['project_id', ]
    filter_backends = [DjangoFilterBackend]


class RenderedImageViewSet(viewsets.ModelViewSet):
    queryset = RenderedImage.objects.all()
    serializer_class = RenderedImageSerializer
    filter_backends = [DjangoFilterBackend]


class NullPostId(Exception):
    pass


class RenderPost(APIView):
    """
    Render new post from original post.
    """
    def post(self, request, format=None):
        try:
            post_config = self._parse_config(request.data)
            rendered_post = self._create_post(post_config)
            # id = self._save_rendered_post(rendered_post)

            response = Response({
                'rendered_post_id': rendered_post.id
            })

            return response
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
        =================== ===========================

        :param data: config
        :type data: Request
        :return: Post config
        """
        post_config = {}

        original_post_id = data.get('original_post_id')
        if original_post_id is None:
            raise NullPostId()

        post_config['original_post_id'] = original_post_id

        return post_config

    def _create_post(self, post_config):
        """Create a new post. Take info from post config

        :param post_config: Configuration for building of post
        :return: Rendered post
        """
        original_post = Post.objects.get(id=post_config['original_post_id'])
        comments = original_post.comments.all()
        project = original_post.source_id.project_id

        rendered_post = RenderedPost(
            post_id=original_post,
            project_id=project,
            text=comments[0].text,
        )

        rendered_post.save()
        rendered_post.images.create(path='123.jpg')
        rendered_post.save()

        return rendered_post

# from PIL import Image, ImageDraw, ImageFont
#
# im = Image.open('images/download.jpeg')
#
# xsize, ysize = im.size
# offset = 100
#
# nim = Image.new('RGB', (xsize, ysize+offset), color="white")
# nim.paste(im, (0, offset))
#
# imdr = ImageDraw.Draw(nim)
#
# fnt = ImageFont.truetype("fonts/tahoma.ttf", 40)
# imdr.text((10, 10), "Helo wrld@", fill=(0, 0, 0), font=fnt)
#
# # imdr.
#
# nim.show()
#
# # rim = im.resize((xsize+100, ysize+100))
#
# # rim.show()