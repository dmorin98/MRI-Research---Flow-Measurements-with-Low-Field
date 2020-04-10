NoiseSum = NoiseSum/NoisePoints

        #Finding Highest Point value
        High = 0

        for value in range(0,len(magnitudeY),1):
            if(int(magnitudeY[value]) > High):
                High = int(magnitudeY[value])
                #print('Highest val:', High)