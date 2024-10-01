import csv
import os
import pandas as pd
import joblib
from sklearn.feature_extraction import DictVectorizer
import imdb

# Create an IMDb object
ia = imdb.IMDb()

def fetch_tconst(movie_name):
    # Search for the movie by name
    search_results = ia.search_movie(movie_name)
    
    # Get the first result (assuming it's the most relevant)
    if search_results:
        movie = search_results[0]
        return "tt" + movie.movieID
    else:
        return None

def fetch_nconst(name):
    # Search for the person by name
    search_results = ia.search_person(name)
    
    # Get the first result (assuming it's the most relevant)
    if search_results:
        person = search_results[0]
        print("nm" + person.personID)
        return "nm" + person.personID
    else:
        return None

def fetch_n_predict(movie_name, directors, writers, producers, cast):
    # Split names into lists
    print("Fetching Unique IDs from IMDb...")
    tconst = fetch_tconst(movie_name)
    directors_list = directors.split(", ")
    writers_list = writers.split(", ")
    producers_list = producers.split(", ")
    cast_list = cast.split(", ")

    # Initialize the combined list with directors
    all_list = directors_list.copy()

    # Add writers to the combined list
    for writer in writers_list:
        if writer not in all_list:
            all_list.append(writer)

    # Add producers to the combined list
    for producer in producers_list:
        if producer not in all_list:
            all_list.append(producer)

    # Add cast members to the combined list
    for actor in cast_list:
        if actor not in all_list:
            all_list.append(actor)

    # Fetch nconst values and names for each person
    all_data = [(fetch_nconst(name), name) for name in all_list if name.strip()]
    if all_data:
        print("Fetched")
        # Determine the file paths in the same directory as the script
        cast_and_crew_file_path = os.path.join(os.path.dirname(__file__), "Cast_and_Crew.tsv")
        nconst_name_file_path = os.path.join(os.path.dirname(__file__), "Nconst_and_Name.tsv")
        print()
        print("Log files created : Cast_and_Crew.tsv , Nconst_and_Name.tsv")

        # Delete the files if they already exist
        if os.path.exists(cast_and_crew_file_path):
            #print("Exists")
            os.remove(cast_and_crew_file_path)
        if os.path.exists(nconst_name_file_path):
            #print("Exists")
            os.remove(nconst_name_file_path)

        # Write the combined names and nconst values to the TSV files
        with open(cast_and_crew_file_path, 'w', newline='', encoding='utf-8') as tsvfile:
            writer = csv.writer(tsvfile, delimiter='\t')
            writer.writerow(['Title', 'Cast&Crew'])
            writer.writerow([tconst, ','.join(nconst for nconst, _ in all_data)])

        with open(nconst_name_file_path, 'w', newline='', encoding='utf-8') as tsvfile:
            writer = csv.writer(tsvfile, delimiter='\t')
            writer.writerow(['Nconst', 'Name'])
            for nconst, name in all_data:
                writer.writerow([nconst, name])

        # Call the machine learning model
        predicted_rating = call_ml_model(cast_and_crew_file_path)

        return predicted_rating
    else:
        print("No data in IMDb")
        return None

def write_to_tsv(file_name, df):
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    df.to_csv(file_path, sep='\t', index=False)

def call_ml_model(tsv_file_path):
    # Load the TSV file
    try:
        df = pd.read_csv(tsv_file_path, delimiter='\t')
    except Exception as e:
        print("Error loading TSV file:", e)
        return None

    # Extract Cast&Crew data
    cast_and_crew_str = df.iloc[0]['Cast&Crew']
    cast_and_crew = cast_and_crew_str.split(',')

    # Load the saved model
    print()
    print(f"Loading Model and Encoder...")
    model_file_name = "Model.pkl"
    vectorizer_file_name = "dict_vectorizer.pkl"
    script_directory = os.path.dirname(__file__)
    model_path = os.path.join(script_directory, model_file_name)
    vectorizer_path = os.path.join(script_directory, vectorizer_file_name)

    try:
        with open(model_path, 'rb') as model_file:
            model = joblib.load(model_file)
    except Exception as e:
        print("Error loading Model:", e)
        return None

    try:
        with open(vectorizer_path, 'rb') as vectorizer_file:
            vectorizer = joblib.load(vectorizer_file)
    except Exception as e:
        print("Error loading the DictVectorizer Encoder:", e)
        return None

    try:
        # Convert the 'Cast&Crew' column into a list of dictionaries
        cast_and_crew_dict = {person: 1 for person in cast_and_crew}

        # Transform the data using the loaded DictVectorizer
        X_upcoming = vectorizer.transform([cast_and_crew_dict])

        # Predict averageRating for the upcoming movie
        prediction = model.predict(X_upcoming)
        print(f"Prediction Success")
    
        # Format the predicted rating to one decimal place
        predicted_rating = round(prediction[0], 1)
        print()
        print(f"Base Rating : {predicted_rating}")
        print()
        
        df.at[0, 'PredictedRating'] = predicted_rating

        # Save DataFrame back to TSV file
        write_to_tsv(tsv_file_path, df)

        return predicted_rating
    except Exception as e:
        print("Error during prediction:", e)
        return None