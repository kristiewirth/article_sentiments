import requests
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from datetime import datetime
from dateutil.relativedelta import relativedelta
from secrets import API_KEY

nltk.download('vader_lexicon')

all_articles = []

page = 0
while page <= 100:
    r = requests.get(
        'https://api.nytimes.com/svc/search/v2/articlesearch.json',
        params={
            'sort': 'newest',
            'api-key': API_KEY,
            'page': page,
            'end_date': datetime.now() + relativedelta(days=-1),
        },
    )

    if r.status_code != 200:
        break

    result_articles = r.json()['response']['docs']

    all_articles += result_articles

    page += 1

sid = SentimentIntensityAnalyzer()

positive_articles = ''
for article in all_articles:
    scores = sid.polarity_scores(article['headline']['main'] + article['snippet'])
    if scores['pos'] > 0.25 and scores['neg'] < 0.1:
        positive_articles += (
            '\n\n\n<'
            + article['web_url']
            + '|*'
            + article['headline']['main']
            + '*>\n\n\n'
            + article['snippet']
            + '\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n'
        )

# requests.post(
#     'https://hooks.zapier.com/hooks/catch/3023316/o998k4q/',
#     params={'data': positive_articles},
# )
print(positive_articles)
