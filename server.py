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


utillc.default_opt["with_date"] = 1


fileDir = os.path.dirname(os.path.abspath(__file__))
localDir = os.path.join(fileDir, '.')

gitdir = os.path.join(fileDir, '..')

rootDir = os.path.join(localDir, "html")
EKOX(rootDir)
ezvizDir = os.path.join(localDir, "ezviz")
port = 8092
if "PORT" in os.environ :
    port = int(os.environ["PORT"])

MDP = os.environ["MDP"]

garage_fn = "/deploy/data/garage.pickle"


#EKOX(os.environ)

MYIP = os.environ["MYIP"]

tels = ["tel_louis", "Galaxy-A51", "S20-FE-de-David-001" ]

            
config_running = {
    '/' : {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': os.path.join(fileDir, '..', 'running'),
    }
}

config_ezviz = {
    '/' : {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': os.path.join(fileDir, 'ezviz'),
    }
}

config = {
    '/' : {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': rootDir,
        
    },
    'global' : {
        'server.ssl_module' : 'builtin',
        'server.ssl_certificate' : "cert.pem",
        'server.ssl_private_key' : "privkey.pem",
        
        'server.socket_host' : '0.0.0.0', #192.168.1.5', #'127.0.0.1',
        'server.socket_port' : port,
        'server.thread_pool' : 8,
        'log.screen': False,
        'log.error_file': './error.log',
        'log.access_file': './access.log'
    },
}

class App:
    """
    the Webserver
    """
    def __init__(self) :
        EKOT("app init")

        self.audio_list()

        self.nmScan = nmap.PortScanner()
        thread = threading.Thread(target=self.daemon, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution
        self.devices_connected = []

        self.mode = "auto"
        EKOT("app inited")
        
    def daemon(self):
        while 1 :
            EKOT("checking tels")
            #do_periodic_stuff()
            batcmd="nmap -sL 192.168.1.*"
            result = subprocess.check_output(batcmd, shell=True, text=True)
            result = result.split("\n")
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
                        except subprocess.CalledProcessError as ex:
                            # exception if ping fails ( donc device absent)
                            #EKOX(ex) 
                            pass
            mode = "HOME_MODE" if len(self.devices_connected) > 0 else "AWAY_MODE"
            EKOX(mode)

            if self.mode == "auto" :
                self.alarm(mode)
                
            #EKOX(self.devices_connected)
            time.sleep(60*10)
            EKO()

    def info(self) :
        def read(gi) :
            i = os.environ[gi] if gi in os.environ else ""
            return gi + "=" + i
        return read('GITINFO') + ", " + read("HOST") + ", " + read("DATE")


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
            if len(ldddds) > 0  :
                d["children"] = ldddds
            return d

        def tree(path):
            files = [ ddd(path, f)      for f in sorted(os.listdir(path)) if os.path.isfile(os.path.join(path, f)) ]
            dirs =  [ ddd(path, f, tree(os.path.join(path, f))) for f in os.listdir(path) if os.path.isdir(os.path.join(path, f)) ]
            
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
                "path" :  os.path.join(root, fn).replace(rr, '')    } for root, d_names,f_names in os.walk(path) for i, fn in enumerate(sorted(f_names))]
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


            data += "devices : " + ",".join(self.devices_connected)
            #EKOX(data)
            return data

    @cherrypy.expose
    def test(self):
        EKOT(" ==================== TEST =====================")
        return 'ok'

    @cherrypy.expose
    def get_alarm_mode(self):
        EKO()
        return self.mode
        
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
            except :
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
        """
        onoff = HOME_MODE  or AWAY_MODE
        """
        #pyezviz -u louis.chevallier@gmail.com -p Ezviz_35 home_defence_mode --mode HOME_MODE
        #pyezviz -u louis.chevallier@gmail.com -p Ezviz_35 home_defence_mode --mode AWAY_MODE
        username, password, region = "louis.chevallier@gmail.com", "Ezviz_35", "apiieu.ezvizlife.com"
        #EKOX(onoff)
        result = "?"
        try :
            client = pyezviz.EzvizClient(username, password, region)
            client.login()
            onofft = 1 if onoff == "HOME_MODE" else 0
            client.api_set_defence_mode(onofft)
            #client.api_set_camera_defence(onofft)
            client.close_session()
            result = "ok"
        except Exception as e :
            #EKOX(e)
            result = str(e)
        r = result
        #EKOX(r)
        return self.status(r)
        
    @cherrypy.expose
    def log(self, data=None) :
        #EKO()
        p = urlparse(data);
        rp = os.path.relpath(p.path, start = "/")
        print(rp)
        
    @cherrypy.expose
    def garage(self):
        """ main 
        """
        html = "bad url"
        try :
            url = os.environ["GARAGE_URL"]
            EKOX(url)
            with urllib.request.urlopen(url) as response:  html = response.read()
            with open(garage_fn, 'ab+') as fp:
                EKO()
                pickle.dump({ "date" : datetime.datetime.now()}, fp)
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

root = "/mnt/NUC/data"

class App1(App) :
    def __init__(self) :
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

class AppEZviz(App) :
    def __init__(self) :
        EKOT("app ezviz init")

    @cherrypy.expose
    def test(self):
        EKOT(" ==================== TEST =====================")
        return 'ok'
        
            
    @cherrypy.expose
    def index(self):
        EKO()
        with open(os.path.join(ezvizDir, "index.html"), "r") as file :
            EKOT("main")
            data = file.read()
            data = data.replace("INFO", self.info())
            data = data.replace("MYIP", MYIP)
            EKOX(data)            
            return data
    
    
config2 = {
    "dry" : (False, " true : will not run the reconstructor"),
    "gitinfo" : "info"
}

def go() :
    app = App()
    cherrypy.log.error_log.propagate = False
    cherrypy.log.access_log.propagate = False
    EKOT("server running")

    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)


    batcmd="dir"
    result = subprocess.check_output("hostname -I", shell=True, text=True)
    ip = list(map(str, str(result.strip()).split()))[0]
    EKOX(hostname)
    EKOX(ip)
    EKOX(MYIP)
    EKOX("https://%s:%d" % ( ip, port))

    app1, appezviz = App1(), AppEZviz()
    cherrypy.tree.mount(app1, '/running', config_running)
    cherrypy.tree.mount(appezviz, '/ezviz', config_ezviz)
    #cherrypy.tree.mount(app, '/', config)

    cherrypy.config.update({
        'server.thread_pool': 100
    })

    cherrypy.tree.mount(app1, '/running', config_running)    
    
    EKOT("quickstart ..")
    #cherrypy.engine.start()
    EKO()
    #cherrypy.engine.block()
    cherrypy.quickstart(app, '/', config)    
    EKOT("end server", n=LOG)
