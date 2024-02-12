#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://usefulangle.com/post/352/javascript-capture-image-from-camera

import os, gc, sys, glob
import os, json, base64
import shutil
import re
from utillc import *
import cherrypy
import threading
import queue
import json, pickle
import time
import time as _time
from time import gmtime, strftime
from datetime import timedelta
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
    
fileDir = os.path.dirname(os.path.abspath(__file__))
localDir = os.path.join(fileDir, '.')

rootDir = os.path.join(localDir, "html")
EKOX(rootDir)

port = 8082
if "PORT" in os.environ :
    port = int(os.environ["PORT"])

config = {
  '/' : {
      'tools.staticdir.on': True,
      'tools.staticdir.dir': rootDir,
#      'tools.staticdir.dir': '/mnt/hd2/users/louis/dev/git/three.js/examples/test',

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

    def info(self) :
        def read(gi) :
            i = os.environ[gi] if gi in os.environ else ""
            return gi + "=" + i
        return read('GITINFO') + ", " + read("HOST") + ", " + read("DATE")
        
    @cherrypy.expose
    def index(self):
        with open(os.path.join(rootDir, "index.html"), "r") as file :
            EKOT("main")
            data = file.read()
            data = data.replace("INFO", self.info())
            EKOX(data)
            return data
        
    @cherrypy.expose
    def alarm_off(self):   self.alarm("HOME_MODE")

    @cherrypy.expose
    def alarm_on(self):   self.alarm("AWAY_MODE")

    
    @cherrypy.expose
    def alarm(self, onoff):
        """
        onoff = HOME_MODE  or AWAY_MODE
        """
        #pyezviz -u louis.chevallier@gmail.com -p Ezviz_35 home_defence_mode --mode HOME_MODE
        #pyezviz -u louis.chevallier@gmail.com -p Ezviz_35 home_defence_mode --mode AWAY_MODE
        username, password, region = "louis.chevallier@gmail.com", "Ezviz_35", "apiieu.ezvizlife.com"
        EKOX(onoff)
        result = "?"
        try :
            client = pyezviz.EzvizClient(username, password, region)
            EKO()
            client.login()
            EKO()
            onofft = 1 if onoff == "HOME_MODE" else 0
            client.api_set_defence_mode(onofft)
            EKO()            
            client.close_session()
            EKO()            
            result = "ok"
        except Exception as e :
            EKOX(e)
            result = str(e)
        r = result
        EKOX(r)
        return r
        
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
        EKOT("REQ main")
        url = os.environ["GARAGE_URL"]
        EKOX(url)
        with urllib.request.urlopen(url) as response:
            html = response.read()
        return html
        
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
    EKOX("https://%s:%d" % ( ip, port))
    cherrypy.quickstart(app, '/', config)
    EKOT("end server", n=LOG)
