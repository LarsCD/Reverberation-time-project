import sounddevice as sd
import time


t = 0
sd.RawInputStream.start()

while t < 50:
    input = sd.RawInputStream.read()
    print(f'[t={t}]: Reading input: {input}')
    time.sleep(0.1)
    t += 1

sd.RawInputStream.stop()
