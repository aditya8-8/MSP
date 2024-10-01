import imdb
import requests
from bs4 import BeautifulSoup
import re


# Define the function to convert minutes to hours and minutes
def convert_to_hours_minutes(minutes):
    try:
        minutes = int(minutes)
        hours = minutes // 60
        remaining_minutes = minutes % 60
        return f"{hours}h {remaining_minutes}m"
    except ValueError:
        return "N/A"

def construct_full_credits_url(imdb_id):
    if imdb_id:
        # Append "tt" to IMDb ID
        imdb_id_with_tt = "tt" + imdb_id
        # Construct the full credits URL
        full_credits_url = f"https://www.imdb.com/title/{imdb_id_with_tt}/fullcredits/"
        return full_credits_url
    else:
        return None

import requests
from bs4 import BeautifulSoup

def extract_produced_by_section(url):
    try:
        # Fetch the HTML content of the webpage
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the section with the "Produced by" header
        produced_by_section = soup.find('h4', {'name': 'producer'})

        # If the section is found, extract the names and their specific credits
        if produced_by_section:
            table = produced_by_section.find_next('table', {'class': 'simpleTable'})
            if table:
                # Define priorities for credits
                priorities = ["producer", "producer (produced by)", "executive producer", "co-producer"]
                
                # Extract names of producers and executive producers based on priorities
                produced_by_data = []
                producers_count = 0
                for priority in priorities:
                    for row in table.find_all('tr'):
                        name_cell = row.find('td', {'class': 'name'})
                        credit_cell = row.find('td', {'class': 'credit'})
                        if name_cell and credit_cell:
                            name = name_cell.get_text(strip=True)
                            credit = credit_cell.get_text(strip=True).lower()
                            if credit == priority and producers_count < 3:
                                produced_by_data.append((name, credit))
                                producers_count += 1
                    if producers_count == 3:
                        break  # Stop iteration if 3 producers are found
                if produced_by_data:
                    return produced_by_data
                else:
                    print("No producers found.")
            else:
                print("No table found in the 'Produced by' section.")
        else:
            print("Produced by section not found.")
    except requests.RequestException as e:
        print("Failed to fetch webpage:", e)
    except Exception as ex:
        print("An error occurred:", ex)
    return [("N/A", "N/A")] if len(produced_by_data) == 0 else produced_by_data

def fetch_movie_details(movie_title):
    print()
    print(f"Searching for Movie Details... : {movie_title}")
    ia = imdb.IMDb()

    try:
        # Search for the movie by title
        match = re.match(r'(.+)\s\((\d{4})\)', movie_title)
        if match:
           movie_title_without_year = match.group(1)
        search_result = ia.search_movie(movie_title)
        #print(f"{search_result}")
        if not search_result:
            return None, None, None, None, None, None, None, None
        
        # Get the first movie from the search results
        movie_id = search_result[0].movieID
        #print(f"{movie_id}")
        movie_temp1 = ia.get_movie(movie_id)
        print(f"IMDB : {movie_temp1['title']}")

        if movie_temp1['title'] == movie_title_without_year:
           #print("True")
           movie = movie_temp1
        else:
            #print("False")
            search_result = ia.search_movie(movie_title_without_year)
            if not search_result:
                return None, None, None, None, None, None, None, None
            
            movie_id = search_result[0].movieID
            #print(f"{movie_id}")
            movie_temp2 = ia.get_movie(movie_id)
            #print(f"IMDb : {movie_temp2['title']}")
            
            if movie_temp2['title'] == movie_title_without_year or movie_title_without_year in movie_temp2['title']:
                #print("True")
                movie = movie_temp2

        # Extract movie details
        imdb_link = ia.get_imdbURL(movie)
        print()
        print("Please verify the Movie link from IMDb : ")
        print()
        print(f"{imdb_link}")
        print()
        user_input = input(print("Proceed ? (Y/N): "))
        if user_input.upper() == "Y":
            print()
            print("Movie Found")
            runtime_minutes = movie.get('runtimes', ['N/A'])[0]
            runtime = convert_to_hours_minutes(runtime_minutes)
            plot = movie.get('plot', ['N/A'])[0]
            genres = ', '.join(movie.get('genres', ['N/A']))
            
            # Initialize dictionaries to store unique names for directors, writers, producers, and cast
            directors_dict = {}
            writers_dict = {}
            producers_dict = {}
            cast_dict = {}

            # Fetch directors
            directors_list = movie.get('directors', [])
            directors_list = [person for person in directors_list if person is not None and person.get('name')]
            for person in directors_list:
                if person['name'] not in directors_dict:
                    directors_dict[person['name']] = True
            directors = ', '.join(str(name) for name in directors_dict)

            # Fetch writers
            writers_list = movie.get('writers', [])
            writers_list = [person for person in writers_list if person is not None and person.get('name')]
            for person in writers_list:
                    if person['name'] not in writers_dict:
                        writers_dict[person] = True
            writers = ', '.join(str(name) for name in writers_dict)

            # Fetch producers
            imdb_id = movie_id
            full_credits_url = construct_full_credits_url(imdb_id)
            produced_by_data = extract_produced_by_section(full_credits_url)
            for name, _ in produced_by_data:
                if name not in producers_dict:
                    producers_dict[name] = True
            producers = ', '.join(str(name) for name in producers_dict)

            # Fetch cast
            cast_list = movie.get('cast', ['N/A'])[:4]  # Get only the first 4 members
            cast_list = [person for person in cast_list if person is not None and person.get('name')]
            cast_list = cast_list[:4]
            for person in cast_list:
                if person['name'] not in cast_dict:
                    cast_dict[person['name']] = True
            cast = ', '.join(str(name) for name in cast_dict)
            
            print()
            print("Movie Details fetched from IMDb")
            return  runtime, imdb_link, plot, genres, directors, writers, producers, cast
        else:
            print("Movie not found!")
            return None, None, None, None, None, None, None, None

    except Exception as e:
        return None, None, None, None, None, None, None, None

