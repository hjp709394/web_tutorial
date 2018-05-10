import urllib.parse

class Request:
    def __init__(self, environ):
        self.environ = environ

    @property
    def args(self):
        """ 把查询参数转成字典形式 """
        get_arguments = urllib.parse.parse_qs(self.environ['QUERY_STRING'])
        return {k: v[0] for k, v in get_arguments.items()}

    @property
    def path(self):
        return self.environ['PATH_INFO']
