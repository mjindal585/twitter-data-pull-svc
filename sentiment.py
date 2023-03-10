import re
import os
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
from operator import itemgetter
from dotenv import load_dotenv

load_dotenv()

class TwitterClient():
    def __init__(self):
        consumer_key = os.getenv('CONSUMER_KEY')
        consumer_secret = os.getenv('CONSUMER_SECRET')
        access_token = os.getenv('ACCESS_TOKEN')
        access_token_secret = os.getenv('ACCESS_TOKEN_SECRET') 
        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, 
                                     consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token,
                                       access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")
 
    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"
                               , " ", tweet).split())
 
    def get_tweet_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'
    
    def get_tweet_polarity(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        return analysis.sentiment.polarity
 
    def get_tweets(self, query, count=1000):
        '''
        Main function to fetch tweets and parse them.
        '''
        # empty list to store parsed tweets
        tweets = []
 
        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search(q = query, count = count)
            #print('Fetched Tweets :' , fetched_tweets)
 
            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required 
                               #params of a tweet
                parsed_tweet = {}
 
                # saving text of tweet
                parsed_tweet['text'] = tweet.text
                parsed_tweet['name'] = tweet.user.name
                parsed_tweet['screen_name'] = tweet.user.screen_name

                # saving polarity of tweet
                parsed_tweet['polarity'] =self.get_tweet_polarity(tweet.text)

                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure 
                    #that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

            # return parsed tweets
            positive_tweets = list(filter(lambda tweet: tweet['polarity'] > 0, tweets))
            negative_tweets = list(filter(lambda tweet: tweet['polarity'] < 0, tweets))
            top_five_positive = sorted(positive_tweets, key = itemgetter('polarity'), reverse = True)[:5]
            top_five_negative = sorted(negative_tweets, key = itemgetter('polarity'), reverse = True)[:5]
            return {
                "top_five_positive": top_five_positive,
                "top_five_negative": top_five_negative
            }
 
        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))
