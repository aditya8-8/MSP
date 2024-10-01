import os
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import django

# Function to load and process TSV file
def load_tsv_file(file_path):
    try:
        df = pd.read_csv(file_path, delimiter='\t')
    except Exception as e:
        print("Error loading TSV file:", e)
        return None
    cast_and_crew_str = df.iloc[0]['Cast&Crew']
    cast_and_crew = cast_and_crew_str.split(',')
    return cast_and_crew

# Function to load nconst to name mapping
def load_nconst_to_name_mapping(file_path):
    try:
        mapping_df = pd.read_csv(file_path, delimiter='\t')
        nconst_to_name = dict(zip(mapping_df['Nconst'], mapping_df['Name']))
        return nconst_to_name
    except Exception as e:
        print("Error loading nconst to name mapping file:", e)
        return None

# Get the directory of the script file
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct paths to the required files
nconst_name_path = os.path.join(script_dir, "Nconst_and_Name.tsv")
model_path = os.path.join(script_dir, "Model.pkl")
vectorizer_path = os.path.join(script_dir, "dict_vectorizer.pkl")
tsv_path = os.path.join(script_dir, "Cast_and_Crew.tsv")

# Load Model
try:
    with open(model_path, 'rb') as model_file:
        model = joblib.load(model_file)
except Exception as e:
    print("Error loading model:", e)
    exit()

# Load Vectorizer
try:
    with open(vectorizer_path, 'rb') as vectorizer_file:
        vectorizer = joblib.load(vectorizer_file)
except Exception as e:
    print("Error loading vectorizer:", e)
    exit()

# Load and process TSV file
cast_and_crew = load_tsv_file(tsv_path)
if cast_and_crew is None:
    exit()

# Load nconst to name mapping
nconst_to_name = load_nconst_to_name_mapping(nconst_name_path)
if nconst_to_name is None:
    exit()

# Convert the 'Cast&Crew' column into a list of dictionaries
cast_and_crew_dict = {person: 1 for person in cast_and_crew}

# Transform the data using the loaded DictVectorizer
X_upcoming = vectorizer.transform([cast_and_crew_dict])

# Predict averageRating for the upcoming movie and round to one decimal place
prediction = model.predict(X_upcoming)

prediction = round(prediction[0], 1)

print("Predicted Rating:", prediction)

# Get the indices of features in the input
input_feature_indices = [vectorizer.vocabulary_.get(feature, None) for feature in cast_and_crew_dict.keys()]

# Filter out None values (keys not found in vocabulary)
input_feature_indices = [index for index in input_feature_indices if index is not None]

# Ensure that input_feature_indices is not empty
if not input_feature_indices:
    print("No features found in the vocabulary.")
    exit()

# Get the coefficients for the input features
input_coefficients = model.coef_[input_feature_indices]

# Get the feature names for the input features
input_features = []
for feature, index in zip(cast_and_crew_dict.keys(), input_feature_indices):
    if feature in nconst_to_name:
        input_features.append(nconst_to_name[feature])
    else:
        input_features.append(feature)

# Print coefficients and corresponding features for the input features
print("\nCoefficients for input features:")
for feature, coefficient in zip(input_features, input_coefficients):
    print(f"{feature}: {coefficient}")

# Print intercept value of the model
print("\nIntercept value of the model:", model.intercept_)

# Print the formula used for prediction
print("\nFormula for prediction:")
print("Predicted Rating =", model.intercept_, end=' ')
for feature, coefficient in zip(input_features, input_coefficients):
    print(f"+ ({coefficient})", end=' ')

# Calculate the predicted rating using the formula
calculated_rating = model.intercept_
for feature, coefficient in zip(input_features, input_coefficients):
    calculated_rating += (coefficient)

# Print the calculated rating
print("\n\nCalculated Rating using the formula:", calculated_rating)

# Visualize importance of each feature
print("Plotting Graph...")
plt.figure(figsize=(8, 6))
plt.barh(input_features, abs(input_coefficients), color='salmon')
plt.xlabel('Importance')
plt.title('Importance of Features (Predicted Rating: {})'.format(prediction))
plt.gca().invert_yaxis()  # Invert y-axis to show most important features at the top
plt.tight_layout()
plt.show()

# Add a prompt to keep the script open
input("Press Enter to exit...")
