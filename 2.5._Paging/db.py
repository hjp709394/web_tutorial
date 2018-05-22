import json


json_db = {}
with open('./2.4._Restful/db.json') as dbf:
    json_db = json.load(dbf)


def get_user(uid):
    return json_db['user']


def get_post_list(uid, page_index):
    page_size = 4
    start_index = max(0, min(page_index * page_size, len(json_db['post_list'])))
    end_index = min(start_index + page_size, len(json_db['post_list']))
    return json_db['post_list'][start_index:end_index]


def get_post_display_at_home(uid):
    return json_db['post_display_at_home']
