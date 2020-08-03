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
from rest_framework.filters import OrderingFilter
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from backend.stock_api.utils.parser import parse_post_config, NullPostId
from backend.stock_api.builders import PostCreator
from backend.stock_api.utils.vk_resolver import VKResolver, IdentificatorNotFound, VKRequestError
from rest_framework import status

import time
import threading


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

    def create(self, request, *args, **kwargs):
        json_data = request.data

        if 'url' in json_data:
            try:
                url = json_data['url']
                type_id = json_data['type_id']
                type_ = Type.objects.get(id=type_id)

                if type_.name == 'vk_group':
                    public_page = VKResolver.get_public_page_info_by_url(url, token=type_.token)

                    source_data = {
                        'name': public_page['name'],
                        'platform_id': public_page['id'],
                        'project_id': json_data['project_id'],
                        'type_id': type_id,
                        'members': public_page.get('members_count', 0),
                    }

                    serializer = self.get_serializer(data=source_data)
                    serializer.is_valid(raise_exception=True)
                    self.perform_create(serializer)
                    headers = self.get_success_headers(serializer.data)
                    return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            except VKRequestError:
                return Response(data={'exception': 'error while executing request to vk'}, status=400)
        else:
            return super().create(request, *args, **kwargs)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-id')
    serializer_class = PostSerializer
    filterset_fields = ['source_id']
    ordering_fields = ['date', 'likes']
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
    ordering_fields = ['posted_date', 'rating']
    filter_backends = [DjangoFilterBackend, OrderingFilter]


class RenderedImageViewSet(viewsets.ModelViewSet):
    queryset = RenderedImage.objects.all()
    serializer_class = RenderedImageSerializer
    filter_backends = [DjangoFilterBackend]


class RenderPost(APIView):
    """
    Render new post from original post.
    """
    post_creator = PostCreator()

    def post(self, request):
        try:
            post_config = parse_post_config(request.data)
            rendered_post = self.post_creator.create(post_config)

            serializer = RenderedPostSerializer(rendered_post)
            response = Response(serializer.data)
            return response
        except NullPostId:
            response = Response({
                'exception': 'Id of post is null'
            }, 400)


class Members(APIView):
    """
    Update count of members of sources
    """
    def post(self, request):
        def update_members():
            for source in Source.objects.all():
                source_type = source.type_id
                if source_type.name == 'vk_group':
                    public_page = VKResolver.get_public_page_info(source.platform_id, source_type.token)
                    source.members = public_page.get('members_count', 0)
                    source.save()
                    time.sleep(1)

        threading.Thread(target=update_members).start()
        return Response(status=200)
