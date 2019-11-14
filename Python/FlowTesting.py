import numpy as np
import matplotlib.pyplot as plt
import csv
import nmrglue as ng
from scipy import optimize
from scipy.interpolate import *
from numpy import *
import math
import os
from scipy import stats



starting_point = 27
peaks = 4
OscError = 3 #+/- Hz uncertainty on the oscilliscope for measuring flow velocity
"""
Below, I will create variables that define the slope and flow velocities of the measurements to be
used after this loop to gather that data in the files.
"""
flowVelocity = [] #Array that stores the flow velocities
BA_Data = [] #This is the value of B/A (Slope/Intersept)
OscErrorCCM = 3*15/2

for flowFile in os.listdir("C:/Users/Devin/Desktop/HonorsProject/Python"):
    if flowFile.endswith(".tnt"):
        dic,data = ng.tecmag.read(flowFile)

        magnitudeY = []
        timeX = []
        i = 0
        time = 0
        while (i<data.size):
            magnitudeY.append(math.sqrt((float(data[i].imag))**2+(float(data[i].imag))**2))
            i += 1
            time += float(dic["acq_time"]/dic["acq_points"])
            timeX.append(time)
        #######################################################################################
        # This part of the code will create the linear fit
        increment_point = dic["acq_points"]*2


        InterpolationX = [] 
        InterpolationY = [] 
        for i in range(0, peaks):
            #iff the magnitude of the data is large on either +1 or -1 then use the largest
            if magnitudeY[(increment_point*i + starting_point)+1] > magnitudeY[(increment_point*i + starting_point)]:
                InterpolationX.append(timeX[(increment_point*i + starting_point)+1])
                InterpolationY.append(magnitudeY[(increment_point*i + starting_point)+1])
            elif magnitudeY[(increment_point*i + starting_point)-1] > magnitudeY[(increment_point*i + starting_point)]:
                InterpolationX.append(timeX[(increment_point*i + starting_point)-1])
                InterpolationY.append(magnitudeY[(increment_point*i + starting_point)-1])
            else:  
                InterpolationX.append(timeX[increment_point*i + starting_point])
                InterpolationY.append(magnitudeY[increment_point*i + starting_point])

        plt.plot(InterpolationX, InterpolationY, label= ("%s peaks data" % peaks))
        p1 = polyfit(InterpolationX,InterpolationY,1)


        #Adding Params into FlowVel and BA_Data
        flowVelocity.append(int(flowFile[5:9])) #Creating the flowVelocity array
        B_A = -1*p1[0]/p1[1] #Slope over intercept
        BA_Data.append(B_A) #Creating the BA_Data array
    
        plt.plot(timeX, polyval(p1,timeX), label='Linear Fit')

        ########

        plt.plot(timeX, magnitudeY, label='data')
        plt.xlabel("Time (sec)")
        plt.ylabel("Magnitude (Arbitrary)")
        plt.title("Flow Velocity of: %s CCM" % flowFile[5:9])

        plt.legend()
        plt.figure(1)
        #plt.show()

    else:
        print('File found but not .tnt format')
        continue

plt.close()

p2, residuals, _, _, _ = polyfit(flowVelocity,BA_Data,1, full=True)
plt.plot(flowVelocity, polyval(p2,flowVelocity), label='linear fit')

plt.style.use('dark_background')
plt.errorbar(flowVelocity, BA_Data,
            xerr=OscErrorCCM,
            yerr=math.sqrt(residuals/len(BA_Data)),
            fmt='.k--', label='Actual Data')

plt.xlabel('Flow Velocity (CCM)')
plt.ylabel('-B/A')
plt.legend()
plt.show()

##Error Analysis
slope, intercept, r_value, p_value, std_err = stats.linregress(flowVelocity,BA_Data)

print("______________________________________________________________")
print("Acq_ time: %s"%dic["acq_time"])
print("Acq_ Points: %s"%dic["acq_points"])
print("R Squared : %s"%r_value)

print("P Value : %s"%p_value)
print("Standard Error: %s"%std_err)
