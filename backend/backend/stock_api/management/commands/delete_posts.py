from django.core.management.base import BaseCommand
from backend.stock_api.models import Post


class Command(BaseCommand):
    help = """Delete all posts, post_images, rendered_posts
    rendered_images, comments"""

    def handle(self, *args, **options):
        resp = Post.objects.all().delete()
        print(resp)
