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
gpsDir = os.path.join(app.localDir, "gps")

config_GPS = {
    '/' : {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': os.path.join(app.fileDir, 'gps'),
        'tools.response_headers.on': True,
        'tools.response_headers.headers': [ ('Access-Control-Allow-Origin', 'http://127.0.0.1:8000')]		
    }
}

# Source - https://stackoverflow.com/a/41004271
# Posted by ccarton
# Retrieved 2026-07-05, License - CC BY-SA 3.0

if __name__ == '__main__':
    conf = {
        '/': {
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'image/jpeg'), ('Access-Control-Allow-Origin', 'http://my_ip')],
            'server.socket_host': 'my_ip',
            'server.socket_port': 8888
        }
    }
    cherrypy.quickstart(Camera(), '/', conf)



class AppGPS(app.App0) :
    def __init__(self) :
        self.pos = {}
        super(AppGPS, self).__init__()        
        EKOT("app GPS init")

    @cherrypy.expose
    def test(self):
        EKOT(" ==================== TEST =====================")
        return 'ok'
        
            
    @cherrypy.expose
    def position(self, name, latitude, longitude, accuracy ):
        EKOX(name)
        EKON(latitude, longitude, accuracy)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        
        self.pos[name] =  {
            "time" : current_time,
            "name" : name,            
            "latitude" : latitude,
            "longitude" : longitude,
            "accuracy" : accuracy}
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
        with open(os.path.join(gpsDir, "index.html"), "r") as file :
            EKOT("main")
            data = file.read()
            data = data.replace("INFO", self.info())
            data = data.replace("MYIP", app.MYIP)
            #EKOX(data)            
            return data

    def mount(self) :
        EKO()
        cherrypy.tree.mount(self, '/gps', config_GPS)        
        
