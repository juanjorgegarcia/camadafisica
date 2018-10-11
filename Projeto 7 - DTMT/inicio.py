from signalTeste import *
import sounddevice as sd
import matplotlib.pyplot as plt
import time
from scipy.fftpack import fft

dict_freq = {	'A':[697, 1633], 'B':[770, 1633],
                'C':[852, 1633], 'D':[941, 1633],
                'X':[941, 1209], '#':[941, 1477],
                '1':[697,1209],  '2':[697, 1336],
                '3':[697, 1477], '4':[770, 1209],
                '5':[770, 1336], '6':[770, 1477],
                '7':[852, 1209], '8':[852, 1336],
                '9':[852, 1447], '0':[941, 1336]
                }
signal = signalMeu()
para = False
tempo = 0.5
fs = 44100

while not para:
	dial = input("\nDigite aqui seu número: ")

	if dial.upper() == "QUIT":
		para = True

	else:
		try:
			carac = dict_freq[dial.upper()]
			x1, seno1 = signal.generateSin(carac[0], 1, tempo, fs)
			x2, seno2 = signal.generateSin(carac[1], 1, tempo, fs)
			som = seno1 +seno2
			sd.play(som)
			sd.wait()

			plt.plot(som)
			axes = plt.gca()
			axes.set_xlim([0,500])
			plt.show()

			signal.plotFFT(som, fs)
			plt.show()

		except:
			print("Caractere não identificado")	