import re

def clean_tweet(input):
    return re.sub('[^A-Za-z0-9 ]+','', input)

def get_polarity(tweets):
    return (tweets['sentiment']> .30).sum(), (tweets['sentiment']< -.30).sum(), (tweets['sentiment'].between(-.30, .30)).sum()
