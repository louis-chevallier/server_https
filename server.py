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
port = 8092
if "PORT" in os.environ :
    port = int(os.environ["PORT"])

MDP = os.environ["MDP"]



#EKOX(os.environ)




import gps



            
config_running = {
    '/' : {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': os.path.join(app.fileDir, '..', 'running'),
    }
}

config_ezviz = {
    '/' : {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': os.path.join(app.fileDir, 'ezviz'),
    }
}


config = {
    '/' : {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': app.rootDir,
        
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



root = "/mnt/NUC/data"

class App1(app.App0) :
    def __init__(self) :
        super(App1, self).__init__()
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
    def __init__(self) :
        super(AppEZviz, self).__init__()        
        EKOT("app ezviz init")

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
    ip = list(map(str, str(result.strip()).split()))[0]
    EKOX(hostname)
    EKOX(ip)
    EKOX(app.MYIP)
    EKOX("https://%s:%d" % ( ip, port))

    app1, appezviz = App1(), AppEZviz()
    appGPS = gps.AppGPS()


    EKOX(len(app.apps))
    for e in app.apps :
        EKOX(e)
        e.mount()
    
    
    #cherrypy.tree.mount(app, '/', config)

    cherrypy.config.update({
        'server.thread_pool': 100
    })

    cherrypy.tree.mount(app1, '/running', config_running)    
    
    EKOT("quickstart ..")
    #cherrypy.engine.start()
    EKO()
    #cherrypy.engine.block()
    cherrypy.quickstart(app0, '/', config)    
    EKOT("end server", n=LOG)
