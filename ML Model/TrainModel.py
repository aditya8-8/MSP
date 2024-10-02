import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error
from sklearn.feature_extraction import DictVectorizer
import joblib

# Step 1: Ask for user input for the dataset file path
dataset_file_path = input("Enter the path to the dataset file (.tsv): ")

# Step 2: Load the dataset
data = pd.read_csv(dataset_file_path, sep='\t')

# Step 3: Preprocess the data
# Convert the 'Cast&Crew' column into a list of strings
data['Cast&Crew'] = data['Cast&Crew'].str.split(',')

# Initialize DictVectorizer
vectorizer = DictVectorizer()

# Transform the 'Cast&Crew' column into a feature matrix
X = vectorizer.fit_transform(data['Cast&Crew'].apply(lambda x: {actor: 1 for actor in x}))

# Extract the target variable
y = data['averageRating']

# Step 4: Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 5: Train a machine learning model with L2 regularization
model = Ridge(alpha=0.1)  # You can adjust the value of alpha for the strength of regularization
model.fit(X_train, y_train)

# Step 6: Evaluate the model
train_predictions = model.predict(X_train)
test_predictions = model.predict(X_test)
train_rmse = mean_squared_error(y_train, train_predictions, squared=False)
test_rmse = mean_squared_error(y_test, test_predictions, squared=False)
print(f"Train RMSE: {train_rmse}")
print(f"Test RMSE: {test_rmse}")

# Step 7: Dump the trained model and DictVectorizer
model_file_path = 'movie_rating_prediction_model_with_l2.pkl'
joblib.dump(model, model_file_path)
print(f"Trained model with L2 regularization saved to {model_file_path}")

vectorizer_file_path = 'dict_vectorizer.pkl'
joblib.dump(vectorizer, vectorizer_file_path)
print(f"DictVectorizer saved to {vectorizer_file_path}")
