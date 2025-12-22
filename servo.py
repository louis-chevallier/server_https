import os
from utillc import *
import utillc
import app
import cherrypy
import threading
import queue
import nmap
import subprocess
import json, pickle
from datetime import datetime

servoDir = os.path.join(app.localDir, "servo")

config_Servo = {
	'/' : {
		'tools.staticdir.on': True,
		'tools.staticdir.dir': os.path.join(app.fileDir, 'servo'),
	}
}

class AppServo(app.App0) :
	def __init__(self) :
		self.pos = {}
		super(AppServo, self).__init__()		
		EKOT("app servo init")

		self.connected_servos = []
		

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
		cherrypy.tree.mount(self, '/servo', config_Servo)		 
		
