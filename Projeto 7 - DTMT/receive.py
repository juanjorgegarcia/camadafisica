from signalTeste import *
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import time
import pickle
import peakutils

fs = 44100
duration = 2 # seconds
print("Recording...")
myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
sd.wait()
print('Finished....')
print(myrecording)
sd.play(myrecording,fs)
sd.wait()
print("fim")
