import os
import pickle

# persistence_file = os.path.join("..", "persistence", "3-category-dataset.bin")
persistence_file = os.path.join("..", "persistence", "5-category-dataset.bin")
data_frames = pickle.load(open(persistence_file, 'rb'))
print("Dataset entries: " + str(len(data_frames)))

results = {}
for index, row in data_frames.iterrows():
   category = row["Category"]
   if category in results:
      results[category] += 1
   else:
      results[category] = 1
print(results)
