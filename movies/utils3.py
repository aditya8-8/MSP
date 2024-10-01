import os
import re
import requests
from requests.exceptions import Timeout
from django.conf import settings

# Function to fetch movie poster URL from TMDb API
def fetch_movie_poster(movie_title, release_year):
    api_key = 'fb7bb23f03b6994dafc674c074d01761'
    timeout = 7  # Timeout set to 15 seconds

    try:
        # Search using both movie title and release year
        search_url = f'https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_title}&year={release_year}'
        response = requests.get(search_url, timeout=timeout)
        response.raise_for_status()
        data = response.json()
        if data['results']:
            for movie in data['results']:
                if movie['title'].lower() == movie_title.lower() and str(movie['release_date'][:4]) == release_year:
                    poster_path = movie.get('poster_path')
                    if poster_path:
                        poster_url = f'https://image.tmdb.org/t/p/original{poster_path}'
                        print(f"{poster_url}")
                        return poster_url

        # If poster not found, Search using only movie_title
        print("Searching using Movie Title Only")
        search_url_without_year = f'https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_title}'
        response = requests.get(search_url_without_year, timeout=timeout)
        response.raise_for_status()
        data = response.json()
        if data['results']:
            movie = data['results'][0]
            poster_path = movie.get('poster_path')
            if poster_path:
                poster_url = f'https://image.tmdb.org/t/p/original{poster_path}'
                print(f"{poster_url}")
                return poster_url 
    except (Timeout, ConnectionError) as e:
        print()
        print("Network Error")
        print()
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while fetching movie poster: {e}")
    return None

# Function to sanitize the movie title
def sanitize_movie_title(movie_title):
    return re.sub(r'[^\w\s]', '_', movie_title)

# Function to download the poster image
def download_poster(poster_url, movie_title):
    if poster_url:
        try:
            response = requests.get(poster_url)
            if response.status_code == 200:
                sanitized_title = sanitize_movie_title(movie_title)
                filename = f"{sanitized_title}.jpg"
                media_root = settings.MEDIA_ROOT
                filepath = os.path.join(media_root, filename)
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                print()
                print("Please verify if the Poster is related to the Movie : ")
                print()
                print(f"{poster_url}")
                print()
                user_input = input(print("Add to Database ? (Y/N): "))
                if user_input.upper() == "Y":
                    print()
                    print("Poster Downloaded")
                    return filepath 
                else:
                    print()
                    print("No Poster Found!")
                    return None
            else:
                print(f"Failed to download poster: HTTP status code {response.status_code}")
        except Exception as e:
            print(f"Error occurred while downloading poster: {e}")
    else:
        print("Poster URL not available.")

# Function to extract movie title and release year from input string
def fetch_poster(movie_name_with_year):
    print()
    print("Searching for Movie Poster...")
    match = re.match(r'(.+)\s\((\d{4})\)', movie_name_with_year)
    if match:
        movie_title = match.group(1)
        release_year = match.group(2)
        if movie_title and release_year:
            poster_url = fetch_movie_poster(movie_title, release_year)
            filepath = download_poster(poster_url, movie_title)
            if filepath:
                return filepath  # Return the filepath
            else:
                print("Poster not Found")
    else:
        print("Invalid input format. Please enter the title of the movie followed by its release year in parentheses.")

