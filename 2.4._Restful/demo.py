from flask import Flask
from flask import render_template, send_from_directory
from flask_restful import Api, Resource, reqparse
from db import get_user, get_post_list, get_post_display_at_home

app = Flask(__name__)
api = Api(app)


class UserAPI(Resource):
    def __init__(self):
        super(UserAPI, self).__init__()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('user_id', type=int, location='args', required=True)

    def get(self):
        args = self.parser.parse_args()
        return get_user(args['user_id'])


class PostListAPI(Resource):
    def __init__(self):
        super(PostListAPI, self).__init__()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('user_id', type=int, location='args', required=True)
        self.parser.add_argument('page_index', type=int, location='args', required=True)

    def get(self):
        args = self.parser.parse_args()
        return get_post_list(args['user_id'], args['page_index'])


api.add_resource(UserAPI, '/api/v1.0/user_info')
api.add_resource(PostListAPI, '/api/v1.0/post_list')


@app.route("/")
def main():
    return send_from_directory('templates', 'main.html')


