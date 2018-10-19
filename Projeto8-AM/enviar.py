import soundfile as sf

data, samplerate = sf.read('dale.wav')
one_channel_data=[i[0] for i in data]

# normalized_audio = [i/max(one_channel_data) for i in one_channel_data]
# normalized_audio = list(map(lambda x: x/max(one_channel_data), one_channel_data))

# print(min(normalized_audio),max(normalized_audio))
for i in one_channel_data:
    print(i/max(one_channel_data))