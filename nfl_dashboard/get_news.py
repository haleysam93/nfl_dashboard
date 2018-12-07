import pandas as pd
import requests
from datetime import date, timedelta

GNEWS_API_KEY = '0a1bc2f716d1480b9f01431a2ea0e296'
news_url_all = 'https://newsapi.org/v2/everything'

def result_to_df(json, search_key):
    data = {'search_key':[], 'title':[], 'description':[], 'source':[],
            'date':[], 'url':[]}
    for article in json['articles']:
        data['search_key'].append(search_key)
        data['title'].append(article['title'])
        data['description'].append(article['description'])
        data['source'].append(article['source']['name'])
        data['date'].append(article['publishedAt'])
        data['url'].append(article['url'])
    return pd.DataFrame(data)

def get_news(search_keys, num_days=5):
    """Search for news for the search keys provided."""
    news = []
    from_date = (date.today() - timedelta(num_days)).strftime('%Y-%m-%d')
    for search_key in search_keys:
        params = {'q':search_key, 'from':from_date,
                  'sortBy':'relevancy', 'apiKey':GNEWS_API_KEY}
        json_result = requests.get(news_url_all, params=params).json()
        news.append(result_to_df(json_result, search_key))
    return pd.concat(news, ignore_index=True)
