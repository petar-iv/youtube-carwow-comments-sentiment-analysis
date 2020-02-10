# youtube-carwow-comments-sentiment-analysis

Sentiment analysis of comments of videos from the [carwow channel](https://www.youtube.com/channel/UCUhFaUpnq31m6TNX2VKVSVA). The project follows [this tutorial](https://towardsdatascience.com/basic-binary-sentiment-analysis-using-nltk-c94ba17ae386).

Version of Node.js used: 10.x

Version of Python used: 3.6.1

Directories:
- `datasets`
    - `edmundsconsumer-car-ratings-and-reviews` - the files of the [original dataset](https://www.kaggle.com/ankkur13/edmundsconsumer-car-ratings-and-reviews) should be placed here.
    - `normalized-edmundsconsumer-car-ratings-and-reviews` - initially, the files of the original dataset should be placed here. After that the script `normalazing-dataset/01-normalize-edmundsconsumer-car-ratings-and-reviews.js` should be run in order to normalize the dataset a bit (the script changes the files in the `normalized-edmundsconsumer-car-ratings-and-reviews` directory).
- `nltk_data` - one should put here the additional modules required for NLTK processing.
- `normalazing-dataset` - contains Node.js script for normalizing the used dataset.
- `persistence` - the Python scripts in the `text-processing` directory save intermediate states in that folder.
- `text-processing` - contains Python scripts for handling the dataset files and teaching a model and for classifying the YouTube comments.
    - `01-process-dataset.py` - Assigns discrete categories for the entries in the used dataset (either ('Negavtive', 'Neutral', 'Positive') or ('Negavtive', 'Slightly Negative', 'Neutral', 'Slightly Positive', 'Positive') depending on which part of the code is commented out).
    - `02-count-entries-per-class.py` - counts how many entries there are in the dataset for each discrete category.
    - `03-extract-words-with-duplicates.py` - takes the *Reviews* from the dataset and extracts all adjectives.
    - `04-extract-most-common-words.py` - takes only the adjectives that are used 10 or more times. Those will be our features - the most significant words according to which we will classify the YouTube comments.
    - `05-extract-features.py` - extracts the features and the corresponding classification for every entry in the dataset.
    - `06-test-accuracy.py` - tests the accuracy of several different algorithms on the dataset (75% of the entries are used for training and the rest  for testing). Best ration accuracy/performance is provided by `SGDClassifier` and this is why it will be the one to be used for the YouTube comments classification.
    - `07-classify-youtube-comments.py` - takes the already fetched and pre-processed YouTube comments.
- `youtube-comments` - contains Node.js script for fetching content with the YouTube *v3* API.
    - `carwow-videos` - after running the script `01-fetch-videos-list.js` (Note: it might be necessary to stop the script's execution with *Ctrl-C* if it has done more iterations than needed for fetching the videos. Check in advance the number of videos in the channel) this directory should contain files with paged HTTP responses returned by the YouTube API. These files should contain video ids and video title.
    - `carwow-comments` - here we will have the comments from the videos.
    - `02-assemble-videos.js` - with this script we take only the relevant parts of the HTTP responses we already have in this directory. Then the resulting file is manually processed - we take only the videos related to a single automobile (no drag races, no motor shows videos). We choose 70 models we are interested in (and thus - 70 videos).
    - `03-fetch-comments.js` - with this we are fetching the comments for these 70 videos. The script is run for every video separately (Note: it might be necessary to stop the script's execution with *Ctrl-C* if it has done more iterations than needed to fetch the comments for a video. Check in advance the number of comments for the corresponding video).
    - `04-assemble-comments.js` - assembles all YouTube comments for all videos into a single file.
    Note regarding the content of `carwow-comments` and `carwow-videos` - the `assemble-*` scripts throw (unreadable) errors if run after they have been run once.
    - `key.js` - one should put his/her YouTube API key here.
