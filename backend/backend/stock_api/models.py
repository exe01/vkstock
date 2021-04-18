from django.db import models
from PIL import Image


# CHANGE TYPE OF DELETE RENDERED POST

class Type(models.Model):
    name = models.CharField(max_length=32)
    token = models.CharField(max_length=256)


class Project(models.Model):
    name = models.CharField(max_length=256)
    token = models.CharField(max_length=256)
    platform_id = models.CharField(max_length=256, default="", blank=True)
    type_id = models.ForeignKey(Type, on_delete=models.CASCADE)


class Source(models.Model):
    name = models.CharField(max_length=256)
    platform_id = models.CharField(max_length=256)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    type_id = models.ForeignKey(Type, on_delete=models.CASCADE)


class Post(models.Model):
    date = models.IntegerField(default=0)
    platform_id = models.CharField(max_length=256)
    source_id = models.ForeignKey(Source, null=True, on_delete=models.SET_NULL)
    text = models.TextField(blank=True)
    rating = models.IntegerField(default=0)

    def get_pillow_first_image(self):
        pil_image = None
        post_images = self.images.all()
        if len(post_images) > 0:
            image_model = post_images[0]
            image_model.image.open()
            pil_image = Image.open(image_model.image)

        return pil_image


class PostImage(models.Model):
    post_id = models.ForeignKey(Post, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images')


class Comment(models.Model):
    user_name = models.CharField(max_length=256)
    text = models.TextField(default='', blank=True)
    ref_text = models.TextField(default='', blank=True)
    post_id = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    image = models.ImageField(upload_to='comment_images', null=True)

    def get_pillow_image(self):
        pil_image = None
        try:
            self.image.open()
            pil_image = Image.open(self.image)
        except ValueError:
            return None

        return pil_image

class RenderedPost(models.Model):
    STATUS_CHOICES = [
        ('AC', 'accepted'),
        ('UN', 'unaccepted'),
        ('RE', 'rejected'),
        ('PO', 'posted'),
    ]

    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    platform_id = models.CharField(max_length=256)
    posted_date = models.IntegerField(default=0)
    text = models.TextField(blank=True)
    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default='UN'
    )


class RenderedImage(models.Model):
    rendered_post_id = models.ForeignKey(RenderedPost, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='rendered_images')
