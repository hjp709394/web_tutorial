from flask import Flask
from flask import render_template, send_from_directory
from flask_restful import Api, Resource
from db import get_user, get_post_list, get_post_display_at_home

app = Flask(__name__)
api = Api(app)


class UserAPI(Resource):
    def get(self, user_id):
        return get_user(user_id)


class PostListAPI(Resource):
    def get(self, user_id, page_index):
        return get_post_list(user_id, page_index)


api.add_resource(UserAPI, '/api/v1.0/user_info/<int:user_id>')
api.add_resource(PostListAPI, '/api/v1.0/post_list/<int:user_id>/<int:page_index>')


@app.route("/")
def main():
    return send_from_directory('templates', 'main.html')


