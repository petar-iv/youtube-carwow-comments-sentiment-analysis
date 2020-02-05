import os
import pickle
import nltk
import random
from nltk.classify.scikitlearn import SklearnClassifier
# Available naive bayes flavours: https://scikit-learn.org/stable/modules/naive_bayes.html
from sklearn.naive_bayes import MultinomialNB, ComplementNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC
from datetime import datetime

persistence_file = os.path.join("..", "persistence", "3-category-features-of-dataset-rows.bin")
# persistence_file = os.path.join("..", "persistence", "5-category-features-of-dataset-rows.bin")
features_and_category = pickle.load(open(persistence_file, 'rb'))
print("Features and category count: " + str(len(features_and_category)))

train_rows_portion = 0.75
train_rows_count = int(train_rows_portion * len(features_and_category))


def test_accuracy(classifier):
    print(datetime.utcnow())
    wrapped = SklearnClassifier(classifier)

    for i in range(3):
        random.shuffle(features_and_category)
        train_rows = features_and_category[:train_rows_count]
        test_rows = features_and_category[train_rows_count:]
        wrapped.train(train_rows)
        print(type(classifier).__name__, "accuracy percent:", (nltk.classify.accuracy(wrapped, test_rows)) * 100)

    print(datetime.utcnow())
    print("\n")

test_accuracy(MultinomialNB())
test_accuracy(ComplementNB())
test_accuracy(BernoulliNB())
test_accuracy(LogisticRegression(max_iter=1000))
test_accuracy(SGDClassifier())
# test_accuracy(SVC())  # Hangs
