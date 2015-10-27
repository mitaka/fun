from django.core.management.base import BaseCommand, CommandError
from django.core.cache import cache

class Command(BaseCommand):
    help = 'Cleans redis cache for all post entryes'

    def handle(self, *args, **kwargs):
        cache.delete_pattern('template.cache.post.content*')
