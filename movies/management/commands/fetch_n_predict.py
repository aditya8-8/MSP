# In fetch_prediction.py

from django.core.management.base import BaseCommand
from movies.models import Movies  # Importing the Movies model
from movies.utils import main

class Command(BaseCommand):
    help = 'Fetch prediction for a movie'

    def add_arguments(self, parser):
        parser.add_argument('movie_name', type=str, help='Title of the movie')


    def handle(self, *args, **kwargs):
        movie_name = kwargs['movie_name']
        predicted_rating = main(movie_name)
        
        if predicted_rating is not None:
            self.stdout.write(self.style.SUCCESS(f"Predicted rating for '{movie_name}': {predicted_rating}"))
        else:
            self.stdout.write(self.style.ERROR("Failed to fetch prediction"))

