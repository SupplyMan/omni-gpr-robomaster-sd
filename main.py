from flask import Flask, request

import pigpio
from chassis import Chassis
import rotary_encoder

from simple_pid import PID
import pyrealsense2 as rs
import sys

Debug_ = False # When you're not debugging, set this flag to False
app = Flask(__name__)

ServerIP = sys.argv[1]#'192.168.137.119'
ServerPort = 5000

allowedClients = {117, 223, 332}

@app.route('/path', methods=['POST'])
def path():
	try:
		msg = request.get_json()

		if msg['id'] not in allowedClients:
			print("Unauthorized client tried to control the robot!")
			return "NOT ALLOWED!\n"

		print("path data received")

		ExecuteTrajectory(msg["resolution"], msg["moves"])

		return "OK\n"
	except Exception as e:
		return "ERROR\n"

@app.route('/rect', methods=['POST'])
def rect():
	try:
		msg = request.get_json()

		if msg['id'] not in allowedClients:
			print("Unauthorized client tried to control the robot!")
			return "NOT ALLOWED!\n"

		print("rect parameters received")

		moves = []

		dir = True

		for i in range(msg["width"]):
			if dir:
				moves.append({"dir":"forward", "dist":msg["length"]})
			else:
				moves.append({"dir":"backward", "dist":msg["length"]})

			dir = not dir

			if i < msg["width"]-1:
				moves.append({"dir":"right", "dist":1})

		ExecuteTrajectory(msg["resolution"], moves)

		return "OK\n"
	except Exception as e:
		return "ERROR\n"

pi = pigpio.pi()
freq = 500

ch = Chassis(pi, freq)

pos = [0, 0, 0, 0]
prev = []

def cb1(way):
	global pos
	pos[0] += way

def cb2(way):
	global pos
	pos[1] += way

def cb3(way):
	global pos
	pos[2] += way

def cb4(way):
	global pos
	pos[3] += way

d1 = rotary_encoder.decoder(pi, 14, 15, cb1)
d2 = rotary_encoder.decoder(pi, 20, 21, cb2)
d3 = rotary_encoder.decoder(pi, 8, 7, cb3)
d4 = rotary_encoder.decoder(pi, 23, 24, cb4)

def ExecuteTrajectory(cell_size, moves):
	n = 440
	circ = 0.187

	for move in moves:
		dist = int(n*move["dist"]*cell_size/circ)
		
		if move["dir"] == "forward":
			cur_pos = pos.copy()
			ch.forward()
			while(abs(pos[0]-cur_pos[0])<dist and abs(pos[1]-cur_pos[1])<dist):
				pass

		elif move["dir"] == "backward":
			cur_pos = pos.copy()
			ch.backward()
			while(abs(pos[0]-cur_pos[0])<dist and abs(pos[1]-cur_pos[1])<dist):
				pass

		elif move["dir"] == "right":
			cur_pos = pos.copy()
			ch.right()
			while(abs(pos[2]-cur_pos[2])<dist and abs(pos[3]-cur_pos[3])<dist):
				pass

		elif move["dir"] == "left":
			cur_pos = pos.copy()
			ch.left()
			while(abs(pos[2]-cur_pos[2])<dist and abs(pos[3]-cur_pos[3])<dist):
				pass
	
	ch.stop()

if __name__ == "__main__":
	try:
		app.run(host=ServerIP, port=ServerPort)
	except KeyboardInterrupt:
		print("Keyboard Interrupt")