import numpy as np
import matplotlib.pyplot as plt
import nmrglue as ng
from scipy import optimize
from numpy import polyval, polyfit
import math
import os
from scipy import stats

phase = False
Num_File = 1
PeakSum = 1
starting_point = 27 #High AMP 27, Low AMP 11
peaks = 4


OscError = 4 #+/- Hz uncertainty on the oscilliscope for measuring flow velocity
diam_tube = 0.0075 #m
density_fluid = 995 #kg/m^3
viscocity = 0.001054 #of fluid (kg/ms)

font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 15}	
plt.rc('font', **font)


flowVelocity = [] #Array that stores the flow velocities
BA_Data = [] #This is the value of B/A (Slope/Intersept)
OscErrorCCM = OscError*15/2
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
        realY = []
        imagY = []
        timeX = []

        i = 0
        time = 0
        increment_point = int(dic["acq_points"]*2)
        
        if phase == True:
            while (i<data.size):
                magnitudeY.append(math.atan2(data[i].imag, data[i].real))
                
                i += 1
                time += float(dic["acq_time"]/dic["acq_points"])
                timeX.append(time)

            InterpolationX = [] 
            InterpolationY = [] 
            for i in range(0, peaks):
                plotPeaks()
            plt.plot(InterpolationX, InterpolationY, label= ("%s peaks data" % peaks))
            slope, intercept = polyfit(InterpolationX,InterpolationY,1)
            p1 = polyfit(InterpolationX,InterpolationY,1)
            print('SLOPE:,', slope)



        else:

            while (i<data.size):
                magnitudeY.append(math.sqrt((float(data[i].imag))**2+(float(data[i].real))**2))
                imagY.append((float(data[i].imag)))
                realY.append((float(data[i].real)))
                i += 1
                time += float(dic["acq_time"]/dic["acq_points"])
                timeX.append(time)
            #######################################################################################
            # This part of the code will create the linear fit
            

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
        if phase == False:
            plt.subplot(3,1,1)
            plt.plot(timeX, magnitudeY, label='Magnitude')
            plt.plot(InterpolationX, InterpolationY, label= ("%s peaks data" % peaks))
            plt.title("Flow Velocity of: %s CCM" % flowFile[5:9])
            plt.legend()
            plt.subplot(3,1,2)
            plt.plot(timeX, realY, label='Real')
            plt.legend()
            plt.subplot(3,1,3)
            plt.plot(timeX, imagY, label='Imag')
            plt.legend()

        plt.xlabel("Time (sec)")
        plt.ylabel("Magnitude (Arbitrary)")
        if phase == True:
            plt.ylim((-math.pi), (math.pi))

        

        plt.show()


    else:
        print('File found but not .tnt format')
        continue

plt.close()
#This Section Will Average the three values for BA_DATA
BA_newData = []
Val = 0
newFlow = []

stand_dev = []
temp = []
if Num_File > 1:
    for l in range(0, int(len(BA_Data)/3), 1):
        total = 0
        newFlow.append(flowVelocity[l*3])
        for i in range(0, Num_File, 1):
            total += BA_Data[Val]
            temp.append(BA_Data[Val])
            Val += 1
        average = total/Num_File
        BA_newData.append(average)

        #Standard Deviation
        stand_dev.append(np.std(temp))
        temp = []
else:
    BA_newData = BA_Data
    newFlow = flowVelocity

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
ax1.plot(flowVelocity, BA_newData, 'bo--', color=color, label='Flow Data', linewidth = 3)

ax1.errorbar(flowVelocity, BA_newData, xerr=getFlowVel(OscErrorCCM), fmt='.k')
if Num_File > 1:
    ax1.errorbar(flowVelocity, BA_newData, yerr= stand_dev, fmt='.k')
    
color = 'tab:red'
###Extrapolating Reynolds


flowVelocity.insert(0, 0)
print('LEN OF X:', len(flowVelocity))
print('LEN OF Y:', len(reynolds(flowVelocity)))
ax2.set_ylabel('Reynolds Number', color=color)  # we already handlNed the x-label with ax1
ax2.plot(flowVelocity, reynolds(flowVelocity), color=color, label='Reynolds Number', linestyle='-.', linewidth = 3)
ax2.tick_params(axis='y', labelcolor=color)

#plt.title("2.26MHz at 0 degrees flow measurements | Summing over 1 point")
fig.tight_layout()  # otherwise the right y-label is slightly clipped
fig.legend(loc='lower right', bbox_to_anchor=(0.83, 0.15), frameon=False)
plt.show()

#Fourier Transform

##Error Analysis
print(flowVelocity)
print(BA_newData)
slope, intercept, r_value, p_value, std_err = stats.linregress(flowVelocity, BA_newData)

print("______________________________________________________________")
print("Acq_ time: %s"%dic["acq_time"])
print("Acq_ Points: %s"%dic["acq_points"])
print("R Squared : %s"%r_value)

print("P Value : %s"%p_value)
print("Standard Error: %s"%std_err)
print("SLOPE:", slope)