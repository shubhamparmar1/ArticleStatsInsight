from data_scraping import scrape_data
import nltk
import os
import pandas as pd
from textstat import sentence_count
from nltk.tokenize import sent_tokenize
from nltk.corpus import cmudict

nltk.download('punkt')
nltk.download('cmudict')    

positive_words = []
negative_words = []

# Load your own lists of positive and negative words
with open('./MasterDictionary/positive-words.txt', 'r') as f:
    positive_words = f.read().splitlines()

with open('./MasterDictionary/negative-words.txt', 'r') as f:
    negative_words = f.read().splitlines()

# Initialize an empty set to store the stop words
stop_words = set()

# Specify the directory where your stopword files are
directory = 'StopWords/'

# Loop over all files in the directory
for filename in os.listdir(directory):
    # Only consider .csv files
    if filename.endswith('.txt'):
        with open(os.path.join(directory, filename), 'r') as f:
            # Add the stop words from this file to the set
            stop_words.update(f.read().splitlines())

# # Print the number of positive words and the first 10 positive words
# print(f"Number of positive words: {len(positive_words)}")
# print(f"First 10 positive words: {positive_words[:10]}")

# # Print the number of negative words and the first 10 negative words
# print(f"Number of negative words: {len(negative_words)}")
# print(f"First 10 negative words: {negative_words[:10]}")

# # Print the number of stop words and the first 10 stop words
# print(f"Number of stop words: {len(stop_words)}")
# print(f"First 10 stop words: {list(stop_words)[:10]}")

input_data = pd.read_excel("Input.xlsx")

d = cmudict.dict()

def nsyl(word):
    try:
        return [len(list(y for y in x if y[-1].isdigit())) for x in d[word.lower()]]
    except KeyError:
        # Word not found in cmudict
        return [0]
    
def calculate_metrics(text):
    # Tokenize the text
    tokens = nltk.word_tokenize(text)

    # Remove stopwords
    tokens = [token for token in tokens if token not in stop_words]

    # Calculate word count
    word_count = len(tokens)

    # Calculate positive and negative scores
    positive_score = sum(word in positive_words for word in tokens)
    negative_score = sum(word in negative_words for word in tokens)

    # Calculate polarity score
    polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)

    # Calculate subjectivity score
    subjectivity_score = (positive_score + negative_score) / (word_count + 0.000001)

    # Calculate average sentence length
    avg_sentence_length = word_count / sentence_count(text)

    # Calculate percentage of complex words
    complex_words = [word for word in tokens if word.isalpha() and nsyl(word)[0] > 2]
    percentage_complex_words = len(complex_words) / word_count

    # Calculate Fog Index
    fog_index = 0.4 * (avg_sentence_length + percentage_complex_words)

    # Calculate average number of words per sentence
    avg_words_per_sentence = word_count / len(sent_tokenize(text))

    # Calculate complex word count
    complex_word_count = len(complex_words)

    # Calculate syllable per word
    syllable_per_word = sum(nsyl(word)[0] for word in tokens) / word_count

    # Calculate personal pronouns
    personal_pronouns = sum(1 for word in tokens if word.lower() in ['i', 'me', 'my', 'mine', 'we', 'us', 'our', 'ours'])

    # Calculate average word length
    avg_word_length = sum(len(word) for word in tokens) / word_count

    return polarity_score, subjectivity_score, avg_sentence_length, percentage_complex_words, fog_index, avg_words_per_sentence, complex_word_count, word_count, syllable_per_word, personal_pronouns, avg_word_length

# Read the existing data
output_data = pd.read_excel('Output Data Structure.xlsx')

# Loop through the URLs and scrape data
for index, row in input_data.iterrows():
    url = row['URL'] 
    title, article_text = scrape_data(url)

    # Calculate metrics
    metrics = calculate_metrics(article_text)

    # Print metrics
    print(f'URL: {url}\nTitle: {title}\nMetrics: {metrics}\n')

    # Add metrics to output data
    # output_data.loc[index, 'Title'] = title
    output_data.loc[index, 'Polarity Score'] = metrics[0]
    output_data.loc[index, 'Subjectivity Score'] = metrics[1]
    output_data.loc[index, 'Avg Sentence Length'] = metrics[2]
    output_data.loc[index, 'Percentage Complex Words'] = metrics[3]
    output_data.loc[index, 'Fog Index'] = metrics[4]
    output_data.loc[index, 'Avg Words per Sentence'] = metrics[5]
    output_data.loc[index, 'Complex Word Count'] = metrics[6]
    output_data.loc[index, 'Word Count'] = metrics[7]
    output_data.loc[index, 'Syllable per Word'] = metrics[8]
    output_data.loc[index, 'Personal Pronouns'] = metrics[9]
    output_data.loc[index, 'Avg Word Length'] = metrics[10]

# Write output data back to Excel file
output_data.to_excel('Output Data Structure.xlsx', index=False)