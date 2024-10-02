![Logo](https://github.com/aditya8-8/MSP/blob/main/SCREENSHOTS/LOGO.png?raw=true)
# Project Title

**MSP** is designed to predict the success of a movie during both the production and post-production phases. By leveraging data available before a film's release, the system empowers stakeholders with predictive insights for decision-making.

The system predicts average ratings, which is the target variable, using features such as:

- Cast & Crew – Director, Actors, Producer, Writer
- Instagram – Follower counts
- YouTube – Video views

MSP is built using Django, with the machine learning model trained on datasets provided by IMDb for non-commercial use.

The model is trained using a Ridge Regressor that takes in **nconst** values (Name Constants, which are unique IDs assigned to people in the IMDb database), based on the movies they worked on. The training data includes over 300,000 movies identified by **tconst** values (Title Constants, unique IDs assigned to movie titles), along with their corresponding nconst values and ratings. The Ridge Regressor assigns a weight to each nconst based on how important that person is to the movie's rating.

To predict the rating of a new movie, the model calculates the sum of the weights of the people (nconsts) involved in the movie. This gives an estimate of the movie’s average rating. 

*This is a simplified description, as the Ridge Regressor uses a more complex mathematical formulation.*

In addition to the predicted score, the system incorporates additional scores based on YouTube view counts, Instagram follower counts, and scores for each genre. These additional scores are preset values determined based on the view count, follower count, and genres associated with a movie.

## API Reference

- A YouTube Data API key is essential for retrieving movie-related videos from YouTube and extracting their view counts.

- The Instaloader API is used to collect Instagram details of the cast and crew, with a temporary Instagram account logged in using a saved session. While Instagram’s official API would be ideal, financial constraints prevented its use. Developers are welcome to modify the **"utils4.py"** file inside the **movies** folder to incorporate Instagram's official API if desired.

## Deployment

To deploy this project:

1. **Clone the repository to your local machine:**

    ```bash
    git clone https://github.com/aditya8-8/MSP.git
    ```

2. **Install Django (ensure Python is installed on your machine):**

    ```bash
    pip install django
    ```

3. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Open PowerShell inside the local repo directory and run:**

    ```bash
    python manage.py migrate
    ```
    
    ```bash
    python manage.py collectstatic
    ```

5. **Host the Website on a Local Server:**
    
    *Double-click the **"RUN SERVER.bat"** Windows batch file in the project directory.*
    
    **OR**
    
    *You can run this in the same PowerShell window:*

    ```bash
    python manage.py runserver
    ```

6. **Access the Website:**
    
    *Copy and paste the URL shown in the terminal (usually http://127.0.0.1:8000/) into your web browser, or directly open the URL by pressing Ctrl and clicking the link displayed in the terminal.*

## Demo

[*Demo video to Add Movie to the database*](https://raw.githubusercontent.com/aditya8-8/MSP/main/DEMO/Add%20Movie.mp4)

[*Demo video of Prediction*](https://raw.githubusercontent.com/aditya8-8/MSP/main/DEMO/Predict.mp4)

## Acknowledgements

The initial code was sourced from [here](https://github.com/Saifur43/Movie-Success-Prediction). Special thanks to Saifur43 for the contribution.

Special thanks to IMDb for providing datasets for non-commercial use.

Contributions to this project are always welcome!

## Appendix

- **ML Model**
    
    The machine learning model is trained and saved as a .pkl file (Pickle format from the scikit-learn library), along with a corresponding dictionary vectorizer file used for encoding nconst values. The model can be retrained using updated datasets if necessary.

    The existing model, datasets, and the script to train the model are available in this [repository](https://github.com/aditya8-8/MSP/tree/main/ML%20Model). To train the model with updated datasets, ensure that they are in the same format and structure as the existing dataset file.

- **Dataset**

    The datasets can be downloaded from [here](https://developer.imdb.com/non-commercial-datasets/).

    These datasets are provided in .tsv format, with each file containing different types of information. The goal is to combine all these datasets into a single file, ensuring that it conforms to the format used in the project.

- **Visualization**

    After running predictions for a movie, you can execute the "VISUALIZE.bat" file located in the movies folder. This will provide insights into how the score was predicted and generate a weightage graph for each cast and crew member, plotted using Matplotlib.

    *Please note that the visualization will only display results for the last predicted movie.*

## Screenshots

- ***Homepage***
![App Screenshot](https://github.com/aditya8-8/MSP/blob/main/SCREENSHOTS/Homepage.png?raw=true)

- ***Movie Details***
![App Screenshot](https://github.com/aditya8-8/MSP/blob/main/SCREENSHOTS/Details.png?raw=true)

- ***Backend***
![App Screenshot](https://github.com/aditya8-8/MSP/blob/main/SCREENSHOTS/Backend.png?raw=true)

- ***Visualizing***
![App Screenshot](https://github.com/aditya8-8/MSP/blob/main/SCREENSHOTS/Visualising.png?raw=true)
