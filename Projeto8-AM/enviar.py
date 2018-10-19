import soundfile as sf

data, samplerate = sf.read('dale.wav')
print(data)
# with sf.SoundFile('dale.wav', 'rw') as f:
#     while f.tell() < len(f):
#         pos = f.tell()
#         data = f.read(1024)
#         f.seek(pos)
#         f.write(data*2)
print(data)