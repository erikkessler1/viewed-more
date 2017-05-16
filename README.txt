Greg Szumel and Erik Kessler
CSCI 375 Final Project: Viewed More

### About ###

Viewed More looks to classify YouTube video titles based on whether the title
is likely to bring in more or fewer videos than average.

Directory Structure:
 - crawling: code and intermediate files for generating the untagged dataset
 - post_processing: code and intermediate filed for filtering and tagging



### Installing Dependencies ###

Required modules are stored in 'requirements.txt'.
Install with: pip install -r requirements.txt



### Title/View Count Extraction ###

We extracted titles and view counts for our dataset by downloading
the 'videos' page for each uploader in our uploader list and parsing
the html to find the title and view counts on that page.

To run the title and view count extractor use:
   python get_titles_and_views.py <input_file> <output_file>

The resulting raw dataset is in 'dataset/videos_raw_all.csv'



### Tagging ###

To tag video titles, we used the mean and SD of view counts for
each uploader then looked at how many SD from the mean each title was.

To get the mean and SD values use:
   pyton get_mean_sd.py <input_file> <output_file>


To filter out non-English and young videos use:
   python post_process.py <input_file> <output_file>


The tagged dataset is in the 'dataset' dir.
There are datasets that include all languages and only English.
