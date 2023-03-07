
import time
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt


t = 0
duration = 10  # seconds
fs = 44100 # frames
sd.default.channels = 1


sd.default.device = 'Microphone (USB Audio Device)'
recording = np.empty(0)
data = []
value = 0


def mean_square_root(array):
    msr = np.sqrt(np.mean(array ** 2))
    return msr
# while t < 40:
#     myrecording = sd.rec(int(fs*duration), samplerate=fs)
#     sd.wait()
#     value = (np.mean(myrecording))
#     if value > 2:
#         value = 2
#     if value < 0:
#         value = 0
#     recording = np.append(recording, value)
#     data.append(f'value={value} / t={t}')
#     print(value)
#     t += 0.5

print(f'sd.default.device: \'{sd.default.device}\'')
duration = int(input('Duration time (s): '))
print(f'duration: {duration}s')
start = input('Press ENTER to start recording')
print(f'Recording...    ({duration}s)')
raw_recording = sd.rec(int(fs*duration), samplerate=fs)
sd.wait()
print('Recording succesful')

absolute_recording = np.absolute(raw_recording)


limit_start = int((fs*duration)*(1/8))
end_data_point = int(fs*duration)

xpoints = np.linspace(0, 79, fs*duration)[limit_start:]
ypoints = absolute_recording[limit_start:]

print(xpoints)
print(ypoints)


plt.plot(xpoints, ypoints, label='I (0 tot 1)')
plt.title('Intensiteit over tijd')
plt.ylabel('Intensiteit [W/m2] (0 tot 1)')
plt.xlabel('Tijd [s]')
plt.show()


