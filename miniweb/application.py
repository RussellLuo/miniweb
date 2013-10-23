#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Web application"""

import re

__all__ = [
    'application',
]

class application:
    """
    Application to delegate requests based on path.
    
        >>> urls = ("/", "index")
        >>> app = application(urls, globals())
        >>> class index:
        ...     def GET(self): return "welcome"
    """

    headers = []

    def __init__(self, urls=(), fvars={}):
        self._urls = urls
        self._fvars = fvars

    def __call__(self, environ, start_response):
        self._status = '200 OK' # default status is OK
        del self.headers[:] # clear headers for previous request

        result = self._delegate(environ)
        start_response(self._status, self.headers)

        # translate `result` to be iterable
        if isinstance(result, basestring):
            return iter([result])
        else:
            return iter(result)

    def _delegate(self, environ):
        path = environ['PATH_INFO']
        method = environ['REQUEST_METHOD']

        for pattern, name in self._urls:
            m = re.match('^' + pattern + '$', path)
            if m:
                # pass the matched groups as arguments to the function
                args = m.groups()
                funcname = method.upper() # allow uppercase methods only (e.g. GET or POST)
                cls = self._fvars.get(name) # find class object by name
                if hasattr(cls, funcname):
                    func = getattr(cls(), funcname)
                    return func(*args)

        return self._notfound()

    def _notfound(self):
        self._status = '404 Not Found'
        self.header('Content-type', 'text/plain')
        return "Not Found\n"

    @classmethod
    def header(cls, name, value):
        cls.headers.append((name, value))

    def run(self, host='', port=8086):
        from wsgiref.simple_server import make_server
        httpd = make_server(host, port, self)
    
        sa = httpd.socket.getsockname()
        print 'http://{0}:{1}/'.format(*sa)
    
        # Respond to requests until process is killed
        httpd.serve_forever()
