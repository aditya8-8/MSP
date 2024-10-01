import re
import os
from django.db import models
from django.db.models.signals import pre_save
from django.db.models.signals import post_save
from django.dispatch import receiver  
from movies.utils1 import fetch_movie_details
from movies.utils2 import fetch_trailer_info
from movies.utils3 import fetch_poster
from movies.utils4 import find_instagram
from django.db import transaction

    
class Movies(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField(null=True, blank=True)
    runtime = models.CharField(blank=True, max_length=20)
    IMDb_link = models.URLField(blank=True)
    Plot = models.TextField(blank=True)
    g_score = models.DecimalField(max_digits=3, decimal_places=1, blank=True, default=0)
    genres = models.CharField(null=True, blank=True, max_length=600)
    image = models.ImageField(upload_to='images/', blank=True ,null=True)
    Predicted_Rating = models.FloatField(null=True, blank=True)
    Youtube_trailer_link = models.URLField(blank=True, max_length=500)
    Youtube_trailer_views = models.IntegerField(blank=True, default=0)
    v_score = models.DecimalField(max_digits=3, decimal_places=1, blank=True, default=0)
    directors = models.CharField(max_length=200, blank=True)
    writers = models.CharField(max_length=200, blank=True)
    producers = models.CharField(max_length=200, blank=True)
    cast = models.CharField(max_length=200, blank=True)
    c1_insta = models.URLField(blank=True, null=True)
    c1_followers = models.IntegerField(blank=True, default=0)
    c2_insta = models.URLField(blank=True, null=True)
    c2_followers = models.IntegerField(blank=True, default=0)
    c3_insta = models.URLField(blank=True, null=True)
    c3_followers = models.IntegerField(blank=True, default=0)
    c4_insta = models.URLField(blank=True, null=True)
    c4_followers = models.IntegerField(blank=True, default=0)
    f_score = models.DecimalField(max_digits=3, decimal_places=1, blank=True, default=0)


    class Meta:
        verbose_name_plural = "Movies"  # Specify the plural name explicitly

    def __str__(self):
        return self.name


@receiver(pre_save, sender=Movies)
def call_utils(sender, instance, **kwargs):

    if not instance.id:
        # Check if the movie name includes a year
        match = re.match(r'(.+)\s\((\d{4})\)', instance.name)
        if match:
            #print(f'Year included in Name')

            movie_name_with_year = instance.name
            
        else:

            #print(f'Year not included in Name')

            movie_name_with_year = f"{instance.name} ({instance.year})"

            #print(f'Year appended to Name :{movie_name_with_year}')
            

#MOVIE
        try:
            runtime, imdb_link, plot, genres, directors, writers, producers, cast = fetch_movie_details(movie_name_with_year)

            # Update the Movie's details field 
            if all([runtime, imdb_link, plot, genres, directors, writers, producers, cast]):
                instance.runtime = runtime
                instance.IMDb_link = imdb_link
                instance.Plot = plot
                instance.directors = directors
                instance.writers = writers
                instance.producers = producers
                instance.cast = cast
                
                if genres.strip().lower() != 'n/a':
                    instance.genres = genres

                print('Movie Details updated to Database')
            else:
                print('No source found for updating Movie Details')
                
        except Exception as movie_error:
            print(f"Error occurred while updating Movie Details: {movie_error}")

#YOUTUBE
        try:
                   
            trailer_link, view_count = fetch_trailer_info(movie_name_with_year)

            # Update Youtube trailer and views 
            if trailer_link and view_count:
                instance.Youtube_trailer_link = trailer_link
                instance.Youtube_trailer_views = view_count
                print('Video Source and View Count updated to Database')
            else:
                print('No source found for updating Video and Viewcount')

        except Exception as youtube_error:
            print(f"Error occurred while updating Youtube Details")

#POSTER
        try:
            movie_poster_path = fetch_poster(movie_name_with_year)

            # Update the movie's image field with the path to the poster image
            if movie_poster_path:
                instance.image = movie_poster_path
                print('Poster Source updated to Database')
            else:
                print('No source found for updating Poster')

        except Exception as poster_error:
            print(f"Error occurred while updating Poster: {poster_error}")

#INSTA     
        try:       
            counts_string = find_instagram(instance.cast)

            # Update Instagram URL trailer and followers

            # Split the counts_string by ", " to get individual URL: followers pairs
            if counts_string:
                pairs = counts_string.split(", ")
                # Initialize the counter
                counter = 1

                # Iterate over the pairs and assign them to the respective fields of the Movies model
                for pair in pairs:
                    url, followers = pair.split(": ")
                    url = url.strip()
                    followers = int(followers.split()[0])  # Extract the follower count and convert it to an integer

                    # Assign the URL and followers to the respective fields
                    setattr(instance, f"c{counter}_insta", url)
                    setattr(instance, f"c{counter}_followers", followers)

                    # Increment the counter
                    counter += 1

                    # Break the loop if all four fields are filled
                    if counter > 4:
                        break
                print()
                print('Instagram Details updated to Database')
            else:
                print('No source found for updating Instagram Details')

        except Exception as insta_error:
            print(f"Error occurred while updating Instagram Details: {insta_error}")
        print("-------------------------------------------------------------------------------------------------")

@receiver(post_save, sender=Movies)
def update_scores(sender, instance, **kwargs):
   
    update_fields = []

#V_SCORE
    if instance.Youtube_trailer_views < 1000000:
        ytv = 0.0
    elif 1000000 <= instance.Youtube_trailer_views <= 5000000:
        ytv = 0.1
    elif 5000000 < instance.Youtube_trailer_views <= 10000000:
        ytv = 0.2
    elif 10000000 < instance.Youtube_trailer_views <= 100000000:
        ytv = 0.3
    else:
        ytv = 0.4

    instance.v_score = ytv
    update_fields.append('v_score')

#F_SCORE
    followers = [instance.c1_followers, instance.c2_followers, instance.c3_followers, instance.c4_followers]

    score = 0
    count = 0
    for value in followers:
        if value > 1000000:
            if value >= 1000000 and value < 5000000:
                score += 0.1
            elif value >= 5000000 and value < 10000000:
                score += 0.2
            elif value >= 10000000 and value < 50000000:
                score += 0.3
            elif value >= 50000000:
                score += 0.4
            count += 1
    if count > 0 and score > 0:
        total_score = score / count
        instance.f_score = total_score
        update_fields.append('f_score')
    else:
        instance.f_score = 0.0
        update_fields.append('f_score')

#G_SCORE
    genre_scores = {
    "Action": 0.4,
    "Adult": -0.4,
    "Adventure": 0.3,
    "Animation": 0.2,
    "Biography": -0.7,
    "Comedy": 0.4,
    "Crime": 0.3,
    "Documentary": -1.0,
    "Drama": -0.1,
    "Family": 0.1,
    "Fantasy": 0.2,
    "Film-Noir": -0.1,
    "Game-Show": -0.1,
    "History": -0.6,
    "Horror": -0.4,
    "Music": -0.5,
    "Musical": -0.1,
    "Mystery": 0.3,
    "News": -0.3,
    "Reality-TV": -0.1,
    "Romance": 0.1,
    "Sci-Fi": 0.6,
    "Sport": -0.3,
    "Talk-Show": -0.1,
    "Thriller": 0.5,
    "War": -0.2,
    "Western": -0.2
}
    if instance.genres:
        genres_list = instance.genres.split(', ')
        total_score = 0
        count = 0
        for genre_name in genres_list:
            genre_score = genre_scores.get(genre_name.strip(), 0)  # Get the score from the dictionary
            total_score += genre_score
            count += 1
        if count > 0:
            mean_score = total_score / count
            instance.g_score = mean_score
            update_fields.append('g_score')
    
    if update_fields:
            with transaction.atomic():
                Movies.objects.filter(pk=instance.pk).update(**{field: getattr(instance, field) for field in update_fields})
