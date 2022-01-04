from flask import Flask, render_template, request
from common_functions import get_polarity
from textblob_functions import get_tb_tweets
from vader_functions import get_vader_tweets
import tweepy as tp

from twitter_auth import *

auth = tp.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tp.API(auth)

app = Flask(__name__)


@app.route('/', methods=['GET'])
def homepage():
    return render_template('index.html')


@app.route('/textblob', methods=['GET'])
def textblobpage():
    topic = 'biden'
    title = 'Data Vis Project 2021'
    df = get_tb_tweets(topic)

    pos, neg, neu = get_polarity(df)

    return render_template('textblob.html', pos=pos, neg=neg, neu=neu, topic=topic)


@app.route('/vader', methods=['GET'])
def vaderpage():
    topic = 'biden'
    title = 'Data Vis Project 2021'
    desc = 'A chart to visualise sentiment on ' + topic
    df = get_vader_tweets(topic)

    pos, neg, neu = get_polarity(df)

    labels = ['positive', 'negative', 'neutral']
    values = [pos, neg, neu]

    data = zip(labels, values)

    list_of_data = []

    for label, value in data:
        list_of_data.append({'name': label, 'y': value})

    return render_template('vader.html', title=title, description_text=desc, chart_name='Pie',
                           data_list=list_of_data)


@app.route('/tweets', methods=['POST'])
def tweetspage():  # put application's code here

    if request.method == 'POST':
        query = request.form['query']
        tweets = api.search(query)

        return render_template('results.html', query = tweets)

    return render_template('404.html')




if __name__ == '__main__':
    app.run()
