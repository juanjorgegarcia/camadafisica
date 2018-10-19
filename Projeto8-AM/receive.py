import soundfile as sf
from scipy import signal
from signalTeste import signalMeu as st
import matplotlib.pyplot as plt
import sounddevice as sd
time = 0.5
amplitude = 1
freq = 8000
fs = 44100
duration = 2

sig = st()
myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
sd.wait()

myrecording = [i[0]for i in myrecording]

sd.play(myrecording)

x,carrier = sig.generateSin(freq,amplitude,65621/fs,fs)
demodule_audio = list(map(lambda x,y: (x)*y, myrecording,carrier))

#exemplo de filtragem do sinal yAudioNormalizado
# https://scipy.github.io/old-wiki/pages/Cookbook/FIRFilter.html
nyq_rate = fs/2
width = 5.0/nyq_rate
ripple_db = 60.0 #dB
N , beta = signal.kaiserord(ripple_db, width)
cutoff_hz = 4000.0
taps = signal.firwin(N, cutoff_hz/nyq_rate, window=('kaiser', beta))
filtered_audio = signal.lfilter(taps, 1.0, myrecording)
sd.play(filtered_audio)
sd.wait()