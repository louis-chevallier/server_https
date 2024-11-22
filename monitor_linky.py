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
#url = "http://192.168.1.6/data_linky"

T = 1 # second
K = 3000
S = 3600*24*7

MAX_LEN = S # sliding over 1 week

#K=6
#S=31

fn1, fn2 = "linky1.pickle", "linky2.pickle"


parser = argparse.ArgumentParser(description='monitor linky')
parser.add_argument('--read', action='store_true')
parser.add_argument('--write', action='store_true')
parser.add_argument('--file', default=fn1)
args = parser.parse_args()

def read() :
	with open(args.file, "rb") as f:
		d = pickle.load(f)
		EKOX(len(d["values"]))
		v = np.asarray(d["values"])
		v = v[:,1]
		EKOX(v)
		n = len(v)
		EKOX(n)
		d0 = d["date"]
		ndates = [ d0 + timedelta(seconds=s * T) for s in range(0,n)]
		EKOX(list(map(str, ndates)))
		return ndates, v

def write_step(d, i) :
	# called every T seconds
	inst,pp = 0, 0
	EKO()
	try :
		with urllib.request.urlopen(url) as p :
			data = json.load(p)
			#print(data["Iinst"])
			inst,pp = int(float(data["Iinst"]))*100, int(float(data["papp"]))
			EKON(inst, pp)
	except Exception as e  :
		EKOX(e)
		pass
	d["values"].append( (inst,pp))			

	# discard old records
	if (len(d["values"]) > MAX_LEN) :
		d["values"].pop(0)
		d["date"] = d["date"] + timedelta(seconds=T)
		
	# saving every K*T sec
	if i % K == 0 :
		with open(fn1, "wb") as f:
			pickle.dump(d, f)
			
	
if __name__ == '__main__':

	if args.read :
		ndates, v = read()
		plt.plot(ndates, v); plt.show()
	if args.write :
		for j in range(999999999) :
			d = {
				"values" : [],
				"date" : datetime.datetime.now() # date of first record
			}
			for i in range(S) :
				EKOX(i)
				time.sleep(T)
				write_step(d, i)


