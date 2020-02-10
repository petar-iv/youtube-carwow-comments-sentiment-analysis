import os
import nltk
import pickle
from datetime import datetime


print(datetime.utcnow())
persistence_file = os.path.join("..", "persistence", "all-words-with-duplicates.bin")
all_words_with_duplicates = pickle.load(open(persistence_file, 'rb'))
print("All words with duplicates count: " + str(len(all_words_with_duplicates)))

frequency_distribution = nltk.FreqDist(all_words_with_duplicates)
print("Unique words count: " + str(len(frequency_distribution)))
most_common_words = frequency_distribution.most_common(5295)
print("Most common words count: " + str(len(most_common_words)))

persistence_file = os.path.join("..", "persistence", "most-common-words.bin")
pickle.dump(most_common_words, open(persistence_file, 'wb'))
print(datetime.utcnow())
