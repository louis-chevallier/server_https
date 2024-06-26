# -*- coding: utf-8 -*-
__doc__ = """
A simple chat example using a CherryPy webserver.

$ pip install cherrypy

Then run it as follow:

$ python app.py

You will want to edit this file to change the
ws_addr variable used by the websocket object to connect
to your endpoint. Probably using the actual IP
address of your machine.
"""
import random
import os
from utillc import *

import cherrypy
#https://github.com/Lawouach/WebSocket-for-Python/blob/master/example/echo_cherrypy_server.py

from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
from ws4py.websocket import WebSocket
from ws4py.messaging import TextMessage
import socket

ip = socket.gethostbyname(socket.gethostname())
ip = socket.gethostbyname(socket.getfqdn()) 
EKOX(ip)
EKOX(socket.gethostbyname_ex(socket.gethostname())[-1])

import socket
ip = [(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]
EKOX(ip)


cur_dir = os.path.normpath(os.path.abspath(os.path.dirname(__file__)))
index_path = os.path.join(cur_dir, 'index_websocket.html')
index_page = open(index_path, 'r').read()

class ChatWebSocketHandler(WebSocket):
    def received_message(self, m):
        EKOX(m)
        cherrypy.engine.publish('websocket-broadcast', m)

    def closed(self, code, reason="A client left the room without a proper explanation."):
        EKOX(reason)
        cherrypy.engine.publish('websocket-broadcast', TextMessage(reason))

class ChatWebApp(object):
    @cherrypy.expose
    def index(self):
        user = random.randint(50, 1000)
        EKOX(user)
        return index_page % {'username': "User%d" % user,
                             'ws_addr': 'ws://%s:9000/ws' % ip}

    @cherrypy.expose
    def ws(self):
        EKO()
        cherrypy.log("Handler created: %s" % repr(cherrypy.request.ws_handler))

if __name__ == '__main__':
    cherrypy.config.update({
        'server.socket_host': '0.0.0.0',
        'server.socket_port': 9000
    })
    
    WebSocketPlugin(cherrypy.engine).subscribe()
    cherrypy.tools.websocket = WebSocketTool()

    cherrypy.quickstart(ChatWebApp(), '',
                        config={
                            '/': {
                                'tools.response_headers.on': True,
                                'tools.response_headers.headers': [
                                    ('X-Frame-options', 'deny'),
                                    ('X-XSS-Protection', '1; mode=block'),
                                    ('X-Content-Type-Options', 'nosniff')
                                ]
                            },
                            '/ws': {
                                'tools.websocket.on': True,
                                'tools.websocket.handler_cls': ChatWebSocketHandler
                            },
                        })
