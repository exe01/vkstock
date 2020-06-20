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


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class SourceViewSet(viewsets.ModelViewSet):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostImageViewSet(viewsets.ModelViewSet):
    queryset = PostImage.objects.all()
    serializer_class = PostImageSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class RenderedPostViewSet(viewsets.ModelViewSet):
    queryset = RenderedPost.objects.all()
    serializer_class = RenderedPostSerializer


class RenderedImageViewSet(viewsets.ModelViewSet):
    queryset = RenderedImage.objects.all()
    serializer_class = RenderedImageSerializer
