#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://usefulangle.com/post/352/javascript-capture-image-from-camera

import os, gc, sys, glob, re
import os, json, base64
import shutil
import re
from utillc import *
import utillc
import cherrypy
import threading
import queue
import json, pickle
import time
import time as _time
from time import gmtime, strftime
from datetime import timedelta
import datetime 
import PIL
from PIL import Image
import os
from urllib.parse import urlparse
import urllib
import urllib.request

import socket
import fcntl
import struct

import subprocess
import pyezviz
import cherrypy
import time
import nmap
import app

utillc.default_opt["with_date"] = 1

ezvizDir = os.path.join(app.localDir, "ezviz")
linkyDir = os.path.join(app.localDir, "linky")
chaudiereDir = os.path.join(app.localDir, "chaudiere")
port = 8092
if "PORT" in os.environ :
	port = int(os.environ["PORT"])

MDP = os.environ["MDP"]


#EKOX(os.environ)
import gps
import servo
			
config_running = {
	'/' : {
		'tools.staticdir.on': True,
		'tools.staticdir.dir': os.path.join(app.fileDir, 'running'),
	}
}

config_ezviz = {
	'/' : {
		'tools.staticdir.on': True,
		'tools.staticdir.dir': os.path.join(app.fileDir, 'ezviz'),
	}
}

config_linky = {
	'/' : {
		'tools.staticdir.on': True,
		'tools.staticdir.dir': os.path.join(app.fileDir, 'linky'),
	}
}

config_chaudiere = {
	'/' : {
		'tools.staticdir.on': True,
		'tools.staticdir.dir': os.path.join(app.fileDir, 'chaudiere'),
	}
}


config = {
	'/' : {
		'tools.staticdir.on': True,
		'tools.staticdir.dir': app.rootDir,

				'tools.response_headers.on': True,
				'tools.response_headers.headers': [
						('X-Frame-options', 'deny'),
						('X-XSS-Protection', '1; mode=block'),
						('X-Content-Type-Options', 'nosniff')]


			
	},
	'global' : {
			
#		'server.ssl_module' : 'builtin',
#		'server.ssl_certificate' : "cert.pem",
#		'server.ssl_private_key' : "privkey.pem",
		
		'server.socket_host' : '0.0.0.0', #192.168.1.5', #'127.0.0.1',
		'server.socket_port' : port,
		'server.thread_pool' : 8,
		'log.screen': False,
		'log.error_file': './error.log',
		'log.access_file': './access.log',
		'tools.response_headers.on': True,
		'tools.response_headers.headers': [
				('X-Frame-options', 'deny'),
				('X-XSS-Protection', '1; mode=block'),
				('X-Content-Type-Options', 'nosniff')]
	},
}



root = "/mnt/NUC/data"

class AppRunning(app.App0) :
	def __init__(self) :
		super(AppRunning, self).__init__()
		EKOT("app init")
		self.running_data = {}
		try :
			with open(os.path.join(root, "running_data.pickle"), "rb") as fd :
				self.running_data = pickle.load(fd)
			EKOX(self.running_data.keys())
		except :
			pass

	@cherrypy.expose
	def test(self):
		EKOT(" ==================== TEST =====================")
		return 'ok'
		
		
	@cherrypy.expose
	def save(self, runner=None, data=None) :
		EKOX(runner)
		data = json.loads(data)
		self.running_data[runner] = data 
		with open(os.path.join(root, "running_data.pickle"), "wb") as fd :
			pickle.dump(self.running_data, fd, protocol=pickle.HIGHEST_PROTOCOL)
	   
		return "OK"

	@cherrypy.expose
	def load(self, runner=None) :
		EKOX(runner)
		sd = json.dumps(self.running_data[runner])
		return sd

	def mount(self) :
		cherrypy.tree.mount(self, '/running', config_running)
		
	

class AppEZviz(app.App0) :
	def __init__(self, app0) :
		super(AppEZviz, self).__init__()		
		EKOT("app ezviz init")
		self.app0 = app0

	@cherrypy.expose
	def test(self):
		EKOT(" ==================== TEST =====================")
		return 'ok'

	def mount(self) :
		EKO()
		cherrypy.tree.mount(self, '/ezviz', config_ezviz)
			
	@cherrypy.expose
	def index(self):
		EKO()
		with open(os.path.join(ezvizDir, "index.html"), "r") as file :
			EKOT("main")
			data = file.read()
			data = data.replace("INFO", self.info())
			data = data.replace("MYIP", app.MYIP)
			data += "<br> Devices : " + ",".join(self.app0.devices_connected)

			#EKOX(data)			   
			return data

class AppLinky(app.App0) :
	url = "http://192.168.1.55/data_linky"
	T = 1 # second
	K = 3000
	S = 3600*24*7
	MAX_LEN = S # sliding over 1 week
	def __init__(self) :
		super(AppLinky, self).__init__()		
		EKOT("app linky init")
		self.d = {
			"values" : [],
			"interval_sec" : self.T,
			"date" : str(datetime.datetime.now()) # date of first record
		}
		
		thread = threading.Thread(target=self.daemon_linky, args=())
		thread.daemon = True							# Daemonize thread
		thread.start()									# Start the execution


	def daemon_linky(self):
		EKOT("daemon")
		while 1 :
			#EKOX(self.url)
			# called every T seconds
			inst,pp = 0, 0
			#EKO()
			try :
				with urllib.request.urlopen(self.url) as p :
					data = json.load(p)
					#print(data["Iinst"])
					inst,pp = int(float(data["Iinst"]))*100, int(float(data["papp"]))
					#EKON(inst, pp)
			except Exception as e  :
				EKOX(e)
				pass
			self.d["values"].append( (inst,pp))
			#EKOX(json.dumps(self.d))
			# discard old records
			#EKOX(len(self.d["values"]))
			#EKOX( self.MAX_LEN)
			if (len(self.d["values"]) > self.MAX_LEN) :
				self.d["values"].pop(0)
				self.d["date"] = self.d["date"] - timedelta(seconds=self.T)
			time.sleep(self.T)

			#EKO()

	@cherrypy.expose
	def data(self):
		now = datetime.datetime.now()
		self.d["now"] = str(datetime.datetime.now())
		sd = json.dumps(self.d)
		return sd
			
	@cherrypy.expose
	def test(self):
		EKOT(" ==================== TEST =====================")
		return 'ok'

	def mount(self) :
		EKO()
		cherrypy.tree.mount(self, '/linky', config_linky)
			
	@cherrypy.expose
	def index(self):
		EKO()
		with open(os.path.join(linkyDir, "index.html"), "r") as file :
			EKOT("main")
			data = file.read()
			data = data.replace("INFO", self.info())
			data = data.replace("MYIP", app.MYIP)
			#EKOX(data)			   
			return data

class AppChaudiere(app.App0) :
	url = "http://192.168.1.55/data_linky"
	T = 1 # second
	K = 3000
	S = 3600*24*7
	MAX_LEN = S # sliding over 1 week
	def __init__(self) :
		super(AppChaudiere, self).__init__()		
		EKOT("app chaudiere init")
		self.d = {
			"values" : [],
			"interval_sec" : self.T,
			"date" : str(datetime.datetime.now()) # date of first record
		}
		
		thread = threading.Thread(target=self.daemon_chaudiere, args=())
		thread.daemon = True							# Daemonize thread
		thread.start()									# Start the execution


	def daemon_chaudiere(self):
		EKOT("daemon")
		while 1 :
			#EKOX(self.url)
			# called every T seconds
			inst,pp = 0, 0
			#EKO()

			#EKO()

	@cherrypy.expose
	def get_data(self):
		get = sd = json.dumps(self.d)
		EKOX(get)
		return sd

	@cherrypy.expose
	def set_data(self, data):
		sset = self.d = json.loads(data)
		EKOX(sset)
		return 'ok'

			
	@cherrypy.expose
	def test(self):
		EKOT(" ==================== TEST =====================")
		return 'ok'

	def mount(self) :
		EKO()
		cherrypy.tree.mount(self, '/chaudiere', config_chaudiere)
			
	@cherrypy.expose
	def index(self):
		EKO()
		with open(os.path.join(chaudiereDir, "index.html"), "r") as file :
			EKOT("main")
			data = file.read()
			data = data.replace("INFO", self.info())
			data = data.replace("MYIP", app.MYIP)
			#EKOX(data)			   
			return data

	
	
config2 = {
	"dry" : (False, " true : will not run the reconstructor"),
	"gitinfo" : "info"
}

def go() :
	app0 = app.App()
	cherrypy.log.error_log.propagate = False
	cherrypy.log.access_log.propagate = False
	EKOT("server running")

	hostname = socket.gethostname()
	IPAddr = socket.gethostbyname(hostname)

	batcmd="dir"
	result = subprocess.check_output("hostname -I", shell=True, text=True)
	EKOX(result)
	ip = list(map(str, str(result.strip()).split()))[0]
	EKOX(hostname)
	EKOX(ip)
	EKOX(app.MYIP)
	EKOX("https://%s:%d" % ( ip, port))

	apprunning, appezviz = AppRunning(), AppEZviz(app0)
	appLinky = AppLinky()
	appChaudiere = AppChaudiere()
	appGPS = gps.AppGPS()
	appServo = servo.AppServo()

	EKOX(len(app.apps))
	for e in app.apps :
		EKOX(e)
		e.mount()
	
	
	#cherrypy.tree.mount(app, '/', config)

	cherrypy.config.update({
		'server.thread_pool': 100
	})

	cherrypy.tree.mount(apprunning, '/running', config_running)	 
	
	EKOT("quickstart ..")
	#cherrypy.engine.start()
	EKO()
	#cherrypy.engine.block()
	cherrypy.quickstart(app0, '/', config)	  
	EKOT("end server", n=LOG)
