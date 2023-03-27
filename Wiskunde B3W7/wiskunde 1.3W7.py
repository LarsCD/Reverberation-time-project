import numpy as np
import matplotlib.pyplot as plt

# constanten
m = 1
c = 0.2
k = 1

# tijd
teind = 100
Nstap = 10000+1
tijd = np.linspace(0, teind, Nstap)
dt = teind/(Nstap-1)

# formules a,b
a = (k - 2*m/(dt**2))/(m/(dt**2)+c/(2*dt))
b = (m/(dt**2)-c/(2*dt))/(m/(dt**2)+c/(2*dt))

# begin waarde
x0 = 1
v0 = 0

# positie en eerste stap
x = np.zeros_like(tijd)
x[0] = x0
x[1] = x0+dt*v0

for ti in range(1,Nstap-1):
    x[ti + 1] = -a * x[ti] - b * x[ti - 1]

plt.plot(tijd, x)
plt.show()

# -----------------------------------------------------------------------------------------

# constanten
m = 1
c = 0.2
k = 1
F0 = 1

F0e = F0/(m/(dt**2)+c/(2*dt))
f = 0.12

for ti in range(1,Nstap-1):
    x[ti+1]=-a*x[ti]-b*x[ti-1]+F0e*np.sin(2*np.pi*f*tijd[ti])

# begin waarde
x0 = 0
v0 = 0




