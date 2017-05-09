Greg Szumel and Erik Kessler
CSCI 375 Final Project: Viewed More

### Installing Dependencies ###

Required modules are stored in 'requirements.txt'.
Install with: pip install -r requirements.txt

### Title/View Count Extraction ###

We extracted titles and view counts for our dataset by downloading
the 'videos' page for each uploader in our uploader list and parsing
the html to find the title and view counts on that page.

To run the title and view count extractor use:
   python get_titles_and_views.py <input_file> <output_file>


### Tagging ###

To tag video titles, we used the mean and SD of view counts for
each uploader then looked at how many SD from the mean each title was.

To get the mean and SD values use:
   pyton get_mean_sd.py <input_file> <output_file>
