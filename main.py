from dotenv import load_dotenv
from pytwitter import Api

import os
from datetime import datetime, timedelta

load_dotenv()
api = Api(bearer_token=os.getenv('BEARER_TOKEN'))

def users_lookup(user_names):
    res = api.get_users(usernames=user_names)
    return res.data

def timeline_lookup(user_id, from_, days):
    res = api.get_timelines(user_id=user_id, 
                          start_time=(from_-timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%SZ"), 
                          end_time=from_.strftime("%Y-%m-%dT%H:%M:%SZ"),
                          max_results=100)
    return res.data

def tweet_lookup(tweet_id):
    res = api.get_tweet(tweet_id)
    return res.data

if __name__=='__main__':
    user_names = 'TheMoonCarl'
    users_res = users_lookup(user_names)
    for user in users_res:
        tweets_res = timeline_lookup(user.id, from_=datetime.now(), days=10)
    for tweet in tweets_res:
        tweet_res = tweet_lookup(tweet.id)
        print(tweet_res.text)


