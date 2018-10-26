import soundfile as sf
from scipy import signal
from signalTeste import signalMeu as st
import matplotlib.pyplot as plt
import sounddevice as sd
import numpy as np
time = 0.5
amplitude = 1
freq = 12000



sig = st()
data, samplerate = sf.read('dale.wav')
samplerate = 44100
one_channel_data=[i[0] for i in data]
plt.plot(one_channel_data)
plt.show()
sig.plotFFT(one_channel_data,samplerate)
plt.title("Fourier do audio")
plt.show()

# normalized_audio = [i/max(one_channel_data) for i in one_channel_data]
max_value = max(one_channel_data)
normalized_audio = list(map(lambda x: x/max_value, one_channel_data))

sig.plotFFT(normalized_audio,samplerate)
normalized_audio += [0]*20000
plt.title("Fourier do audio normalizado")

plt.show()

#exemplo de filtragem do sinal yAudioNormalizado
# https://scipy.github.io/old-wiki/pages/Cookbook/FIRFilter.html
nyq_rate = samplerate/2
width = 5.0/nyq_rate
ripple_db = 60.0 #dB
N , beta = signal.kaiserord(ripple_db, width)
cutoff_hz = 4000.0
taps = signal.firwin(N, cutoff_hz/nyq_rate, window=('kaiser', beta))
filtered_audio = signal.lfilter(taps, 1.0, normalized_audio)

sig.plotFFT(filtered_audio,samplerate)
plt.title("Fourier do audio filtrado")
plt.show()
x,carrier = sig.generateSin(freq,amplitude,len(filtered_audio)/samplerate,samplerate)

am_audio = list(map(lambda x,y: (x)*y, filtered_audio,carrier))
# am_audio = filtered_audio*carrier
print((len(filtered_audio)))
plt.plot(x,am_audio)
sig.plotFFT(am_audio,samplerate)
plt.title("Fourier do audio AM")

plt.show()
# am_audio.export("moduled_audio", format="wave")
from scipy.io.wavfile import write
write('test.wav', 44100, np.array(am_audio))

sd.play(am_audio)
sd.wait()
# print(min(normalized_audio),max(normalized_audio))
