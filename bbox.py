#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://usefulangle.com/post/352/javascript-capture-image-from-camera

import os, gc, sys, glob
import os, json, base64
import shutil
import re
from utillc import *
import threading
import queue
import json, pickle
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

def send(url) :
    with urllib.request.urlopen(url) as response:
        html = response.read()
        EKOX(html)


send("https://mabbox.bytel.fr/api/v1/login?password=BBoxBBox_35")
send("https://mabbox.bytel.fr/api/v1/device/token")
