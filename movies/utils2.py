import os
import re
import time
import requests
import pyshorteners
import googleapiclient.discovery
from googleapiclient.errors import HttpError
from imdb import IMDb
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Set up API key and build the YouTube Data API service
# Function to load or request the API key from the user
def get_api_key():
    # Get the directory of the current program file
    program_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define the path for the API key file in the same directory
    api_key_file = os.path.join(program_dir, 'api_key.txt')
    
    # Check if the API key is saved in the file
    if os.path.exists(api_key_file):
        # If the file exists, read the API key from it
        with open(api_key_file, 'r') as file:
            api_key = file.read().strip()
            if api_key:
                print("API Key loaded from file.")
                return api_key
            else:
                print("API Key file is empty.")
                print()
                print("Youtube Data API key needed to fetch related videos from Youtube")
                print()
                api_key = input(print("Please enter your YouTube Data API key: ")).strip()
        
                # Save the API key to the file for future use
                with open(api_key_file, 'w') as file:
                    file.write(api_key)
                print("API Key saved for future use.")
                return api_key
    else:
        # If the file does not exist, ask the user for the API key
        print()
        print("Youtube API key needed to fetch related videos from Youtube !!")
        print()
        api_key = input(print("Please enter your YouTube Data API key: ")).strip()
        
        # Save the API key to the file for future use
        with open(api_key_file, 'w') as file:
            file.write(api_key)
        print("API Key saved for future use.")
        return api_key

def fetch_trailer_info(movie_title):
    print()
    print("Searching for Related Videos...")
    print()
                
    api_service_name = "youtube"
    api_version = "v3"
    api_key = get_api_key()
    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)

    # Define the keywords to include in the search query
    keywords = ["Official Trailer", "Official Teaser", "Official Teaser Trailer", "Trailer", "Teaser", "Title video", "Title card",]
    
    # Initialize variables to store the maximum view count and corresponding trailer URL
    max_view_count = 0
    best_trailer_url = ""
    
    # Search for movie trailers using the YouTube Data API
    for title_option in [movie_title, re.sub(r'\s*\(\d{4}\)$', '', movie_title)]:
        for keyword in keywords:
            attempts = 0  # Initialize attempts counter
            while attempts < 3:  # Limit to 3 attempts
                try:
                    request = youtube.search().list(
                        q=f"{title_option} {keyword}",
                        part="id,snippet",
                        type="video",
                        maxResults=5,  # Fetch more results to increase chances of finding a match
                        channelType="any"  # Filter for YouTube channels only
                    )
                    
                    # Execute the request and retrieve the trailer link and view count
                    response = request.execute()
                    if 'items' in response:
                        for item in response['items']:
                            video_title = item['snippet']['title']
                            trailer_id = item['id']['videoId']
                            trailer_link = f"https://www.youtube.com/watch?v={trailer_id}"
                            
                            # Check if some part of the movie title is in the video title
                            if title_option.split('(')[0].strip().lower() in video_title.strip().lower() and keyword.strip().lower() in video_title.strip().lower():
                                # Fetch video details to get view count
                                video_request = youtube.videos().list(
                                    part='statistics',
                                    id=trailer_id
                                )
                                video_response = video_request.execute()
                                view_count = int(video_response['items'][0]['statistics']['viewCount'])
                                
                                # Update maximum view count and corresponding trailer URL if current trailer has more views
                                if view_count > max_view_count:
                                    max_view_count = view_count
                                    best_trailer_url = trailer_link
                                    break  # Exit loop if a matching trailer is found
                    break  # Exit the while loop if request is successful
                except HttpError as e:
                    # Catch HttpError 403 and prompt for a new API key
                    if e.resp.status == 403:
                        print()
                        print("API Limit Exceeded!")
                        print()
                        if attempts < 2:  # Check if there are attempts left
                            api_key = input(print("Please enter your new YouTube Data API key: ")).strip()

                            program_dir = os.path.dirname(os.path.abspath(__file__))
                            api_key_file = os.path.join(program_dir, 'api_key.txt')
                            with open(api_key_file, 'w') as file:
                                file.write(api_key)  # Save the new API key
                            print()
                            print("New API Key saved for future use.")
                            print()
                            # Rebuild the YouTube API client with the new key
                            youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)
                            attempts += 1  # Increment attempts counter
                        else:
                            print()
                            print("Exceeded maximum attempts for new API key. Skipping...")
                            print()
                            return None  # Skip further processing if attempts are exhausted
                    else:
                        print(f"An error occurred: {e}")
                        return None  # Exit if it's not a 403 error

    # If no trailer is found with any of the keywords
    if best_trailer_url:
        # Extract video_id from best_trailer_url
        video_id = best_trailer_url.split("=")[-1]
        
        # Check if the video is embeddable
        is_embeddable = check_video_embeddability(video_id,)
        
        if is_embeddable:
            print()
            print("Please verify if the video is related to the Movie : ")
            print()
            print(f"{best_trailer_url}")
            print()
            user_input = input(print("Add to Database ? (Y/N): "))
            if user_input.upper() == "Y":
                print()
                print("Related Video Found")
                return best_trailer_url, max_view_count
            elif user_input.upper() == "N":
                shortened_url = fetch_video_src(movie_title)
                best_trailer_url = shortened_url
                print()
                print("Please verify if the video is related to the Movie : ")
                print()
                print(f'Video from IMDb : {best_trailer_url}')
                print()
                user_input = input(print("Add to Database ? (Y/N): "))
                if user_input.upper() == "Y":
                    print()
                    print("Related Video Found")
                    return best_trailer_url, max_view_count
                else:
                    print("No related videos were found!")
                    return None
                
        else:
            print(f'Youtube Video Not Embeddable : {best_trailer_url}')
            print()
            shortened_url = fetch_video_src(movie_title)
            best_trailer_url = shortened_url
            print()
            print("Please verify if the video is related to the Movie : ")
            print()
            print(f'Video from IMDb : {best_trailer_url}')
            print()
            user_input = input(print("Add to Database ? (Y/N): "))
            if user_input.upper() == "Y":
                print()
                print("Related Video Found")
                return best_trailer_url, max_view_count
            else:
                print("No related videos were found!")
                return None
    else:
        print("No related videos were found!")
        return None

def check_video_embeddability(video_id):
    embed_url = f"https://www.youtube.com/embed/{video_id}"
    
    # Make a GET request to the embed URL
    response = requests.get(embed_url)
    
    # Check if the response contains "Video unavailable" message
    if "Video unavailable" in response.text:
        # Video is not embeddable
        return False
    else:
        # Video is embeddable
        return True

# Function to fetch the video source URL after clicking play
def fetch_video_src(title_name):
    # Initialize the IMDbPY instance
    ia = IMDb()

    # Search for the title name
    results = ia.search_movie(title_name)

    if results:
        # Get the first search result (assuming it's the most relevant)
        movie = results[0]

        # Get the IMDb ID (tconst) of the movie
        imdb_id = movie.movieID

        # Add the "tt" prefix to the IMDb ID
        imdb_id_with_prefix = "tt" + imdb_id

        # Construct the IMDb URL using the IMDb ID with prefix
        imdb_url = f"https://www.imdb.com/title/{imdb_id_with_prefix}/"
        print("Fetching Video from:", imdb_url)

        # Set Firefox options for headless mode
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')

        # Initialize the Firefox webdriver with headless options
        driver = webdriver.Firefox(options=options)

        try:
            # Open the IMDb page
            driver.get(imdb_url)
            print("Using Selenium to fetch Video")

            try:
                # Wait for the play button container to be present in the DOM
                play_button_container = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'ipc-lockup-overlay__content'))
                )

                # Execute JavaScript to simulate a click on the play button container
                driver.execute_script("arguments[0].click();", play_button_container)

                # Print a message indicating the play button is clicked
                print("Fetched")

                # Wait for the video to load (you can increase the time if needed)
                time.sleep(5)

            except TimeoutException:
                # If the play button is not found, assume the video is already playing
                print("Video Fetched")

            # Find the video element and get its source URL
            video_element = driver.find_element(By.CLASS_NAME, 'jw-video')
            video_src = video_element.get_attribute('src')

            # Shorten the video source URL
            shortener = pyshorteners.Shortener()
            shortened_url = shortener.tinyurl.short(video_src)

            # Print the shortened URL
            if shortened_url:
                return shortened_url
            print("Shortened Video Source URL:", shortened_url)

        finally:
            # Close the webdriver
            driver.quit()
    else:
        print("No results found for the given title.")
