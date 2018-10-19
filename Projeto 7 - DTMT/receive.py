from signalTeste import *
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from matplotlib import pyplot
import peakutils
from peakutils.plot import plot as pplot
import math

signal = signalMeu()
fs = 44100
duration = 1 #seconds

dic = {	'A':[697, 1633], 'B':[770, 1633],
        'C':[852, 1633], 'D':[941, 1633],
        'X':[941, 1209], '#':[941, 1477],
        '1':[697,1209],  '2':[697, 1336],
        '3':[697, 1477], '4':[770, 1209],
        '5':[770, 1336], '6':[770, 1477],
        '7':[852, 1209], '8':[852, 1336],
        '9':[852, 1447], '0':[941, 1336]
        }

while True:
	print("\nRecording...")
	myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
	sd.wait()
	print('Finished Recording....')

	a = [i[0] for i in myrecording]
	x,y = signal.calcFFT(a, fs)
	indexes = peakutils.indexes(y, thres=0.3, min_dist=70)
	print(indexes)

	for i in range(len(indexes)-1):
		for j in dic:
			carac = dic[j]
			if math.isclose(indexes[i], carac[0], rel_tol=0) and math.isclose(indexes[i+1], carac[1], rel_tol=0):
				signal.plotFFT(a,fs)

				pyplot.figure(figsize=(8,5))
				pplot(x, y, indexes)
				axes = plt.gca()
				axes.set_xlim([0,2000])

				print("Tecla: " + j)
				plt.show()