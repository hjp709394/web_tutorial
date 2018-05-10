from wsgiref.simple_server import make_server
import argparse
from pprint import pprint

from decorator import request_response_application
from request import Request
from response import Response


@request_response_application
def application(request):
    name = request.args.get('name', 'MengJiang')
    return Response(['{name} is diligent'.format(name=name)])


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
