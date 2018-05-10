import http.client
from wsgiref.headers import Headers


class Response:
    def __init__(self, response=None, status=200, charset='utf-8', content_type='text/html'):
        self.response = [] if response is None else response
        self.charset = charset
        self.headers = Headers()
        content_type = '{content_type}; charset={charset}'.format(content_type=content_type, charset=charset)
        self.headers.add_header('content-type', content_type)
        self._status = status

    @property
    def status(self):
        status_string = http.client.responses.get(self._status, 'UNKNOWN')
        return '{status} {status_string}'.format(status=self._status, status_string=status_string)

    def __iter__(self):
        for val in self.response:
            if isinstance(val, bytes):
                yield val
            else:
                yield val.encode(self.charset)
