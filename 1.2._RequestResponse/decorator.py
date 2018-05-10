from request import Request
from response import Response

def request_response_application(func):
    def application(environ, start_response):
        request = Request(environ)
        response = func(request)
        start_response(response.status, response.headers.items())
        return iter(response)
    return application
