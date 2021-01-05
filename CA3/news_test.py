import json
from newsapi import covid_news 

def news_test_one():
    news_json = json.load(open('gb-news.json'))
    news:str = covid_news(news_json)
    assert news[0]['title'] != None