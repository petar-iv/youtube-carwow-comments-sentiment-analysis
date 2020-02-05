import os
import pickle
import pandas as pd
from datetime import datetime


CATEGORY_NEGATIVE = "negative"
CATEGORY_SLIGHTLY_NEGATIVE = "s-negative"
CATEGORY_NEUTRAL = "neutral"
CATEGORY_SLIGHTLY_POSITIVE = "s-positive"
CATEGORY_POSITIVE = "positive"

def classify_rating(row):
    num_rating = row["Rating"]
    if 1.0 <= num_rating < 2.7:
        return CATEGORY_NEGATIVE
    if 2.7 <= num_rating < 3.3:
        return CATEGORY_NEUTRAL
    if 3.3 <= num_rating <= 5.0:
        return CATEGORY_POSITIVE
    raise ValueError("This code wasn't prepared for a car with a rating of " + str(num_rating))


# def classify_rating(row):
#     num_rating = row["Rating"]
#     if 1.0 <= num_rating < 2.0:
#         return CATEGORY_NEGATIVE
#     if 2.0 <= num_rating < 2.7:
#         return CATEGORY_SLIGHTLY_NEGATIVE
#     if 2.7 <= num_rating < 3.3:
#         return CATEGORY_NEUTRAL
#     if 3.3 <= num_rating < 4.0:
#         return CATEGORY_SLIGHTLY_POSITIVE
#     if 4.0 <= num_rating <= 5.0:
#         return CATEGORY_POSITIVE
#     raise ValueError("This code wasn't prepared for a car with a rating of " + str(num_rating))


print(datetime.utcnow())
data_frames_list = []
for relative_path, directories, files in os.walk(os.path.join("..", "datasets", "normalized-edmundsconsumer-car-ratings-and-reviews")):
    for file in files:
        data = pd.read_csv(os.path.join(relative_path, file))
        data_frames_list.append(data)
data_frames = pd.concat(data_frames_list, axis=0)

data_frames["Category"] = data_frames.apply(lambda row: classify_rating(row), axis=1)

print("Dataset entries: " + str(len(data_frames)))

persistence_file = os.path.join("..", "persistence", "3-category-dataset.bin")
pickle.dump(data_frames, open(persistence_file, 'wb'))
print(datetime.utcnow())
