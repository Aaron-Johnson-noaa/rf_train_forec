import numpy as np
#predtypes:
#1: mean-max single time 
#2: mean-min single time
#3: mean-mean single time
#4: z500 special case
#5: max-max hourly max
#6: mean-max hourly max

def getpredvectors(allpredictors,predtype):

  predvectors=[[],[],[],[],[],[],[]]

  for ipred in range(len(predtype)):

    if predtype[ipred]==1:
        tempvector=[]
        for itime in range(11,36):
            tempvector.append(np.mean(allpredictors[ipred,:,itime]))
        predvectors[0].append(np.max(tempvector))

        tempvector=[]
        for itime in range(11,16):
            tempvector.append(np.mean(allpredictors[ipred,:,itime]))
        predvectors[1].append(np.max(tempvector))

        tempvector=[]
        for itime in range(15,20):
            tempvector.append(np.mean(allpredictors[ipred,:,itime]))
        predvectors[2].append(np.max(tempvector))

        tempvector=[]
        for itime in range(19,24):
            tempvector.append(np.mean(allpredictors[ipred,:,itime]))
        predvectors[3].append(np.max(tempvector))

        tempvector=[]
        for itime in range(23,28):
            tempvector.append(np.mean(allpredictors[ipred,:,itime]))
        predvectors[4].append(np.max(tempvector))

        tempvector=[]
        for itime in range(27,32):
            tempvector.append(np.mean(allpredictors[ipred,:,itime]))
        predvectors[5].append(np.max(tempvector))

        tempvector=[]
        for itime in range(31,36):
            tempvector.append(np.mean(allpredictors[ipred,:,itime]))
        predvectors[6].append(np.max(tempvector))

    elif predtype[ipred]==2:

        tempvector=[]
        for itime in range(11,36):
            tempvector.append(np.mean(allpredictors[ipred,:,itime]))
        predvectors[0].append(np.min(tempvector))
    
        tempvector=[]
        for itime in range(11,16):
            tempvector.append(np.mean(allpredictors[ipred,:,itime]))
        predvectors[1].append(np.min(tempvector))

        tempvector=[]
        for itime in range(15,20):
            tempvector.append(np.mean(allpredictors[ipred,:,itime]))
        predvectors[2].append(np.min(tempvector))

        tempvector=[]
        for itime in range(19,24):
            tempvector.append(np.mean(allpredictors[ipred,:,itime]))
        predvectors[3].append(np.min(tempvector))

        tempvector=[]
        for itime in range(23,28):
            tempvector.append(np.mean(allpredictors[ipred,:,itime]))
        predvectors[4].append(np.min(tempvector))

        tempvector=[]
        for itime in range(27,32):
            tempvector.append(np.mean(allpredictors[ipred,:,itime]))
        predvectors[5].append(np.min(tempvector))

        tempvector=[]
        for itime in range(31,36):
            tempvector.append(np.mean(allpredictors[ipred,:,itime]))
        predvectors[6].append(np.min(tempvector))

    elif predtype[ipred]==3:

        tempvector=[]
        for itime in range(11,36):
            tempvector.append(np.mean(allpredictors[ipred,:,itime]))
        predvectors[0].append(np.mean(tempvector))
    
        tempvector=[]
        for itime in range(11,16):
            tempvector.append(np.mean(allpredictors[ipred,:,itime]))
        predvectors[1].append(np.mean(tempvector))

        tempvector=[]
        for itime in range(15,20):
            tempvector.append(np.mean(allpredictors[ipred,:,itime]))
        predvectors[2].append(np.mean(tempvector))

        tempvector=[]
        for itime in range(19,24):
            tempvector.append(np.mean(allpredictors[ipred,:,itime]))
        predvectors[3].append(np.mean(tempvector))

        tempvector=[]
        for itime in range(23,28):
            tempvector.append(np.mean(allpredictors[ipred,:,itime]))
        predvectors[4].append(np.mean(tempvector))

        tempvector=[]
        for itime in range(27,32):
            tempvector.append(np.mean(allpredictors[ipred,:,itime]))
        predvectors[5].append(np.mean(tempvector))

        tempvector=[]
        for itime in range(31,36):
            tempvector.append(np.mean(allpredictors[ipred,:,itime]))
        predvectors[6].append(np.mean(tempvector))

    elif predtype[ipred]==4:

        tempvector=[]
        tempvector2=[]
        for itime in range(11,36):
            tempvector.append(np.mean(allpredictors[ipred,:,itime]))
            tempvector2.append(np.mean(allpredictors[ipred,:,itime-12]))
        predvectors[0].append(np.mean(tempvector)-np.mean(tempvector2))
    
        tempvector=[]
        tempvector2=[]
        for itime in range(11,16):
            tempvector.append(np.mean(allpredictors[ipred,:,itime]))
            tempvector2.append(np.mean(allpredictors[ipred,:,itime-12]))
        predvectors[1].append(np.mean(tempvector)-np.mean(tempvector2))

        tempvector=[]
        tempvector2=[]
        for itime in range(15,20):
            tempvector.append(np.mean(allpredictors[ipred,:,itime]))
            tempvector2.append(np.mean(allpredictors[ipred,:,itime-12]))
        predvectors[2].append(np.mean(tempvector)-np.mean(tempvector2))

        tempvector=[]
        tempvector2=[]
        for itime in range(19,24):
            tempvector.append(np.mean(allpredictors[ipred,:,itime]))
            tempvector2.append(np.mean(allpredictors[ipred,:,itime-12]))
        predvectors[3].append(np.mean(tempvector)-np.mean(tempvector2))

        tempvector=[]
        tempvector2=[]
        for itime in range(23,28):
            tempvector.append(np.mean(allpredictors[ipred,:,itime]))
            tempvector2.append(np.mean(allpredictors[ipred,:,itime-12]))
        predvectors[4].append(np.mean(tempvector)-np.mean(tempvector2))

        tempvector=[]
        tempvector2=[]
        for itime in range(27,32):
            tempvector.append(np.mean(allpredictors[ipred,:,itime]))
            tempvector2.append(np.mean(allpredictors[ipred,:,itime-12]))
        predvectors[5].append(np.mean(tempvector)-np.mean(tempvector2))

        tempvector=[]
        tempvector2=[]
        for itime in range(31,36):
            tempvector.append(np.mean(allpredictors[ipred,:,itime]))
            tempvector2.append(np.mean(allpredictors[ipred,:,itime-12]))
        predvectors[6].append(np.mean(tempvector)-np.mean(tempvector2))

    elif predtype[ipred]==5:

        tempvector=[]
        for itime in range(12,36):
            tempvector.append(np.max(allpredictors[ipred,:,itime]))
        predvectors[0].append(np.max(tempvector))
    
        tempvector=[]
        for itime in range(12,16):
            tempvector.append(np.max(allpredictors[ipred,:,itime]))
        predvectors[1].append(np.max(tempvector))

        tempvector=[]
        for itime in range(16,20):
            tempvector.append(np.max(allpredictors[ipred,:,itime]))
        predvectors[2].append(np.max(tempvector))

        tempvector=[]
        for itime in range(20,24):
            tempvector.append(np.max(allpredictors[ipred,:,itime]))
        predvectors[3].append(np.max(tempvector))

        tempvector=[]
        for itime in range(24,28):
            tempvector.append(np.max(allpredictors[ipred,:,itime]))
        predvectors[4].append(np.max(tempvector))

        tempvector=[]
        for itime in range(28,32):
            tempvector.append(np.max(allpredictors[ipred,:,itime]))
        predvectors[5].append(np.max(tempvector))

        tempvector=[]
        for itime in range(32,36):
            tempvector.append(np.max(allpredictors[ipred,:,itime]))
        predvectors[6].append(np.max(tempvector))

    elif predtype[ipred]==6:

        tempvector=[]
        for itime in range(12,36):
            tempvector.append(np.mean(allpredictors[ipred,:,itime]))
        predvectors[0].append(np.max(tempvector))
    
        tempvector=[]
        for itime in range(12,16):
            tempvector.append(np.mean(allpredictors[ipred,:,itime]))
        predvectors[1].append(np.max(tempvector))

        tempvector=[]
        for itime in range(16,20):
            tempvector.append(np.mean(allpredictors[ipred,:,itime]))
        predvectors[2].append(np.max(tempvector))

        tempvector=[]
        for itime in range(20,24):
            tempvector.append(np.mean(allpredictors[ipred,:,itime]))
        predvectors[3].append(np.max(tempvector))

        tempvector=[]
        for itime in range(24,28):
            tempvector.append(np.mean(allpredictors[ipred,:,itime]))
        predvectors[4].append(np.max(tempvector))

        tempvector=[]
        for itime in range(28,32):
            tempvector.append(np.mean(allpredictors[ipred,:,itime]))
        predvectors[5].append(np.max(tempvector))

        tempvector=[]
        for itime in range(32,36):
            tempvector.append(np.mean(allpredictors[ipred,:,itime]))
        predvectors[6].append(np.max(tempvector))

    else:
        print('UNDEFINED predtype '+str(predtype[ipred]))
        exit()







  return predvectors

