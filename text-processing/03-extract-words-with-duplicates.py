import os
os.environ["NLTK_DATA"] = os.path.join("..", "nltk_data")

import re
import nltk
import pickle
from datetime import datetime
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

print(datetime.utcnow())
persistence_file = os.path.join("..", "persistence", "5-category-dataset.bin")
data_frames = pickle.load(open(persistence_file, 'rb'))
print("Dataset entries: " + str(len(data_frames)))

stop_words = list(set(stopwords.words('english')))

# Code taken from: https://towardsdatascience.com/basic-binary-sentiment-analysis-using-nltk-c94ba17ae386
def extract_significant_words(row):
    review = row["Review"]
    pruned_review = re.sub(r'[^(a-zA-Z)\s]', '', review)  # take words only
    words = word_tokenize(pruned_review)
    cleaned = [w for w in words if w not in stop_words]
    tagged = nltk.pos_tag(cleaned)
    significant_words = []
    for word in tagged:
        if word[1] in ["JJ", "JJR", "JJS"]:  # Source: https://pythonprogramming.net/natural-language-toolkit-nltk-part-speech-tagging/
            significant_words.append(word[0].lower())
    return significant_words


all_words_with_duplicates = []
row_number = 0
for _, row in data_frames.iterrows():
    row_number += 1
    if row_number % 5000 == 0:
        print("Processing row #" + str(row_number) + " (" + str(datetime.utcnow()) + ")")
    for word in extract_significant_words(row):
        all_words_with_duplicates.append(word)

print("All words with duplicates count: " + str(len(all_words_with_duplicates)))
persistence_file = os.path.join("..", "persistence", "all-words-with-duplicates.bin")
pickle.dump(all_words_with_duplicates, open(persistence_file, 'wb'))
print(datetime.utcnow())
