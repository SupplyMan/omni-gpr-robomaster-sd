from motor import Motor
import math

class Chassis:
	def __init__(self, pi, freq):
		self.pi = pi

		self.m1 = Motor(self.pi, freq, 2, 3, 4)
		self.m2 = Motor(self.pi, freq, 17, 27, 22)
		self.m3 = Motor(self.pi, freq, 10, 9, 11)
		self.m4 = Motor(self.pi, freq, 5, 6, 13)

	def stop(self):
		self.m1.move(0)
		self.m2.move(0)
		self.m3.move(0)
		self.m4.move(0)

	def forward(self):
		self.m1.move(1.0)
		self.m2.move(-1.0)
		self.m3.move(0)
		self.m4.move(0)

	def backward(self):
		self.m1.move(-1.0)
		self.m2.move(1.0)
		self.m3.move(0)
		self.m4.move(0)

	def right(self):
		self.m1.move(0)
		self.m2.move(0)
		self.m3.move(-1.0)
		self.m4.move(1.0)

	def left(self):
		self.m1.move(0)
		self.m2.move(0)
		self.m3.move(1.0)
		self.m4.move(-1.0)

	def holonomic(self, ang, speed=1.0, rotation_speed=0.0):
		Px = speed * (math.sin(ang + math.pi / 4))
		Py = speed * (math.sin(ang - math.pi / 4))
		print(Px, Py)
		self.m1.move(Px)
		self.m2.move(-Px)
		self.m3.move(-Py)
		self.m4.move(Py)
