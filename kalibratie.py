
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
print(sd.query_devices())
print('')


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


# get duration in seconds input from user
def get_duration_input():
    duration = int(input('Input recodring duration time (s): '))
    print(f'Duration: {duration}s')
    return duration

# perform recording and return output
def perform_raw_recodring(duration):
    print(f'Device:  \'{sd.default.device}\'')
    print(f'Duration: {duration}s')
    start = input('Press [ENTER] to start recording')
    time.sleep(1)
    print(f'Recording...    ({duration}s)')
    raw_recording = sd.rec(int(fs*duration), samplerate=fs)
    sd.wait()
    print('Recording succesful')
    return raw_recording


# turn raw recording into dB recording
def raw_recording_to_dB_recording(raw_recording):
    intensiteit_ongekalibreerd = np.absolute(raw_recording)

    limit_start = int((fs*duration)*(1/8))
    end_data_point = int(fs*duration)

    correctiefactor_experimenteel = 0.99088
    correctiefactor_2 = 0.85000
    afgeleide_int = np.diff(intensiteit_ongekalibreerd)

    intensiteit_toppen = []

    for value in afgeleide_int:
        if value < 0.001:
            intensiteit_toppen.append(value)

    intensiteit_toppen = np.array(intensiteit_toppen)

    dB_recording = (np.log((intensiteit_ongekalibreerd)/(1*(10**-6)))/0.1141)*correctiefactor_experimenteel
    return dB_recording



duration = get_duration_input()
raw_recording = perform_raw_recodring(duration)
dB_recording = raw_recording_to_dB_recording(raw_recording)


xpoints = np.linspace(0, duration, len(np.absolute(dB_recording)))
ypoints = dB_recording

x2 = np.linspace(0, duration, len(np.absolute(raw_recording)))
y2 = np.absolute(raw_recording)

# print(xpoints)
# print(ypoints)
max = np.max(ypoints)
print(f'Max is: {max}')

plt.plot(xpoints, ypoints, label='I (0 tot 1)')
plt.title('dB over tijd')
plt.ylabel('dB')
plt.xlabel('Tijd [s]')
plt.show()

plt.plot(x2, y2, label='I (0 tot 1)')
plt.title('Intensiteit over tijd')
plt.ylabel('Intensiteit [W/m2] (0 tot 1)')
plt.xlabel('Tijd [s]')
plt.show()
