from django.db import models


class Type(models.Model):
    """Type of platform for getting and posting posts.
    """
    name = models.CharField(max_length=150)


class Project(models.Model):
    name = models.CharField(max_length=200)
    type_id = models.ForeignKey(Type, on_delete=models.CASCADE)


class Worker(models.Model):
    token = models.CharField(max_length=1000)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    type_id = models.ForeignKey(Type, on_delete=models.CASCADE)


class Source(models.Model):
    name = models.CharField(max_length=200)
    platform_id = models.CharField(max_length=1000)
    worker_id = models.ForeignKey(Worker, on_delete=models.CASCADE)
    last_record_id = models.CharField(max_length=1000)


class Post(models.Model):
    platform_id = models.CharField(max_length=1000)


class Comment(models.Model):
    user_name = models.CharField(max_length=200)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
