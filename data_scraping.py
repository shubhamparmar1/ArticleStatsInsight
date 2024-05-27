import requests
from bs4 import BeautifulSoup
import pandas as pd

# Read the input file
input_data = pd.read_excel("Input.xlsx")

def scrape_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the title
    title_tag = soup.find('h1', class_='entry-title')
    title = title_tag.text if title_tag else "Title not found"
    
    # Find the article text
    article_tag = soup.find('div', class_='td-post-content tagdiv-type')
    article_text = article_tag.text if article_tag else "Article text not found"
    
    return title, article_text

# # Loop through the URLs and scrape data
# for index, row in input_data.iterrows():
#     url = row['URL']  # assuming the column name in the excel file is 'URLs'
#     title, article_text = scrape_data(url)
#     print(f'Title: {title}\nArticle Text: {article_text}\n')