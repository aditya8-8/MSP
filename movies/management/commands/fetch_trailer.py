# Inside fetch_trailer.py

from django.core.management.base import BaseCommand
from movies.utils3 import fetch_trailer_info  # Import your fetch_trailer_info function

class Command(BaseCommand):
    help = 'Fetches trailer information for a given movie title'

    def add_arguments(self, parser):
        parser.add_argument('movie_title', type=str, help='Title of the movie')

    def handle(self, *args, **kwargs):
        movie_title = kwargs['movie_title']
        trailer_url, view_count = fetch_trailer_info(movie_title)
        self.stdout.write(f'Trailer URL: {trailer_url}')
        self.stdout.write(f'View Count: {view_count}')
