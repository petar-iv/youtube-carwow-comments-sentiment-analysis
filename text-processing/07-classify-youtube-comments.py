import os
os.environ["NLTK_DATA"] = os.path.join("..", "nltk_data")

import json
import pickle
from nltk.tokenize import word_tokenize
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.linear_model import SGDClassifier
from datetime import datetime

# persistence_file = os.path.join("..", "persistence", "3-category-features-of-dataset-rows.bin")
persistence_file = os.path.join("..", "persistence", "5-category-features-of-dataset-rows.bin")
features_and_category = pickle.load(open(persistence_file, 'rb'))
print("Features and category count: " + str(len(features_and_category)))

persistence_file = os.path.join("..", "persistence", "most-common-words.bin")
most_common_words = pickle.load(open(persistence_file, 'rb'))
print("Most common words count: " + str(len(most_common_words)))

features = most_common_words


print("Started training", datetime.utcnow())
classifier = SklearnClassifier(SGDClassifier())
classifier.train(features_and_category)
print("Training complete", datetime.utcnow())


def comment_to_feature_set(comment):
    words = word_tokenize(comment)
    features_in_review = {}
    for feature in features:
        feature_value = feature[0]
        if feature_value in words:
            features_in_review[feature_value] = True
    return features_in_review

car_counter = 0
print("Started classification of youtube comments", datetime.utcnow())
results = {}
with open(os.path.join("..", "youtube-comments", "carwow-comments", "all-comments.json"), "r", encoding="UTF-8") as f:
    cars = json.load(f)
    for car in cars:
        car_counter += 1
        results[car] = {}
        comments = cars[car]
        for comment in comments:
            category = classifier.classify(comment_to_feature_set(comment["text"]))
            if category in results[car]:
                results[car][category] += 1
            else:
                results[car][category] = 1
        print("(#" + str(car_counter) + ")", "Classification of comments for", car, "done")

# with open(os.path.join("..", "youtube-comments", "carwow-comments", "3-category-classification.json"), "w", encoding="UTF-8") as f:
with open(os.path.join("..", "youtube-comments", "carwow-comments", "5-category-classification.json"), "w", encoding="UTF-8") as f:
    json.dump(results, f, indent=2, sort_keys=True)

print("Classification of youtube comments complete", datetime.utcnow())
