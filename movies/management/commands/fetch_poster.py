from django.core.management.base import BaseCommand
from movies.utils2 import fetch_movie_poster, download_poster

class Command(BaseCommand):
    help = 'Fetches the poster for a given movie'

    def add_arguments(self, parser):
        parser.add_argument('movie_title', type=str, help='Title of the movie')
        parser.add_argument('release_year', type=int, help='Release year of the movie')

    def handle(self, *args, **kwargs):
        movie_title = kwargs['movie_title']
        release_year = kwargs['release_year']
        
        poster_url = fetch_movie_poster(movie_title, release_year)
        if poster_url:
            download_path = download_poster(poster_url, movie_title)
            self.stdout.write(self.style.SUCCESS(f'Successfully fetched and downloaded poster for {movie_title} ({release_year}). File saved at: {download_path}'))
        else:
            self.stdout.write(self.style.WARNING(f'Failed to fetch poster for {movie_title} ({release_year}).'))
