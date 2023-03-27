import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

xdata = np.array([0, 0.125, 0.250, 0.375, 0.500, 0.625, 0.750, 0.875])
ydata = np.array([2.581, 3.254, 3.476, 3.840, 4.408, 4.852, 4.905, 5.397])



def func(x, a, b):
    return a*x+b

plt.plot(xdata, ydata, 'b', label='data')

popt, pcov = curve_fit(func, xdata, ydata)
popt_sigma, pcov = curve_fit(func, xdata, ydata, sigma=np.zeros(8)+0.1, absolute_sigma=True)

plt.plot(xdata, func(xdata, *popt), 'r--',
         label='fit: a=%5.3f, b=%5.3f' % tuple(popt))

print(f'Beste a={popt_sigma[0]}+/-{pcov[0,0]**0.5}')
print(f'Beste b={popt_sigma[1]}+/-{pcov[1,1]**0.5}')

plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.show()
