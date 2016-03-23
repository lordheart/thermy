#!/usr/bin/env python

import os
import json
import threading
import Queue
import datetime
from flask import Flask, request, redirect, render_template

from PIL import Image
#from rendertext import rendertext, combinetext

LOGPATH = "log.json"
SYMBOLPATH = "static/symbols/"
BITMAPPATH = "gfx"
SERIAL_PORT = "/dev/ttyAMA0"
DTR_PIN = 18
DEBUG = False

if not DEBUG:
    from Adafruit_Thermal import Adafruit_Thermal
else:
    from dummy_printer import Adafruit_Thermal
    

def log_printtask(task):
    log.append(task)
    print("Saving logs")
    with open(LOGPATH, "w") as logfile:
        json.dump(log, logfile)
    print("Done saving")

def printer_job():
    print("Printer job started")
    while True:
        task = printer_queue.get()
        print("Printing task", task)
        text, symbol = task
        task = (text + "\n(" + str(datetime.datetime.now()) + ")", symbol)
        log_printtask(task)
        imgpath = os.path.join(BITMAPPATH, "{}.py".format(symbol))
        #symbolimg = Image.open(imgpath)
        #img = combinetext(text, symbolimg)
        #print symbolimg
        print("imgpath " + imgpath + " - symbol " + symbol)
        import sys
        sys.path.append(BITMAPPATH)
        import importlib
        smile = importlib.import_module(symbol)
        printer.printBitmap(smile.width, smile.height, smile.data)
        printer.printUpsideDown(text)
        print("Print finished")
        printer_queue.task_done()

server = Flask(__name__)

@server.route("/")
def index_page():
    symbols = []
    for filename in os.listdir(SYMBOLPATH):
        symbols.append(os.path.splitext(filename)[0])
    symbols.sort()
    return render_template("index.html", symbols=symbols)

@server.route("/status")
def status_page():
    paper_status = printer.hasPaper()
    return render_template("status.html", paper_status=paper_status, log=log)

@server.route("/log")
def log_page():
    return render_template("log.html", log=log)

@server.route("/redirect")
def redirect_page():
    return render_template("redirect.html")

@server.route("/static/<path:name>")
def get_resource(name):
    return send_from_directory("static", name)

@server.route("/print", methods=["POST"])
def print_post():
    text = request.form["text"]
    symbol = request.form["symbol"]
    task = (text, symbol)
    printer_queue.put(task)
    print("Printing text:", text, "with symbol", symbol)
    return redirect("/redirect", code=303)



printer_queue = Queue.Queue()
printer = Adafruit_Thermal(SERIAL_PORT, 19200, heattime=255, 
    dtr=DTR_PIN, timeout=5)
printer.reset()
printer.setDefault()
print "printer reset"

# Check if the logfile exists and is not empty
if os.path.exists(LOGPATH) and os.path.getsize(LOGPATH) > 0:
    with open(LOGPATH, "r") as logfile:
        log = json.load(logfile)
else:
    log = []
    with open(LOGPATH, "w") as logfile:
        # Write an empty list
        logfile.write("[]")

print_thread = threading.Thread(target=printer_job)
print_thread.daemon = True
print_thread.start()

server.run(host="0.0.0.0", debug=True)