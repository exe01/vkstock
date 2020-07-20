from django.core.management.base import BaseCommand
from backend.stock_api.models import RenderedPost


class Command(BaseCommand):
    help = """Delete posted and rejected posts, post_images, rendered_posts
    rendered_images, comments"""

    def handle(self, *args, **options):
        for post in RenderedPost.objects.filter(status="RE"):
            try:
                resp = post.post_id.delete()
                print(resp)
            except KeyError:
                print('key error')

        for post in RenderedPost.objects.filter(status="PO"):
            try:
                resp = post.post_id.delete()
                print(resp)
            except KeyError:
                print('key error')

