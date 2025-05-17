import pytz
from utillc import *
import argparse, pickle, os, sys, json
from datetime import datetime, timezone
import os, time, glob
import numpy as np      
import pandas as pd
import numpy as np, matplotlib.pyplot as plt, sys; 

import os
from utillc import *
import utillc
import cherrypy
import threading
import queue
import nmap
import subprocess
import json, pickle, re, time
from urllib.parse import urlparse
import urllib
import urllib.request
from datetime import timedelta, datetime
#from pythonping import ping
import pyezvizapi
import pytz
fileDir = os.path.dirname(os.path.abspath(__file__))
localDir = os.path.join(fileDir, '.')
EKOX(fileDir)

rootDir = os.path.join(localDir, "html")
EKOX(rootDir)


gitdir = os.path.join(fileDir, '..')
MYIP = os.environ["MYIP"]


apps = []
#mon tel :  e0:dc:ff:ec:d6:89 	Android-3 	192.168.1.72 	CHEVALLIER_BORDEAU 	2.4GHz 
tel_louis_ip = "192.168.1.72"
tels = ["tel_louis", "Galaxy-A51", "S20-FE-de-David-001" ]

garage_fn = "/deploy/data/garage.pickle"


class App0 :
	def __init__(self) :
		EKOT("app init")
		apps.append(self)

	def mount(self) :
		EKO()
		pass
	
	def info(self) :
		def read(gi) :
			i = os.environ[gi] if gi in os.environ else ""
			return gi + "=" + i
		return read('GITINFO') + ", " + read("HOST") + ", " + read("DATE")

	@cherrypy.expose
	def log(self, data=None) :
		#EKO()
		p = urlparse(data);
		rp = os.path.relpath(p.path, start = "/")
		print(rp)

	
class App(App0) :
	"""
	the Webserver
	"""
	def __init__(self) :
		super(App, self).__init__()				   
		EKOT("app init")
		apps.append(self)
		self.audio_list()

		self.nmScan = nmap.PortScanner()
		thread = threading.Thread(target=self.daemon, args=())
		thread.daemon = True							# Daemonize thread
		thread.start()									# Start the execution
		self.devices_connected = []
		
		self.mode = "auto"
		EKOT("app inited")
		self.ezviz_mode = None
		self.changed_mode = 0		

	def daemon(self):
		EKOT("daemon")
		version = 1
		while 1 :
			if version == 0 :
				EKOT("checking tels")
				batcmd="nmap -sL 192.168.1.*"
				result = subprocess.check_output(batcmd, shell=True, text=True)
				result = result.split("\n")
				#EKOX(result)
				self.devices_connected.clear()
				for e in result :
					#EKO()
					for ee in tels :
						if ee in e :
							ip = re.search("\((.*)\)", e).groups()[0]
							try :
								pp = subprocess.run("ping -c 1 %s" % ip, shell=True, text=True, check=True, timeout=15, capture_output=True).stdout
								pp = pp.split("\n")
								self.devices_connected.append(ee)
								ipok = 1;
								#EKON(ipok, ip)
							except subprocess.CalledProcessError as ex:
								# exception if ping fails ( donc device absent)
								EKOX(ex);
								pass
			else :
				#EKO()                    
				self.devices_connected.clear()                    
				tels = [ ("louis", tel_louis_ip) ]
				for ee, ip in tels :
					try :
						pp = subprocess.run("ping -c 1 -W 1 %s" % ip, shell=True, text=True, check=True, timeout=15, capture_output=True).stdout
						pp = pp.split("\n")
						self.devices_connected.append(ee)
						ipok = 1;
						#EKON(ipok, ip)
					except subprocess.CalledProcessError as ex:
						# exception if ping fails ( donc device absent)
						EKOX(ex);
						pass
			mode = "HOME_MODE" if len(self.devices_connected) > 0 else "AWAY_MODE"
			#EKOX(mode)
			#EKOX(len(self.devices_connected))

			if self.mode == "auto" :
				self.alarm(mode)
				
			#EKOX(self.devices_connected)
			#time.sleep(6)
			time.sleep(10*1)
			#EKO()

	@cherrypy.expose
	def heure(self) :
		now = datetime.now()
		print(now.year, now.month, now.day, now.hour, now.minute, now.second)
		d = { "an" : now.year,
			  "mois" : now.month,
			  "jour": now.day,
			  "heure" : now.hour,
			  "minute" : now.minute,
			  "seconde" : now.second }
		sd = json.dumps(d)
		return sd
	
	def status(self, rep) :
		with open(os.path.join(rootDir, "index.html"), "r") as file :
			data = file.read()
			data = data.replace("INFO", rep)
			data = re.sub("<p>[\w\W.]*</p>", "", data)
			return data

	@cherrypy.expose
	def audio_list(self, data=None):
		EKO()
		
		def ddd(path, f, ldddds=[]) :
			d = { "id" : os.path.join(path, f), "text" : f, "node" : os.path.join(path, f) }
			if len(ldddds) > 0	:
				d["children"] = ldddds
			return d

		def tree(path):
			try :
				files = [ ddd(path, f) for f in sorted(os.listdir(path)) if os.path.isfile(os.path.join(path, f)) ]
				dirs =	[ ddd(path, f, tree(os.path.join(path, f))) for f in os.listdir(path) if os.path.isdir(os.path.join(path, f)) ]
			except :
				files, dirs = [], []
			return files + dirs
		
		r = "http://%s:9000/Audio/" % MYIP
		rr = "/var/www/html/"

		dindex = {}

		def flat(t, r) :
			for e in t :
				ee = e.copy()
				ee["artist"] = os.path.basename(e["id"])
				ee["image"] = ""				
				e["no"] = str(len(r))
				ee["name"] = e["id"].replace("/var/www/html", "")
				ee["path"] = e["id"].replace("/var/www/html", "")
				dindex[e["id"]] = str(len(r))
					
				if "children" in ee :
					flat(ee["children"], r)
					del ee["children"]
				else :
					r.append(ee)
					
			return r
		

		path = os.path.join(rr, "Audio")		
		#path = os.path.join(rr, "Audio/meditation")		
		ttt = tree(path)
		EKO()
		dd = { "id" : "0", "text" : "root", "node" : "", "children" : tree(path)}
		EKO()
		r1 = "http://192.168.1.38/"

		l = [ { "name" :  "%s_%s" % (os.path.basename(root) + "\n" + fn , i),
				"artist" : "%s_%s" % (os.path.basename(root) , i),
				"image" : "",
				"path" :  os.path.join(root, fn).replace(rr, '')	} for root, d_names,f_names in os.walk(path) for i, fn in enumerate(sorted(f_names))]
		ll = []		   
		l = flat(ttt, ll)
		d = { "status" : "ok", "list" : l, "dict" : tree(path), "index" : dindex  }
		#EKOX(dd)
		
		sd = json.dumps(d)

		with open("/tmp/tree.json", "w") as fd :
			fd.write(json.dumps(d, sort_keys=True, indent=4))
		
		return sd

	
	@cherrypy.expose
	def index(self):
		with open(os.path.join(rootDir, "index.html"), "r") as file :
			EKOT("main")
			data = file.read()
			data = data.replace("INFO", self.info())
			data = data.replace("MYIP", MYIP)


			data += "<br> Devices : " + ",".join(self.devices_connected)
			EKOX(data)
			return data

	@cherrypy.expose
	def test(self):
		EKOT(" ==================== TEST =====================")
		return 'ok'

	@cherrypy.expose
	def get_alarm_mode(self):
		rep = self.mode + ", tel =	 " + ",".join(self.get_devices()) + " - ezviz =" + self.ezviz_mode + ", changed : %d" % self.changed_mode
		EKOX(rep)
		return rep


	@cherrypy.expose
	def get_devices(self):
		EKO()
		return self.devices_connected

	@cherrypy.expose
	def set_alarm_mode(self, mode):
		EKOX(mode)
		if 1==1 :
			self.mode = mode
			d = {
				"on" : "AWAY_MODE",
				"off" : "HOME_MODE"
			}
			try :
				self.alarm(d[mode])
			except Exception as e:
				EKOX(e)
				pass
			return "ok, mode=%s" % self.mode
		else :
			return "fail"


	@cherrypy.expose
	def alarm_off(self, mdp):
		if mdp == MDP :
			return self.alarm("HOME_MODE")
		else :
			return self.status("fail")

	@cherrypy.expose
	def alarm_on(self, mdp):
		if mdp == MDP :
			return self.alarm("AWAY_MODE")
		else :
			return self.status("fail")

	
	@cherrypy.expose
	def alarm(self, onoff):
		if self.ezviz_mode != onoff :
			"""
			onoff = HOME_MODE  or AWAY_MODE
			"""
			#pyezviz -u louis.chevallier@gmail.com -p Ezviz_35 home_defence_mode --mode HOME_MODE
			#pyezviz -u louis.chevallier@gmail.com -p Ezviz_35 home_defence_mode --mode AWAY_MODE
			username, password, region = "louis.chevallier@gmail.com", "EZVIZ_35", "apiieu.ezvizlife.com"
			#EKOX(onoff)
			self.changed_mode += 1
			result = "?"
			try :
				client = pyezvizapi.EzvizClient(username, password, region)
				client.login()
				onofft = 1 if onoff == "HOME_MODE" else 0
				client.api_set_defence_mode(onofft)
				#client.api_set_camera_defence(onofft)
				client.close_session()
				now=datetime.now(pytz.timezone("Europe/Paris"))
				open("presence.csv","a").write("%s ; %d\n" %(now.isoformat(), onofft))
				EKOT("ok")
				result = "ok"
				self.ezviz_mode = onoff
			except Exception as e :
				EKOX(e)
				result = str(e)
			r = result
		else :
			already = onoff
			#EKON(already, self.ezviz_mode)
			result = "OK"
		#EKOX(r)
		return self.status(result)
		
		
	@cherrypy.expose
	def garage(self):
		""" main 
		"""
		html = "bad url"
		try :
			url = os.environ["GARAGE_URL"]
			EKOX(url)
			with urllib.request.urlopen(url) as response:
				html = response.read()
			EKO()
			with open(garage_fn, 'ab+') as fp:
				EKO()
				pickle.dump({ "date" : datetime.now()}, fp)
			EKO()
		except Exception as err:
			html = "bad url"			
			EKOT(err)
			
		"""
		with open(os.path.join(rootDir, "garage.html"), "r") as file :
			data = file.read()
			return data
		"""
		return html

def ppp(self) :
	n = datetime.now(pytz.timezone("Europe/Paris"))
	ni = n.isoformat()
	EKON(ni)
	EKON(datetime.fromisoformat(ni))

	p  = pd.read_csv("presence.csv", delimiter=";")
	l = [ (datetime.fromisoformat(row.iloc[0] + "+02:00"), row.iloc[1]) for index, row in p.iterrows()]
	dates =  [ e[0] for e in l]
	EKOX(len(dates))
	dates2 =  [ v for e in l for v in [ e[0], e[0]] ]
	EKOX(len(dates))
	v  =  [ e[1] for e in l]
	v2 = [ vv for (v0,v1) in zip(v, v[1:] + [0]) for vv in [v0, v1]] 
	
	EKOX(len(v))
	EKOX(len(v2))

	plt.plot(dates2, v2); plt.show()
	EKO()
