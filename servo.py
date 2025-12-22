
# https://ssojet.com/websocket/create-a-websocket-server-in-cherrypy/
# https://github.com/Lawouach/WebSocket-for-Python/blob/master/example/basic/app.py

import os
from utillc import *
import utillc
import app
import cherrypy

EKOX(dir(cherrypy))

import threading
import queue
import nmap
import subprocess
import json, pickle
from datetime import datetime

servoDir = os.path.join(app.localDir, "servo")

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

class ChatWebSocketHandler(WebSocket):
	def received_message(self, m):
		EKOX(m)
		cherrypy.engine.publish('websocket-broadcast', m)

	def closed(self, code, reason="A client left the room without a proper explanation."):
		EKOX(reason)
		cherrypy.engine.publish('websocket-broadcast', TextMessage(reason))



config_Servo = {
		'/' : {
				'tools.staticdir.on': True,
				'tools.staticdir.dir': os.path.join(app.fileDir, 'servo'),
				'tools.response_headers.on': True,
				'tools.response_headers.headers': [
						('X-Frame-options', 'deny'),
						('X-XSS-Protection', '1; mode=block'),
						('X-Content-Type-Options', 'nosniff')
				]
		},
		
#		'/ws': {
#				'tools.websocket.on': True,
#				'tools.websocket.handler_cls': ChatWebSocketHandler
#		},
		
}

#config_Servo['/ws'] =	{		'tools.websocket.on': True,		'tools.websocket.handler': ChatSocket	}



class AppServo(app.App0) :
	def __init__(self) :
		self.pos = {}
		super(AppServo, self).__init__()		
		EKOT("app servo init")

		self.connected_servos = []
		
	@cherrypy.expose
	def ws(self):
		EKO()
		cherrypy.log("Handler created: %s" % repr(cherrypy.request.ws_handler))

	@cherrypy.expose
	def test(self):
		EKOT(" ==================== TEST Servo =====================")
		return 'ok'
			
	@cherrypy.expose
	def register_me(self, me):
		now = datetime.now()
		EKOX(me)
		EKOX(cherrypy.serving.request)#.rfile.rfile._sock)		
		EKOX(cherrypy.request.remote.ip)
		return json.dumps({
			"remote_ip" : cherrypy.request.remote.ip
		})
	
	@cherrypy.expose
	def unregister_me(self, me):
		now = datetime.now()
		EKOX(me)
		
	@cherrypy.expose
	def get_connected_servos(self):
		now = datetime.now()
		current_time = now.strftime("%H:%M:%S")
		self.s = {
			"robots" : self.connected_servos
		}
		sd = json.dumps(self.pos)
		EKOX(sd)
		return sd

	@cherrypy.expose
	def refresh(self) :
		EKO()
		sd = json.dumps(self.pos)
		return sd
		
	@cherrypy.expose
	def index(self):
		EKO()
		with open(os.path.join(servoDir, "index.html"), "r") as file :
			EKOT("main")
			data = file.read()
			data = data.replace("INFO", self.info())
			data = data.replace("MYIP", app.MYIP)
			#EKOX(data)			   
			return data

	def mount(self) :
		EKO()

		WebSocketPlugin(cherrypy.engine).subscribe()
		cherrypy.tools.websocket = WebSocketTool()
		
		cherrypy.tree.mount(self, '/servo', config_Servo)		 
