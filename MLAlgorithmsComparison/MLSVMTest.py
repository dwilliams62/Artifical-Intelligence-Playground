import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score

# Read the processed data
data = pd.read_csv('processed_articles_sanitized.csv')

# Prepare the features (X) and labels (y)
X = data[['title', 'abstract']]   # Using 'title' and 'abstract' for training
y = data['category']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Convert text data into tf-idf features
vectorizer = TfidfVectorizer(max_features=1000)
X_train_tfidf = vectorizer.fit_transform(X_train['title'] + ' ' + X_train['abstract'])
X_test_tfidf = vectorizer.transform(X_test['title'] + ' ' + X_test['abstract'])

# Train the SVM model
model = SVC(kernel='linear', C=1, random_state=42)  # Using a linear kernel for the SVM
model.fit(X_train_tfidf, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test_tfidf)

# Evaluate the accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Model accuracy: {accuracy}")

# Perform 5-fold cross-validation
scores = cross_val_score(model, X_train_tfidf, y_train, cv=5)  # Use y_train instead of y

print(f"Cross-validation scores: {scores}")
print(f"Average accuracy: {scores.mean()}")