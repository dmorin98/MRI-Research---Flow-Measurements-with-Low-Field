import numpy as np

import matplotlib.pyplot as plot
from scipy import stats
from numpy.fft import fft, fftfreq, ifft
points = 1000
time = 100
freq = 2.0*np.pi/time

x = np.linspace(0,time,points)
amplitude  = np.cos(100.0*freq*x)

plot.figure(1)
plot.plot(x, amplitude)
plot.title('Sine wave')

# Give x axis label for the sine wave plot
plot.xlabel('Time')

plot.ylabel('Amplitude = sin(time)')
plot.grid(True, which='both')
plot.axhline(y=0, color='k')
plot.show()
# Display the sine wave
plot.show()
plot.close(1)

plot.figure(2)
fft_freq = fftfreq(points)
fft_vals = fft(amplitude)
plot.plot(fft_freq, fft_vals)
plot.show()
plot.close(2)
