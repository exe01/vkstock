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
from rest_framework import serializers


class ImageRepresentationModelSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super().to_representation(instance)

        request = self.context.get('request')
        if request and ret.get('image'):
            api_url = request.query_params.get('media_url')
            if api_url:
                if not api_url.endswith('/'):
                    api_url += '/'
                ret['image'] = api_url + ret['image']

        return ret


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = '__all__'


class PostImageSerializer(ImageRepresentationModelSerializer):
    image = serializers.ImageField(use_url=False, required=False)

    class Meta:
        model = PostImage
        fields = '__all__'


class CommentSerializer(ImageRepresentationModelSerializer):
    image = serializers.ImageField(use_url=False, required=False)

    class Meta:
        model = Comment
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    images = PostImageSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = '__all__'


class RenderedImageSerializer(ImageRepresentationModelSerializer):
    image = serializers.ImageField(use_url=False, required=False)

    class Meta:
        model = RenderedImage
        fields = '__all__'


class RenderedPostSerializer(serializers.ModelSerializer):
    images = RenderedImageSerializer(many=True, read_only=True)

    class Meta:
        model = RenderedPost
        fields = '__all__'
