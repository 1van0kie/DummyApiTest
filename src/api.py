import requests

from src.utils import *

BASEURL = 'https://dummyapi.io/data/v1'


def get_users(api_key='6647625fc4ca1909b00e8b2c', pagination=None):
    params = {}
    if pagination:
        params['page'] = pagination.page
        params['limit'] = pagination.limit
    resp = requests.get(f'{BASEURL}/user', headers={'app-id': api_key}, params=params)
    return resp


def get_user(id, api_key='6647625fc4ca1909b00e8b2c'):
    resp = requests.get(f'{BASEURL}/user/{id}', headers={'app-id': api_key})
    return resp


def create_user(firstname, lastname, api_key='6647625fc4ca1909b00e8b2c'):
    resp = requests.post(f'{BASEURL}/user/create', headers={'app-id': api_key},
                         json={'firstName': firstname, 'lastName': lastname, 'email': random_email()})
    return resp


def get_user_id(response):
    id = response.json()['id']
    return id


def update_user(user_id, gender, firstname, lastname, api_key='6647625fc4ca1909b00e8b2c'):
    resp = requests.put(f'{BASEURL}/user/{user_id}', headers={'app-id': api_key},
                        json={'gender': gender, 'firstName': firstname, 'lastName': lastname})
    return resp


def create_post(user_id, json_data, api_key='6647625fc4ca1909b00e8b2c'):
    resp = requests.post(f'{BASEURL}/post/create', headers={'app-id': api_key},
                         json={'text': json_data['text'], 'likes': json_data['likes'], 'tags': ["dada", "netnet"],
                               'owner': user_id})
    return resp
