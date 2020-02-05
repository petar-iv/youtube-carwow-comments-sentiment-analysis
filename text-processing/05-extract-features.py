import os
os.environ["NLTK_DATA"] = os.path.join("..", "nltk_data")

import pickle
from nltk.tokenize import word_tokenize
from datetime import datetime


print(datetime.utcnow())
# persistence_file = os.path.join("..", "persistence", "3-category-dataset.bin")
persistence_file = os.path.join("..", "persistence", "5-category-dataset.bin")
data_frames = pickle.load(open(persistence_file, 'rb'))
print("Dataset entries: " + str(len(data_frames)))

persistence_file = os.path.join("..", "persistence", "most-common-words.bin")
most_common_words = pickle.load(open(persistence_file, 'rb'))
print("Most common words count: " + str(len(most_common_words)))

features = most_common_words

# Code taken from: https://towardsdatascience.com/basic-binary-sentiment-analysis-using-nltk-c94ba17ae386
def extract_features(row):
    review = row["Review"]
    words = word_tokenize(review)
    features_in_review = {}
    for feature in features:
        feature_value = feature[0]
        if feature_value in words:
            features_in_review[feature_value] = True
    return features_in_review


features_and_category = []
row_number = 0
for _, row in data_frames.iterrows():
    row_number += 1
    if row_number % 5000 == 0:
        print("Processing row #" + str(row_number) + " (" + str(datetime.utcnow()) + ")")
    features_and_category.append((extract_features(row), row["Category"]))

# persistence_file = os.path.join("..", "persistence", "3-category-features-of-dataset-rows.bin")
persistence_file = os.path.join("..", "persistence", "5-category-features-of-dataset-rows.bin")
pickle.dump(features_and_category, open(persistence_file, 'wb'))
print(datetime.utcnow())
