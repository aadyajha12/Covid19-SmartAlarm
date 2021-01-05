import requests
import json
import config

config = json.load(open('config.json'))
API_KEY = config['news_api_key']
def covid_news(API_KEY):
    url = 'https://newsapi.org/v2/top-headlines'
    keywords = [ "coronavirus","covid-19","covid19","corona virus","vaccine","pandemic","virus",]
    parameter = {
        'q': keywords,
        'source': 'bbc-news',
        'sortBy': 'top',
        'language': 'en',
        #'country': 'uk',
        
    }
    headers = {
        'X-Api-Key': API_KEY,  # KEY in header to hide it from url
    }
    s = str(headers)
    response = requests.get(url, params=parameter, headers=s)
    data = response.json()
    articles = data['articles'][0:10]
    results = [j["title"] for j in articles]

    for i,j in enumerate(results,1):
        print(i,j)

if __name__ == "__main__":
    covid_news(API_KEY)