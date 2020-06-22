from django.db import models


# CHANGE TYPE OF DELETE RENDERED POST

class Type(models.Model):
    name = models.CharField(max_length=32)


class Project(models.Model):
    name = models.CharField(max_length=256)
    type_id = models.ForeignKey(Type, on_delete=models.CASCADE)


class Source(models.Model):
    name = models.CharField(max_length=256)
    platform_id = models.CharField(max_length=512)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    last_record_id = models.CharField(max_length=512)
    type_id = models.ForeignKey(Type, on_delete=models.CASCADE)


class Post(models.Model):
    platform_id = models.CharField(max_length=512)
    source_id = models.ForeignKey(Source, on_delete=models.CASCADE)
    text = models.TextField()


class PostImage(models.Model):
    path = models.CharField(max_length=512)
    post_id = models.ForeignKey(Post, related_name='images', on_delete=models.CASCADE)


class Comment(models.Model):
    user_name = models.CharField(max_length=256)
    post_id = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)


class RenderedPost(models.Model):
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    platform_id = models.CharField(max_length=512)
    text = models.TextField()


class RenderedImage(models.Model):
    rendered_post_id = models.ForeignKey(RenderedPost, related_name='images', on_delete=models.CASCADE)
    path = models.CharField(max_length=512)


