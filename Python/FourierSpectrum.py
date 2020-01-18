import numpy as np
import matplotlib.pyplot as plt
import nmrglue as ng
from scipy import optimize
from numpy import polyval, polyfit
import math
import os
from scipy import stats
from numpy.fft import fft, fftfreq, ifft
NewWay = False
PeakSum = 1
starting_point = 27
peaks = 3
OscError = 3 #+/- Hz uncertainty on the oscilliscope for measuring flow velocity
diam_tube = 0.0075 #m
density_fluid = 995 #kg/m^3
viscocity = 0.001054 #of fluid (kg/ms)

"""
Below, I will create variables that define the slope and flow velocities of the measurements to be
used after this loop to gather that data in the files.
"""


flowVelocity = [] #Array that stores the flow velocities
BA_Data = [] #This is the value of B/A (Slope/Intersept)
OscErrorCCM = 3*15/2
def getFlowVel(CCM):
    area = math.pi*(diam_tube/2)**2
    return (CCM/(100**3*60*area))

def flowCalc(flow_file):
    flow_numberCCM = int(flow_file[5:9])
    return getFlowVel(flow_numberCCM)


def reynolds(flow_Velocity):
     Re = []
    
     for i in range(0, len(flow_Velocity), 1):
         reynolds_number = density_fluid*flowVelocity[i]*diam_tube/viscocity
         Re.append(reynolds_number)
         #print(reynolds_number)
         
     return Re

def plotPeaks():
    total = 0
    for x in range(0, (PeakSum+1)*2):
        print("x : ", PeakSum/2)
        total += magnitudeY[(increment_point*i + starting_point)-int(PeakSum/2)+x]  
    

for flowFile in os.listdir("C:/Users/Devin/Documents/GitHub/MRI-Research---Flow-Measurements-with-Low-Field/Python"):
    if flowFile.endswith(".tnt"):
        dic,data = ng.tecmag.read(flowFile)

        magnitudeY = []
        timeX = []
        i = 0
        time = 0
        while (i<data.size):
            magnitudeY.append(math.sqrt((float(data[i].imag))**2+(float(data[i].real))**2))
            i += 1
            time += float(dic["acq_time"]/dic["acq_points"])
            timeX.append(time)
        #######################################################################################
        # This part of the code will create the linear fit
        increment_point = dic["acq_points"]*2

        #Adding Params into FlowVel and BA_Data
        flowVelocity.append(flowCalc(flowFile)) #Creating the flowVelocity array

        ########

        plt.plot(timeX, magnitudeY, label='data')
        plt.xlabel("Time (sec)")
        plt.ylabel("Magnitude (Arbitrary)")
        plt.title("Flow Velocity of: %s CCM" % flowFile[5:9])

        plt.legend()
        plt.figure(1)
        plt.show()
        plt.close(1)


        #Fourier Transformed Image
        plt.figure(2)
        fft_freq = fftfreq(512)
        fft_vals = fft(magnitudeY)
        plt.plot(fft_freq, fft_vals)
        plt.show()
        plt.close(2)




    else:
        print('File found but not .tnt format')
        continue



