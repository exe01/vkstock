from django.core.management.base import BaseCommand
from backend.stock_api.models import Type, Project, Source


class Command(BaseCommand):
    help = """Seed example project"""

    def handle(self, *args, **options):
        vk_type = Type(
            name='vk_group',
            token='125433e8125433e8125433e8b91226a08111254125433e84cb77682426af7c6780f2899',
        )
        vk_type.save()

        project1 = Project(
            name='Hype',
            token='17fbc948d00e2e6952b404a8b5523f74468dfea47c6c30d4f55428aae34dfb6eb3c66b16dff263ed10deb',
            type_id=vk_type
        )
        project1.save()

        source1_1 = Source(
            name='/dev/null',
            platform_id='72495085',
            type_id=vk_type,
            project_id=project1,

        )
        source1_1.save()

        source1_2 = Source(
            name='IT-KOT',
            platform_id='63708206',
            type_id=vk_type,
            project_id=project1,
        )
        source1_2.save()

        project2 = Project(
            name='IT Humor',
            token='17fbc948d00e2e6952b404a8b5523f74468dfea47c6c30d4f55428aae34dfb6eb3c66b16dff263ed10deb',
            type_id=vk_type
        )
        project2.save()

        source2_1 = Source(
            name='4ch',
            platform_id='45745333',
            type_id=vk_type,
            project_id=project2,
        )
        source2_1.save()

        source2_2 = Source(
            name='Мемы',
            platform_id='45045130',
            type_id=vk_type,
            project_id=project2,
        )
        source2_2.save()
