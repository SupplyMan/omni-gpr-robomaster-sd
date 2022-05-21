import pigpio

class Motor:
	def __init__(self, pi, freq, inA, inB, enable):
		self.pi = pi
		self.inA = inA
		self.inB = inB
		self.enable = enable

		pi.set_mode(inA, pigpio.OUTPUT)
		pi.set_mode(inB, pigpio.OUTPUT)
		pi.set_mode(enable, pigpio.OUTPUT)

		pi.set_PWM_frequency(enable, freq)

	def move(self, speed):
		if speed > 0.0 and speed <= 1.0:
			self.pi.write(self.inA, 1)
			self.pi.write(self.inB, 0)
			self.pi.set_PWM_dutycycle(self.enable, int(speed*255))

		elif speed == 0.0:
			self.pi.write(self.inA, 0)
			self.pi.write(self.inB, 0)
			self.pi.set_PWM_dutycycle(self.enable, 0)

		elif speed < 0.0 and speed >= -1.0:
			self.pi.write(self.inA, 0)
			self.pi.write(self.inB, 1)
			self.pi.set_PWM_dutycycle(self.enable, int(-speed*255))