import numpy as np
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
profile = np.array([1, 2, 3, 4, 5, 4, 3, 2, 1, 2, 3, 4, 3, 2, 1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1, 2, 3, 2, 1, 1, 1, 2, 1, 4, 1, 5, 6, 1, 3, 4, 1, 1, 2, 3, 1, 1, 5, 4, 3, 2, 2, 1, 0, 0, 0, 0])
duration = 3

# https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html


profile_peaks = find_peaks(profile)

print(profile_peaks)

peaks = profile[profile_peaks[0]]
peaks = np.insert(peaks, 0, 0)
print(peaks)

xpoints = np.linspace(0, duration, len(np.absolute(profile)))
ypoints = np.absolute(profile)
x_peak = np.linspace(0, duration, len(peaks))
y_peak = peaks

plt.plot(xpoints, ypoints, label='Profile')
plt.plot(x_peak, y_peak, label='Profile Peaks')

plt.title('Profile')
plt.ylabel('y -->')
plt.xlabel('x -->')
plt.show()