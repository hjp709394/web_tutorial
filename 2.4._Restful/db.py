import json

json_db = {}
with open('./2.4._Restful/db.json') as dbf:
    json_db = json.load(dbf)

def get_user(uid=0):
    return json_db['user']

def get_post_list(uid=0):
    return json_db['post']

def get_post_display_at_home(uid=0):
    post = []
    for p in json_db['post']:
        if p['display_at_home']:
            post.append(p)
    return post
