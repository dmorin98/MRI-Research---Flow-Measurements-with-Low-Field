import numpy as np
import matplotlib.pyplot as plt
import nmrglue as ng
from scipy import optimize
from numpy import polyval, polyfit
import math
import os
from scipy import stats
from numpy.fft import fft, fftfreq, ifft

Num_File = 3
PeakSum = 3
starting_point = 27
peaks = 3
OscError = 3 #+/- Hz uncertainty on the oscilliscope for measuring flow velocity
diam_tube = 0.0075 #m
density_fluid = 995 #kg/m^3
viscocity = 0.001054 #of fluid (kg/ms)

font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 15}	
plt.rc('font', **font)

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
        
         
     return Re

def plotPeaks():
    total = 0
    for x in range(0, ((PeakSum)*2)-1):
        total += magnitudeY[(increment_point*i + starting_point)-int(PeakSum/2)+x]  
    
    
    InterpolationX.append(timeX[(increment_point*i + starting_point)])
    InterpolationY.append(total)

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

        InterpolationX = [] 
        InterpolationY = [] 
        for i in range(0, peaks):
            plotPeaks()


        plt.plot(InterpolationX, InterpolationY, label= ("%s peaks data" % peaks))
        p1 = polyfit(InterpolationX,InterpolationY,1)


        #Adding Params into FlowVel and BA_Data
        flowVelocity.append(flowCalc(flowFile)) #Creating the flowVelocity array
        B_A = -1*p1[0]/p1[1] #Slope over intercept
        BA_Data.append(B_A) #Creating the  BA_Data array
    
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
print('Array:', BA_Data)
#This Section Will Average the three values for BA_DATA
BA_newData = []
Val = 0
newFlow = []

stand_dev = []

for l in range(0, int(len(BA_Data)/3), 1):
    total = 0
    newFlow.append(flowVelocity[l*3])
    for i in range(0, Num_File, 1):
        total += BA_Data[Val]
        Val += 1
    average = total/Num_File
    BA_newData.append(average)

    #Standard Deviation
    sum = (BA_Data[l*3]-average)**2+(BA_Data[l*3+1]-average)**2+(BA_Data[l*3+2]-average)**2
    stand_dev.append(math.sqrt((1/(Num_File-1))*sum))




flowVelocity = newFlow

#########################


p2, residuals, _, _, _ = polyfit(flowVelocity,BA_newData,1, full=True)


fig = plt.figure()
ax1 = fig.add_subplot()
ax2 = ax1.twinx()

color = 'tab:blue'

ax1.set_xlabel('Flow Velocity (m/s)')
ax1.set_ylabel('-B/A', color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax1.plot(flowVelocity, polyval(p2,flowVelocity), label='Linear fit', color = "black", linewidth = 3)
ax1.plot(flowVelocity, BA_newData, 'bo--', color=color, label='Flow Data')

ax1.errorbar(flowVelocity, BA_newData, xerr=getFlowVel(OscErrorCCM), fmt='.k')
ax1.errorbar(flowVelocity, BA_newData, yerr= stand_dev, fmt='.k')
color = 'tab:red'

ax2.set_ylabel('Reynolds Number', color=color)  # we already handlNed the x-label with ax1
ax2.plot(flowVelocity, reynolds(flowVelocity), color=color, label='Reynolds Number')
ax2.tick_params(axis='y', labelcolor=color)

#plt.title("2.26MHz at 0 degrees flow measurements | Summing over 1 point")
fig.tight_layout()  # otherwise the right y-label is slightly clipped
fig.legend(loc='lower right', bbox_to_anchor=(0.83, 0.15), frameon=False)
plt.show()

#Fourier Transform

##Error Analysis
slope, intercept, r_value, p_value, std_err = stats.linregress(flowVelocity,BA_newData)

print("______________________________________________________________")
print("Acq_ time: %s"%dic["acq_time"])
print("Acq_ Points: %s"%dic["acq_points"])
print("R Squared : %s"%r_value)

print("P Value : %s"%p_value)
print("Standard Error: %s"%std_err)
print("SLOPE:", slope)