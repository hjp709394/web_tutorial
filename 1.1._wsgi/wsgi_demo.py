from wsgiref.simple_server import make_server
import argparse
from pprint import pprint

def application(environ, start_response):
    ### uncommend the following code if you want to check what is inside environ and start_response
    # print('environ: \n')
    # pprint(environ)                   # environ is a dict that contains most of the information 
                                        # you need to decide how to response a request
    # print('\nstart_response: \n')
    # print(start_response)
    # print('\n\n')

    status = '200 OK'                   # Status code ref: https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html
    headers = [('Content-Type', 'text/html; charset=utf8')]
    start_response(status, headers)
    return [b"Meng Jiang is smart"]     # WSGI requires to return iterable bytes literal


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

    print("Starting a server with address {}:{}. Send C-c to stop the server.".format(ip, port))
    httpd = make_server(ip, port, application)
    httpd.serve_forever()
