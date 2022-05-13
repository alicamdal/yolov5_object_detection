import json
import requests
from xbox import XboxController
import numpy as np
from time import sleep
import math


def main(joy):
	global ip
	stopFlag = True
	data = {
		"region" : -1,
		"angle"  : -1
	}
	thruster = 0
	nFlag = True
	sFlag = True
	old_x = old_y = old_s = old_n = old_e = old_w = 0
	old_data = None
	while True:
		x, y, s, n, e, w = joy.read()
		# stop reading
		if e == 1:
			stopFlag = True
			data['region'] = -1
			data['angle'] = -1
		# start reading
		if w == 1:
			stopFlag = False
		if n == 1 and nFlag:
			# increase thruster by 5
			thruster += 5
			thrs = json.dumps(thruster)
			requests.post("http://" + ip + ":5000/thruster",data=thrs)
			nFlag = False
		elif n == 0:
			nFlag = True
		if s == 1 and sFlag:
			# decrease thruster by 5
			thruster -= 5
			thrs = json.dumps(thruster)
			requests.post("http://" + ip + ":5000/thruster",data=thrs)
			sFlag = False
		elif s == 0:
			sFlag = True
		if not stopFlag:
			# if system is on read joystick data and normalize them
			x = np.interp(x, [-32768,32768],[0,1023])
			y = np.interp(y, [-32768,32768],[0,1023])
			x = x - 512
			y = y - 512
			deg = math.atan2(y, x)
			if deg < 0:
				angle = np.ceil(-deg * (180 / math.pi))
			else:
				angle = np.ceil(360 - (deg * (180 / math.pi)))
		else:
			angle = -1
		# create angle
		data['angle'] = int(angle)
		# find joystick region on coordinate system
		if angle > 0 and angle <= 90:
			data['region'] = 1
		elif angle > 90 and angle <= 180:
			data['region'] = 2
		elif angle > 180 and angle <= 270:
			data['region'] = 3
		elif angle > 270 and angle <= 360:
			data['region'] = 4
		# send data if there is any change
		if old_data != data :
			requests.post("http://" + ip + ":5000/readJoystick",data=json.dumps(data))
			old_x = x
			old_y = y
			old_s = s
			old_n = n
			old_e = e
			old_w = w
		sleep(0.001)

if __name__ == "__main__":
	ip = "192.168.10.113" # WebServer IP
	joy = XboxController()
	main(joy)