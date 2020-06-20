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
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class TypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        depth = 1


class SourceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Source
        fields = '__all__'


class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        depth = 1


class PostImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PostImage
        fields = '__all__'


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class RenderedPostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RenderedPost
        fields = '__all__'
        depth = 1


class RenderedImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RenderedImage
        fields = '__all__'
