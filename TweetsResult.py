from jinja2 import Undefined
import json


class TweetsResult:
    def __init__(self, date, format):
        self.date = date
        self.tweets = []
        self.scoreAverage = []
        self.numberOfTweets = 0
        self.format = {
            'labels' : format,
            'counts' : [0] * len(format)
        }
    
    def setTweetType(self, tweet):

        match = 0
        type = self.format['labels'][0]

        for i in range(len(self.format['labels'])):

            if tweet['score'][i]['score'] > tweet['score'][match]['score']:
                type = self.format['labels'][i]
                match = i

        self.format['counts'][match] += 1

        return type

    def addTweetResult(self, tweet):

        if (len(self.tweets) == 0):
            self.scoreAverage = tweet['score']
        else:
            for i in range(len(tweet['score'])):
                self.scoreAverage[i]['score'] += tweet['score'][i]['score']

        self.numberOfTweets += 1

        tweet['type'] = self.setTweetType(tweet)

        self.tweets.append(tweet)

    
    def calculateAverage(self):

        for i in range(len(self.scoreAverage)):
            self.scoreAverage[i]['score'] = self.scoreAverage[i]['score'] / self.numberOfTweets

    def toJSON(self):
        return json.dumps(self.__dict__)