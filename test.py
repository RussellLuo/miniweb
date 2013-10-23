#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""test.py"""

from miniweb import application

urls = (
    ("/", "index"),
    ("/hello/(.*)", "hello"),
)

app = application(urls, globals())

class index:
    def GET(self):
        return "Welcome!"

class hello:
    def GET(self, name):
        if not name: name = 'world'
        return "Hello %s!" % name

if __name__ == '__main__':
    app.run()
