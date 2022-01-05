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

    labels = ['positive', 'neutral', 'negative']
    values = [pos, neu, neg]

    data = zip(labels, values)

    list_of_data = []
    drilldown = {}
    drilldown['neg'] = [['-1 to -0.9', 0], ['-0.9 to -0.8', 0], ['-0.8 to -0.7', 0], ['-0.7 to -0.6', 0],
                        ['-0.6 to -0.5', 0], ['-0.5 to -0.4', 0], ['-0.4 to -0.3', 0]]
    drilldown['neu'] = [['-0.3 to -0.2', 0], ['-0.2 to -0.1', 0], ['-0.1 to 0', 0], ['0 to 0.1', 0],
                        ['0.1 to 0.2', 0], ['0.2 to 0.3', 0]]
    drilldown['pos'] = [['0.3 to 0.4', 0], ['0.4 to 0.5', 0], ['0.5 to 0.6', 0], ['0.6 to 0.7', 0],
                        ['0.7 to 0.8', 0], ['0.8 to 0.9', 0], ['0.9 to 1', 0]]

    for sentiment in df['sentiment']:
        if (sentiment < -.9):
            drilldown['neg'][0][1] += 1
        elif (sentiment < -.8):
            drilldown['neg'][1][1] += 1
        elif (sentiment < -.7):
            drilldown['neg'][2][1] += 1
        elif (sentiment < -.6):
            drilldown['neg'][3][1] += 1
        elif (sentiment < -.5):
            drilldown['neg'][4][1] += 1
        elif (sentiment < -.4):
            drilldown['neg'][5][1] += 1
        elif (sentiment < -.3):
            drilldown['neg'][6][1] += 1
        elif (sentiment < -.2):
            drilldown['neu'][0][1] += 1
        elif (sentiment < -.1):
            drilldown['neu'][1][1] += 1
        elif (sentiment < 0):
            drilldown['neu'][2][1] += 1
        elif (sentiment < .1):
            drilldown['neu'][3][1] += 1
        elif (sentiment < .2):
            drilldown['neu'][4][1] += 1
        elif (sentiment < .3):
            drilldown['neu'][5][1] += 1
        elif (sentiment < .4):
            drilldown['pos'][0][1] += 1
        elif (sentiment < .5):
            drilldown['pos'][1][1] += 1
        elif (sentiment < .6):
            drilldown['pos'][2][1] += 1
        elif (sentiment < .7):
            drilldown['pos'][3][1] += 1
        elif (sentiment < .8):
            drilldown['pos'][4][1] += 1
        elif (sentiment < .9):
            drilldown['pos'][5][1] += 1
        else:
            drilldown['pos'][6][1] += 1

    for label, value in data:
        list_of_data.append({'name': label, 'y': value})
    print(drilldown)
    return render_template('vader.html', title=title, description_text=desc, chart_name='Pie',
                           data_list=list_of_data, drilldown=drilldown)


@app.route('/tweets', methods=['POST'])
def tweetspage():  # put application's code here

    if request.method == 'POST':
        query = request.form['query']
        tweets = api.search(query)

        return render_template('results.html', query = tweets)

    return render_template('404.html')




if __name__ == '__main__':
    app.run()
