from importlib import import_module
import os
from flask import Flask, render_template, Response, request
from camera_opencv import Camera
import cv2
import numpy as np
from obj_detection import object_detect
from time import sleep
import serial
import serial.tools.list_ports

app = Flask(__name__)

@app.route("/")
def index():
    # index template
    return render_template("index.html")

def gen(camera, selector):
    global obj
    yield b'--frame\r\n'
    while True:
        if selector == 1:
            # original stream
            frame = camera.get_frame()
            frame = cv2.imencode('.jpg', frame)[1].tobytes()
            yield b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n--frame\r\n'
        else:
            # object detection stream
            frame = camera.get_frame()
            frame = obj.detect(frame)
            frame = cv2.resize(frame, (640,480))
            frame = cv2.imencode('.jpg', frame)[1].tobytes()
            yield b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n--frame\r\n'

@app.route('/orig_feed')
def orig_feed():
    frame = gen(Camera(),1)
    return Response(frame, mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/detect_feed')
def detect_feed():
    frame = gen(Camera(),0)
    return Response(frame, mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/readJoystick', methods=["GET","POST"])
def readJoystick():
    global escController
    data = request.get_json(force=True)
    msg = str(data['region']) + "," + str(data['angle']) + "\n"
    escController.write(msg.encode())
    return "none"

@app.route('/thruster', methods=["GET","POST"])
def thruster():
    global thrusterPerct, escController
    data = request.get_json(force=True)
    thrusterPerct = data
    msg = "t" + str(thrusterPerct) + "\n"
    escController.write(msg.encode())
    return "none"

@app.route('/getThruster')
def getThruster():
    global thrusterPerct
    return str(thrusterPerct)

if __name__ == '__main__':
    stopFlag = False
    thrusterPerct = 0
    # serial communication initialize
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        if p.description == "FT232R USB UART - FT232R USB UART":
            escController = serial.Serial("/dev/" + p.name, 115200)
        elif p.description == "USB Serial":
            compassController = serial.Serial("/dev/" + p.name, 115200)
        elif p.description == "u-blox 7 - GPS/GNSS Receiver":
            gpsController = serial.Serial("/dev/" + p.name, 115200)
    # object detection class
    obj = object_detect()
    # run application
    app.run(host='0.0.0.0', threaded=True)