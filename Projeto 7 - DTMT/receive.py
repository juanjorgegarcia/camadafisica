from signalTeste import *
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import time
import pickle
import peakutils

signal = signalMeu()
fs = 44100
duration = 2 # seconds
print("Recording...")
myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
sd.wait()

print('Finished....')
a=[i[0]for i in myrecording]
signal.plotFFT(a,fs)
plt.show()
# time.sleep(2)
# sd.play(myrecording,fs)
# print(myrecording)
# sd.wait()

print("fim")
