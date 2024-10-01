from django.core.management.base import BaseCommand
from movies.utils1 import fetch_movie_details

class Command(BaseCommand):
    help = 'Fetch details of a movie from IMDb'

    def add_arguments(self, parser):
        parser.add_argument('movie_title', type=str, help='Title of the movie')

    def handle(self, *args, **kwargs):
        movie_title = kwargs['movie_title']
        runtime, imdb_link, plot, genres, directors, writers, producers, cast = fetch_movie_details(movie_title)

        if not runtime:
            self.stdout.write(self.style.ERROR('Failed to fetch movie details.'))
            return

        self.stdout.write(self.style.SUCCESS('Movie Details:'))
        self.stdout.write(f"Title: {movie_title}")
        self.stdout.write(f"Runtime: {runtime}")
        self.stdout.write(f"IMDb Link: {imdb_link}")
        self.stdout.write(f"Plot: {plot}")
        self.stdout.write(f"Genres: {genres}")
        self.stdout.write(f"Directors: {directors}")
        self.stdout.write(f"Writers: {writers}")
        self.stdout.write(f"Producers: {producers}")
        self.stdout.write(f"Cast: {cast}")
