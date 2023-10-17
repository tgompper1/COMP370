import requests
import datetime

from datetime import date

API_KEY = "22c05da432d1401a922f84a455e251b7"
TODAY = date.today()
LANGUAGE = "en"

ARTICLES_QUERY_STRING_TEMPLATE = "https://newsapi.org/v2/everything?q={}&from={}&language={}&apiKey={}"

# queries NewsAPI and returns python list of english news articles 
#   (represented as dicts) containing news_keywords and published in the last <lookback> days
def fetch_latest_news(api_key, news_keywords, lookback=10):

    keywords = "+AND+".join(news_keywords)
    date_to_sub = datetime.timedelta(lookback)
    from_date = TODAY-date_to_sub
    query_string = ARTICLES_QUERY_STRING_TEMPLATE.format(keywords, from_date, LANGUAGE, api_key)

    response = requests.get(query_string)


    
    data = response.json()

    if data["status"] == "error":
         raise Exception("unable to fetch articles")

    return data["articles"]

# if __name__ == '__main__':
#     print(fetch_latest_news(API_KEY, []))