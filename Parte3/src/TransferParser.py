from scipy import signal
import numpy as np

class TransferParser:
	
	def parsePZG(self, data):
		# paso en data [polos, ceros, gain]
		try:
			valid = True
			polos = data[0].split(" ")
			ceros = data[1].split(" ")

			polos = [complex(i) for i in polos]
			ceros = [complex(i) for i in ceros]
			gain = float(data[2])

			s1 = signal.lti(polos, ceros, gain)
			w,mag,phase = signal.bode(s1)
			return valid, [w/(2*np.pi), mag, phase]
		except:
			return False, []

	def parseNumDen(self, data):
		try:
			valid = True
			num = data[0].split(" ")
			den = data[1].split(" ")

			num = [complex(i) for i in num]
			den = [complex(i) for i in den]
			s1 = signal.lti(num, den)
			w,mag,phase = signal.bode(s1)
			return valid, [w/(2*np.pi), mag, phase]
		except:
			return False, []