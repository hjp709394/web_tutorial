from wsgiref.simple_server import make_server
import argparse
from pprint import pprint

from decorator import request_response_application
from request import Request
from response import Response

from decorator import routers
from exceptions import NotFoundError

@routers(r'/say/something/(.*)$')
def say_something(request, something):
    name=request.args.get('name', 'Meng-Jiang')
    return Response(['{name} is {something}'.format(name=name, something=something)])


def application(environ, start_response):
    try:
        request = Request(environ)
        callback, args = routers.match(request.path)
        response = callback(request, *args)
    except NotFoundError:
        response = Response("<h1>Not found</h1>", status=404)
    start_response(response.status, response.headers.items())
    return iter(response)


def parse_arguments():
    parser = argparse.ArgumentParser(description='Simple SWGI demo')
    parser.add_argument('--ip', type=str, required=True, help='ip address')
    parser.add_argument('--port', type=int, required=True, help='port')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_arguments()
    ip = args.ip
    port = args.port

    httpd = make_server(ip, port, application)
    httpd.serve_forever()
