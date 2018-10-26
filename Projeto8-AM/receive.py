import soundfile as sf
from scipy import signal
from signalTeste import signalMeu as st
import matplotlib.pyplot as plt
import sounddevice as sd
time = 0.5
amplitude = 1
freq = 12000
fs = 44100
duration = 5

sig = st()
print("gravando")
myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
sd.wait()
print("pronto")
myrecording = [i[0] for i in myrecording]

#myrecording, samplerate = sf.read('test.wav')
sd.play(myrecording)
sd.wait()

sig.plotFFT(myrecording, fs)
plt.show()

x,carrier = sig.generateSin(freq,amplitude,len(myrecording)/fs,fs)
demodule_audio = list(map(lambda x,y: (x)*y, myrecording,carrier))
sig.plotFFT(demodule_audio, fs)
plt.show()

a = [0 for i in range(20000)]
audio = demodule_audio+a

taxa = fs/2
width = 5.0/taxa
ripple_db = 60.0 #dB
N , beta = signal.kaiserord(ripple_db, width)
cutoff_hz = 4000.0
taps = signal.firwin(N, cutoff_hz/taxa, window=('kaiser', beta))
yFiltrado = signal.lfilter(taps, 1.0, demodule_audio)

sig.plotFFT(yFiltrado, fs)
plt.show()
print("audio filtrado")
sd.play(yFiltrado)
sd.wait()