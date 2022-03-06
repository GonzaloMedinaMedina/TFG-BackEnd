from flask import Flask
from jinja2 import Undefined
import requests
import os
import json
from flask import jsonify, request
from flask_cors import CORS
import tweepy
from datetime import datetime
import calendar
import time

from TweetsResult import TweetsResult

TRIPLEFORMAT = [
    'negative',
    'neutral',
    'positive'
]

FORMATS = [
    {
      'id': 'cardiffnlp/twitter-roberta-base-sentiment',
      'format': TRIPLEFORMAT
    },
    {
      'id': 'cardiffnlp/twitter-xlm-roberta-base-sentiment',
      'format': TRIPLEFORMAT
    },
    {
      'id': 'cardiffnlp/twitter-roberta-base-emotion',
      'format': [
                'joy',
                'optimism',
                'anger',
                'sadness'
              ]
    },
    {
      'id': 'cardiffnlp/twitter-roberta-base-hate',
      'format': [
                'not-hate',
                'hate'
              ]
    },
    {
      'id': 'cardiffnlp/twitter-roberta-base-irony',
      'format': [
                'irony',
                'not-irony'
              ]
    },
    {
      'id': 'cardiffnlp/twitter-roberta-base-offensive',
      'format': [
                'not-offensive',
                'offensive'
              ]
    },
    {
      'id': 'cardiffnlp/twitter-roberta-base-emoji',
      'format': TRIPLEFORMAT
    },
    {
      'id': 'cardiffnlp/twitter-roberta-base-stance-abortion',
      'format': [
                'not-abortion-related',
                'abortion-topic-related',
                'abortion'
              ]
    },
    {
      'id': 'cardiffnlp/twitter-roberta-base-stance-atheism',
      'format': [
                'not-atheism-related',
                'atheism-topic-related',
                'atheism'
              ]
    },
    {
      'id': 'cardiffnlp/twitter-roberta-base-stance-climate',
      'format': TRIPLEFORMAT
    },
    {
      'id': 'cardiffnlp/twitter-roberta-base-stance-feminist',
      'format': TRIPLEFORMAT
    },
    {
      'id': 'cardiffnlp/twitter-roberta-base-stance-hillary',
      'format': TRIPLEFORMAT
    },
    {
      'id': 'cardiffnlp/twitter-roberta-base',
      'format': TRIPLEFORMAT
    },
    {
      'id': 'cardiffnlp/twitter-xlm-roberta-base',
      'format': TRIPLEFORMAT
    }
  ]


HUGGING_TOKEN = 'api_QDmvqWFqDPqTngiSDNRqcfUlcrVeckHbKD'
auth = tweepy.OAuthHandler('a9LhK5Pgep6Bub0CNh7jm7vGE', 'k1k5WdeTQ6rtKjMN65BLJhCDn9duZcLmlY6RngoFfy28TFGgC2')
auth.set_access_token('1459928956275249157-d38iQepcZuXCPajyJ8Y4WQ2MHzvMIH', 'APampemIrcLX6y9XBxeJTP5yz3GFd94NqGUTfoMVySBpr')

api = tweepy.API(auth)
#BEARER TOKEN AAAAAAAAAAAAAAAAAAAAAAEnVwEAAAAApQCsW4g67eBvwyAnfX0jtnlv6KE%3D2Tumhc59Wfi1JPSWVVTFIvHbdfcLaOYt7oO89TVJV5LHYVaTfx
#API KEY a9LhK5Pgep6Bub0CNh7jm7vGE
#API KEY SECRET k1k5WdeTQ6rtKjMN65BLJhCDn9duZcLmlY6RngoFfy28TFGgC2
#ACCESS TOKEN 1459928956275249157-d38iQepcZuXCPajyJ8Y4WQ2MHzvMIH
#ACCES TOKEN SECRET APampemIrcLX6y9XBxeJTP5yz3GFd94NqGUTfoMVySBpr

if __name__=="tweetevalController":
    app = Flask(__name__)
    app.run(debug=True)
    app.app_context()
    CORS(app)
    # To set your enviornment variables in your terminal run the following line:
    # export 'BEARER_TOKEN'='<your_bearer_token>'
    bearer_token = 'AAAAAAAAAAAAAAAAAAAAAAEnVwEAAAAApQCsW4g67eBvwyAnfX0jtnlv6KE%3D2Tumhc59Wfi1JPSWVVTFIvHbdfcLaOYt7oO89TVJV5LHYVaTfx'


    def getEndDayOfMonth(month, year):
        if checkIfMonthHasThirtyOneDays(month):
            return 31
        elif month == 2:
            if calendar.isleap(year):
                return 29
            else:
                return 28    
        else:
            return 30

    def checkIfMonthHasThirtyOneDays(month):
        if month in {1, 3, 5, 7, 8, 10, 12}:
            return True
        return False

    def bearer_oauth(r):
        r.headers["Authorization"] = f"Bearer {bearer_token}"
        r.headers["User-Agent"] = "v2FullArchiveSearchPython"
        return r

    def connect_to_endpoint(url, params=""):
        response = requests.request("GET", url, auth=bearer_oauth, params=params)
        print(response.status_code)
        
        if response.status_code != 200:
            raise Exception(
                "Request returned an error: {} {}".format(
                    response.status_code, response.text
                )
            )
        return response.json()

    @app.route("/SingleTweet/", methods=['GET', 'POST'])
    def getTweetById():
        with app.app_context():

            model = request.args.get('model')
            tweetId = request.args.get('tweetId')
            query_params = {
                'ids' : tweetId
            }

            if tweetId:

                url = "https://api.twitter.com/2/tweets?"
                json_response = connect_to_endpoint(url, params=query_params)       
                print(json_response)
                return getTextResult(json_response['data'][0]['text'], model)

    @app.route("/SearchTweets/", methods=['GET'])
    def getTweetsBySearchQuery():
        with app.app_context():
            content = request.args.get('twitterContent')
            dateFrom = request.args.get('dateFrom')
            dateTo = request.args.get('dateTo')
            dayFrom = dateFrom[-2:len(dateFrom)]
            dayTo = dateTo[-2:len(dateTo)]
            monthFrom = dateFrom[-5:-3]
            monthTo = dateTo[-5:-3]
            yearFrom = dateFrom[0:-6]
            yearTo = dateTo[0:-6]
            numberOfTweets = int(request.args.get('numberOfTweets'))
            language = request.args.get('language')
            country = request.args.get('country')
            model = request.args.get('model')

            currentDate = datetime.today().strftime('%Y-%m-%d')
            
            if numberOfTweets > 100 or numberOfTweets < 0:
                numberOfTweets = 15

            query = content + ' -is:retweet -is:reply -has:media -has:links lang:' + language
            now = datetime.now() 
            end_time = "23:59:00"
            current_time = now.strftime("%H:59:59")
            hour_time = int(current_time[0:2]) - 1
            current_time = current_time.replace(current_time[0:2], str(hour_time))
            start_time = now.strftime("00:00:00")
            
            if dateTo and dateFrom:
                query_params = {
                    'query': query,
                    'tweet.fields': 'author_id,created_at',
                    'user.fields' : 'name',
                    "max_results": numberOfTweets,
                    "start_time": dateFrom + "T" + start_time + "Z", 
                    "end_time": dateTo + "T" + end_time + "Z"
                    #"place.fields": "country"
                }
            
            url = 'https://api.twitter.com/2/tweets/search/recent'
            results = []

            if (model):

                for modelFormat in FORMATS:
                    if modelFormat['id'] == model:
                        currentFormat = modelFormat['format']
                        break

                if dayTo < dayFrom and monthTo > monthFrom:
                    dayEndOfMonthFrom = getEndDayOfMonth(int(monthFrom), yearFrom)
                    intDayFrom = int(dayFrom)
                    print(intDayFrom)
                    print(dayEndOfMonthFrom)
                    for i in range(intDayFrom, dayEndOfMonthFrom+1):
                        day = str(i) if i / 10 > 1 else '0' + str(i)
                        date = yearFrom + '-' + monthFrom + '-' + day

                        if currentDate == date:
                            time_to = current_time
                        else:
                            time_to = end_time

                        query_params['start_time'] = date + "T" + start_time + "Z"
                        query_params['end_time'] = date + "T" + time_to + "Z"

                        json_response = connect_to_endpoint(url, params=query_params)
                        results.append(getTweetsResults(json_response, model, date, currentFormat))
                    
                    intDayTo = int(dayTo)
                    i = 1

                    for i in range(1, intDayTo+1):
                        day = str(i) if i / 10 > 1 else '0' + str(i)
                        date = yearTo + '-' + monthTo + '-' + day

                        if currentDate == date:
                            time_to = current_time
                        else:
                            time_to = end_time 

                        query_params['start_time'] = date + "T" + start_time + "Z"
                        query_params['end_time'] = date + "T" + time_to + "Z"

                        json_response = connect_to_endpoint(url, params=query_params)
                        results.append(getTweetsResults(json_response, model, date, currentFormat))
                else:
                               
                    intDayFrom = int(dayFrom)
                    intDayTo = int(dayTo)

                    for day in range(intDayFrom, intDayTo+1):
                        date = yearFrom + '-' + monthFrom + '-' + str(day) 

                        if currentDate == date:
                            time_to = current_time
                        else:
                            time_to = end_time
                        
                        query_params['start_time'] = date + "T" + start_time + "Z"
                        query_params['end_time'] = date + "T" + time_to + "Z"

                        json_response = connect_to_endpoint(url, params=query_params)
                        results.append(getTweetsResults(json_response, model, str(date), currentFormat))
                
                return jsonify(results)

    def getTweetsResults(tweets, model, day, format):
        with app.app_context():         
            API_URL = "https://api-inference.huggingface.co/models/" + model
            headers = {"Authorization": f"Bearer {HUGGING_TOKEN}"}
            tweetResults = TweetsResult(day, format)

            for tweet in tweets['data']:
                response = requests.post(API_URL, headers=headers, json={"inputs": tweet['text']}).json()
                
                tweetResults.addTweetResult(
                    {
                        'text' : tweet['text'],
                        'score' : response[0],
                        'type' : Undefined
                    }
                )

            tweetResults.calculateAverage()

            return tweetResults.toJSON()

    @app.route("/evaluateText/", methods=['GET'])
    def evaluateText():
        with app.app_context():
            text = request.args.get('text')
            model = request.args.get('model')
            print(model)
            return getTextResult(text, model)
    
    def getTextResult(text, model):
        with app.app_context():         
            API_URL = "https://api-inference.huggingface.co/models/" + str(model)
            headers = {"Authorization": f"Bearer {HUGGING_TOKEN}"}
            
            if (model):
                for modelFormat in FORMATS:
                    if modelFormat['id'] == model:
                        currentFormat = modelFormat['format']
                        break

            response = requests.post(API_URL, headers=headers, json={"inputs": text}).json()
            
            return jsonify({'score':response, 'text':text})

#tweetevalController.py
#$env:FLASK_APP = "tweetevalController"
#$env:FLASK_ENV = "development"
#python -m flask run 