import numpy as np
import matplotlib.pyplot as plt
import nmrglue as ng
from scipy import optimize
from numpy import polyval, polyfit
import math
import os
from scipy import stats
FinalmagnitudeY = []
FinaltimeX = []
Num_File=0
NoisePoints=5
import time


for flowFile in os.listdir("C:/Users/Devin/Documents/GitHub/MRI-Research---Flow-Measurements-with-Low-Field/Python"):
    if flowFile.endswith(".tnt"):
        dic,data = ng.tecmag.read(flowFile)

        magnitudeY = []
        realY = []
        imagY = []
        timeX = []
        Num_File += 1
        i = 0
        time = 0
        increment_point = int(dic["acq_points"]*2)
        while (i<data.size):
            magnitudeY.append(math.sqrt((float(data[i].imag))**2+(float(data[i].real))**2))
            if(Num_File==1):
                FinalmagnitudeY.append(math.sqrt((float(data[i].imag))**2+(float(data[i].real))**2))
                FinaltimeX.append(time)
            i += 1
            time += float(dic["acq_time"]/dic["acq_points"])
            timeX.append(time)



        for i in range(0,len(FinaltimeX),1):
            FinalmagnitudeY[i] += magnitudeY[i]
            FinaltimeX[i] += timeX[i]


time=[]
mag=[]


for number in FinalmagnitudeY:
    mag.append(number/Num_File)


plt.plot(timeX,mag)
plt.show()

NoiseSum = 0

for i in range(0, NoisePoints, 1):
    NoiseSum += mag[-i]
NoiseSum = NoiseSum/NoisePoints

#Finding Highest Point value
High = 0

for value in range(0,len(mag),1):
    if(int(mag[value]) > High):
        High = int(mag[value])
        print('Highest val:', High)


print("SNR:", (High/NoiseSum))
