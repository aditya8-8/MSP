from django.core.management.base import BaseCommand
from movies.utils2 import find_instagram

class Command(BaseCommand):
    help = 'Find Instagram follower counts for given names'

    def handle(self, *args, **kwargs):
        names = "Nivin Pauly, Anaswara Rajan, Dhyan Sreenivasan, Shine Tom Chacko"
        counts_string = find_instagram(names)
        self.stdout.write(self.style.SUCCESS(f"{counts_string}"))

