import urllib.request, json
import time
import datetime
import pickle
from utillc import *
import argparse
import matplotlib.pyplot as plt
import numpy as np
from datetime import timedelta
import shutil, os, sys
url = "http://192.168.1.115/data_linky"

T = 1 # second
K = 3000
S = 3600*24*7

#K=3
#S = 6

fn, fn1 = "linky1.pickle", "linky2.pickle"


parser = argparse.ArgumentParser(description='monitor linky')
parser.add_argument('--read', action='store_true')
parser.add_argument('--write', action='store_true')
args = parser.parse_args()
if args.read :
    with open(fn, "rb") as f:
        d = pickle.load(f)
        dates = list(d["dates"].keys())
        EKOX(len(dates))
        dates = sorted(dates)
        d0 = dates[0]
        EKOX(d0)
        fi = d["dates"][d0]
        EKOX(fi)                
        v = np.asarray(d["values"][fi:])
        v = v[:,1]
        EKOX(v)
        n = len(v)
        EKOX(n)
        ndates = [ d0 + timedelta(seconds=s * T) for s in range(0,n)]
        EKOX(list(map(str, ndates)))
        plt.plot(ndates, v); plt.show()
if args.write :
    for j in range(999999999) :
        d = {
            "values" : [],
            "dates" : {},
        }
        for i in range(S) :
            time.sleep(T)                
            try :
                with urllib.request.urlopen(url) as p :
                    data = json.load(p)
                    #print(data["Iinst"])
                    inst,p = int(float(data["Iinst"]))*100, int(float(data["papp"]))
            except :
                inst,p = 0, 0
            d["values"].append( (inst,p))
            if i % K == 0 :
                now = datetime.datetime.now()
                d["dates"][now] = i
                EKON(i, now)
                with open(fn, "wb") as f:
                    pickle.dump(d, f)
        try :
            os.remove(fn1)
        except :
            pass
        os.replace(fn, fn1)

