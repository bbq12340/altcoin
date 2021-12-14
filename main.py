import requests
from dotenv import load_dotenv

import os, json
from datetime import datetime, timedelta

import requests

load_dotenv()

API_URL = 'https://api.twitter.com/2'

__header__ = {
        "Authorization": f"Bearer {os.getenv('BEARER_TOKEN')}"
    }

def user_id_lookup(username):
    url = f'{API_URL}/users/by/username/{username}'
    res = requests.get(url, headers=__header__).json()
    return res['data']['id']

def timeline_lookup(id, **kwargs):
    url = f'{API_URL}/users/{id}/tweets'
    payload = {
        'max_results': 100,
        'tweet.fields': 'author_id,attachments,created_at,public_metrics,conversation_id'
    }
    if kwargs:
        payload.update(kwargs)
    res = requests.get(url, params=payload, headers=__header__).json()
    return res

if __name__=='__main__':
    today = datetime.now()
    last_week = (today-timedelta(days=7))
    id = user_id_lookup('TheMoonCarl')
    data = []
    tweets_data = timeline_lookup(id, start_time=last_week.strftime("%Y-%m-%dT%H:%M:%SZ"), end_time=today.strftime("%Y-%m-%dT%H:%M:%SZ"))
    while True:
        try:
            data.extend(tweets_data['data'])
            next_token = tweets_data['meta']['next_token']
            tweets_data = timeline_lookup(id, start_time=last_week.strftime("%Y-%m-%dT%H:%M:%SZ"), end_time=today.strftime("%Y-%m-%dT%H:%M:%SZ"), pagination_token=next_token)
        except KeyError:
            print(tweets_data)
            break
    with open('sample/data.json', 'w') as f:
        json.dump(data, f, indent=4, sort_keys=True, ensure_ascii=False)