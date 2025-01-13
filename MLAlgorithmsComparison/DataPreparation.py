import pandas as pd
import os
import re
from sklearn.model_selection import train_test_split
import logging

dropped_rows = []

# Set up logging
logging.basicConfig(filename='data_preprocessing.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def sanitize_text(text):
    """Sanitize text by removing special characters that might cause issues."""
    if pd.isna(text):
        return ""
    return re.sub(r'[^A-Za-z0-9\s\.,!?]', '', str(text))

def validate_record(row, min_abstract_length=25):
    """Validate that the record has necessary information."""
    if not row['title']:
        row['title'] = "No Title"
    if pd.isna(row['abstract']) or len(row['abstract'].split()) < min_abstract_length:
        return False
    return True

# Function to combine and sanitize specific CSV files
# Function to combine and sanitize specific CSV files
def combine_and_sanitize_csvs(folder_path):
    combined_data = pd.DataFrame()
    
    # List of specific CSV files to process
    csv_files = ['Biophysical.csv', 'Psychological.csv', 'Social.csv']
    
    for filename in os.listdir(folder_path):
        if filename in csv_files:
            file_path = os.path.join(folder_path, filename)
            df = pd.read_csv(file_path, on_bad_lines='skip')
            
            # Sanitize and validate data
            columns_to_keep = ['Key', 'title', 'abstract']  # Updated column names
            df = df[columns_to_keep]
            df['title'] = df['title'].apply(sanitize_text)
            df['abstract'] = df['abstract'].apply(sanitize_text)
            
            # Validate each row
            mask = df.apply(lambda row: validate_record(row), axis=1)
            valid_data = df[mask]
            dropped_rows.extend(df[~mask].index.tolist())
            
            # Add category based on filename (keeping original category names)
            valid_data['category'] = filename.split('.')[0].capitalize()
            combined_data = pd.concat([combined_data, valid_data], ignore_index=True)

    logging.info(f"Total rows dropped: {len(dropped_rows)}")
    logging.info(f"Rows dropped indices: {dropped_rows}")

    return combined_data

# Process the data
folder_path = r"C:\Users\User\Documents\GitHub2\Artificial-Intelligence-Playground\MLAlgorithmsComparison"  # Update this path
data = combine_and_sanitize_csvs(folder_path)

# Save processed data to a single CSV
output_path = 'processed_articles_sanitized.csv'
data.to_csv(output_path, index=False)

# Report data completeness
print(f"Total articles processed: {len(data)}")
print(f"Total articles dropped: {len(dropped_rows)}")

# Split the data into features (X) and labels (y)
X = data[['title', 'abstract']]   # Only use 'Title' and 'abstract' for training
y = data['category']

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Convert text data to tf-idf vectors for machine learning models
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer(max_features=2000)
X_train_tfidf = vectorizer.fit_transform(X_train['title'] + ' ' + X_train['abstract'])
X_test_tfidf = vectorizer.transform(X_test['title'] + ' ' + X_test['abstract'])