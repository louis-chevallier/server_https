import os
from utillc import *
import utillc
import cherrypy
import threading
import queue
import nmap
import subprocess
import json, pickle, re, time

fileDir = os.path.dirname(os.path.abspath(__file__))
localDir = os.path.join(fileDir, '.')
EKOX(fileDir)

rootDir = os.path.join(localDir, "html")
EKOX(rootDir)


gitdir = os.path.join(fileDir, '..')
MYIP = os.environ["MYIP"]


apps = []

tels = ["tel_louis", "Galaxy-A51", "S20-FE-de-David-001" ]


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
                            ipok = 1;
                            EKON(ipok, ip)
                        except subprocess.CalledProcessError as ex:
                            # exception if ping fails ( donc device absent)
                            EKOX(ex);
                            pass
            mode = "HOME_MODE" if len(self.devices_connected) > 0 else "AWAY_MODE"
            EKOX(mode)

            if self.mode == "auto" :
                self.alarm(mode)
                
            #EKOX(self.devices_connected)
            #time.sleep(6)
            time.sleep(60*1)
            EKO()



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
