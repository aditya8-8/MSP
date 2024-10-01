import instaloader
import requests
from bs4 import BeautifulSoup
import re
import os
import sys

def find_instagram(names):
    print()
    print("Searching for Instagram Accounts of Cast...")
    print()
    # Create an instance of Instaloader
    L = instaloader.Instaloader()

    user = "_.m.s.p_"
    script_directory = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the running script
    session_file_path = os.path.join(script_directory, f"{user}.session")  # Specify the session file path

    try:

        # Redirecting stdout to null to suppress the message
        sys.stdout = open(os.devnull, 'w')
        L.load_session_from_file(user, filename=session_file_path)  # Load the session from the file
        # Reset stdout to the original value
        sys.stdout = sys.__stdout__
        #print("Session Loaded")

    except Exception as e:
        pass
  
    # Split the names string into individual names
    names_list = [name.strip() for name in names.split(",")]

    # Dictionary to store follower counts and Instagram URLs
    follower_data = {}
    print("Instagram Accounts fetched")
    print()
    print("Please verify the authenticity of the Instagram accounts:")
    for name in names_list:
        print()
        print(f"{name}")
        # Constructing the search query for Google
        search_query = f"{name} Instagram"
        google_search_url = f"https://www.google.com/search?q={search_query}"

        # Sending a GET request to Google and parsing the HTML response
        response = requests.get(google_search_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Finding all the search results
        search_results = soup.find_all('a')

        # Looping through search results to find Instagram links
        for result in search_results:
            link = result.get('href')
            # Checking if the link is from Instagram
            if link and 'instagram.com' in link:
                # Extracting the username from the link using regex
                match = re.search(r'instagram.com/([\w\.\_]+)', link)
                if match:
                    username = match.group(1)
                    # Constructing the Instagram profile URL
                    instagram_url = f"https://www.instagram.com/{username}/?hl=en"

                    # Print and ask for user confirmation
                    print()
                    print(instagram_url)
                    print()
                    confirmation = input(print("Proceed with this account? (Y/N): ")).strip().lower()
                    if confirmation == "y":
                        # Retrieve the profile information of the specified Instagram user
                        profile = instaloader.Profile.from_username(L.context, username)
                        # Add the follower count and Instagram URL to the dictionary
                        follower_data[instagram_url] = profile.followers
                        break  # Stop searching once an Instagram link is found
                    elif confirmation == "n":
                        # If user says no, go to the next name
                        break
                    else:
                        print("Invalid input. Please enter 'Y' or 'N'.")
                    

    # Convert follower data dictionary to a string with Instagram URLs and follower counts
    result_strings = [f"{url}: {count} followers" for url, count in follower_data.items()]
    counts_string = ", ".join(result_strings)

    if not follower_data:  # If follower data is empty
        return None
    else:
        return counts_string
