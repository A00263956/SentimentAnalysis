import re

def clean_tweet(input):
    return re.sub('[^A-Za-z0-9 ]+','', input)

def get_polarity(tweets):
    return (tweets['sentiment']> .25).sum(), (tweets['sentiment']< -.25).sum(), (tweets['sentiment'].between(-.25, .25)).sum()
