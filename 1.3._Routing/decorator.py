from request import Request
from response import Response
import re

from exceptions import NotFoundError

def request_response_application(func):
    def application(environ, start_response):
        request = Request(environ)
        response = func(request)
        start_response(response.status, response.headers.items())
        return iter(response)
    return application

class DecoratorRouter:
    def __init__(self):
        self.routing_table = []    # 保存 url pattern 和 可调用对象

    def match(self, path):
        for (pattern, callback) in self.routing_table:
            m = re.match(pattern, path)
            if m:
                return (callback, m.groups())
        raise NotFoundError()

    def __call__(self, pattern):
        def _(func):
            self.routing_table.append((pattern, func))
        return _

routers = DecoratorRouter()
