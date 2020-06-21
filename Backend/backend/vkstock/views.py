from rest_framework import viewsets
from django.contrib.auth.models import User, Group
from backend.vkstock.models import (
    Type,
    Project,
    Source,
    Post,
    PostImage,
    Comment,
    RenderedPost,
    RenderedImage,
)
from backend.vkstock.serializers import (
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
from rest_framework.response import Response


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

