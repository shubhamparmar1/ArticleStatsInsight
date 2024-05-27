# ArticleStatsInsight

## Objective
The objective of this project is to extract textual data from articles provided in given URLs and perform text analysis to compute various metrics. The metrics include sentiment scores, readability scores, and other textual statistics.

## Data Extraction

### Input
The URLs of the articles are provided in the `Input.xlsx` file. For each URL, the program extracts the article text and saves it in a text file named after the URL_ID.

### Extraction Process
- Only the article title and text are extracted.

## Data Analysis
For each extracted text, perform textual analysis to compute the variables as specified in the `Output Data Structure.xlsx` file.

 Dependencies:
   ```sh
    BeautifulSoup
    NLTK
    Pandas
    Requests
