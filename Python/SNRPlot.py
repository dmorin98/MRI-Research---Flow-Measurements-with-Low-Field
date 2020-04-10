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
NoisePoints=3
import time

flow = []
SNR = []
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
            i += 1
            time += float(dic["acq_time"]/dic["acq_points"])
            timeX.append(time)

        NoiseSum = 0

        for i in range(0, NoisePoints, 1):
            NoiseSum += magnitudeY[-i]

        NoiseSum = NoiseSum/NoisePoints

        #Finding Highest Point value
        High = 0

        for value in range(0,len(magnitudeY),1):
            if(int(magnitudeY[value]) > High):
                High = int(magnitudeY[value])
                #print('Highest val:', High)
                   
        flow.append(flowFile[5:9])
        SNR.append(High/NoiseSum)
        print('Highest val:', High)
        print('File:', flowFile[5:9])   
        
        print("SNR:", (High/NoiseSum))
from matplotlib import pyplot as plt
plt.plot(flow,SNR)
plt.show()



