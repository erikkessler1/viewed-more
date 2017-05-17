Greg Szumel and Erik Kessler
CSCI 375 Final Project: Viewed More

### About ###

Viewed More looks to classify YouTube video titles based on whether the title
is likely to bring in more or fewer videos than average.

Directory Structure:
 - src/crawling: code for gathering the raw data
 - src/procecessing: code for analyzing, filtering, and labeling data
 - src/classifier: code for the classifier
 - dataset: title, view count dataset
 - report.pdf: our final writeup


### Installing Dependencies ###

Required modules are stored in 'requirements.txt'.
Install with: pip install -r requirements.txt



### Video Fetching ###

We extracted titles and view counts for our dataset by downloading
the 'videos' page for each uploader in our uploader list and parsing
the html to find the title and view counts on that page.

To run the title and view count extractor use:
   python video_fetcher.py <input_file> <output_file>

The resulting raw dataset is in 'dataset/raw_all.csv'



### Processing and Labeling ###

To label video titles, we used the mean and SD of view counts for
each uploader then looked at how many SD from the mean each title was.

To get the mean and SD values use:
   pyton analyzer.py <input_file> <output_file>


To filter out non-English and young videos use:
   python processer.py <input_file> <output_file>


The labeled dataset is in the 'dataset' dir.
There are datasets that include all languages and only English.



### Building Classifiers ###

To build a new classifier use the following command:
   python src/classifying/train_classifier.py -b -s <save_location> -f unigram dataset/labeled_eng_train_t0_00.csv
   
Our trained classifiers are in the 'classifiers' directory.


### Testing Classifiers ###

To test a classifer use the following command:
   python src/classifying/test_classifier.py -f unigram dataset/labeled_eng_test.csv classifiers/eng_t0_00_unigram.cls

