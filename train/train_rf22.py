import numpy as np
import numpy.ma as ma 
import math
from netCDF4 import Dataset
import sys, os

import scipy.ndimage as ndimage
import pickle
import time
from sklearn import preprocessing
 
from sklearn.ensemble import RandomForestClassifier

import getseveres,getpredvectors
import getvarlist


####################################################
#   BEGIN EXECUTABLE CODE ##########################
####################################################

outputfile = str(sys.argv[1])
skipcase = str(sys.argv[2])
whichtime = int(sys.argv[3])
whichvar = int(sys.argv[4])
username = str(sys.argv[5])


ny=64
nx=92

path2019='/scratch/'+username+'/prep2022/'

#dates2019=['20190430','20190501','20190502','20190503','20190506','20190507','20190508','20190509','20190510','20190513','20190514','20190515','20190516','20190518','20190520','20190521','20190522','20190523','20190524','20190527','20190528','20190529','20190530','20190531','20210427','20210428','20210430','20210503','20210504','20210505','20210506','20210507','20210510','20210511','20210512','20210513','20210514','20210517','20210519','20210520','20210521','20210524','20210525','20210526','20210527','20210528','20210531','20210601','20210602','20210603','20210604']

dates2019=['20220428','20220429','20220502','20220503','20220504','20220505','20220506','20220509','20220510','20220511','20220512','20220513','20220516','20220517','20220518','20220519','20220520','20220523','20220524','20220525','20220526','20220527','20220531','20220601','20220602','20220603']

trainingvector=[]
targetvector=[]

varlist,vartypelist = getvarlist.setvars(whichvar,whichtime)


for icase in range(len(dates2019)): 
 if skipcase != dates2019[icase]:
 #if skipcase != icase:
  ensvars=np.zeros((len(vartypelist),10,36,ny,nx))

  for imem in range(10):
    smem="%03d"%(imem+1) 
    thisdate=dates2019[icase]
    print(path2019+dates2019[icase]+'_'+smem+'.nc')
    nc=Dataset(path2019+dates2019[icase]+'_'+smem+'.nc')


    if imem == 0:
      lat=nc.variables['lat'][:,:]
      lon=nc.variables['lon'][:,:]
      nc2=Dataset('/scratch/'+username+'/rpts2022/'+thisdate+'.nc')
      wind_rpt=nc2.variables['wind'][:,:,:]
      hail_rpt=nc2.variables['hail'][:,:,:]
      tor_rpt=nc2.variables['tor'][:,:,:]
      sigwind_rpt=nc2.variables['sigwind'][:,:,:]
      sighail_rpt=nc2.variables['sighail'][:,:,:]
      sigtor_rpt=nc2.variables['sigtor'][:,:,:]
      mask=nc2.variables['mask'][:,:]
 
    for ipred in range(len(varlist)):
      if varlist[ipred]=='lat':
        for it in range(36):
          ensvars[ipred,imem,it,:,:]=lat[:,:]
      elif varlist[ipred]=='lon':
        for it in range(36):
          ensvars[ipred,imem,it,:,:]=lon[:,:]
      else:
        ensvars[ipred,imem,:,:,:]=nc.variables[varlist[ipred]][:,:,:]
   

  for j in range(ny):
    for i in range(nx):
      if mask[j,i] > 0.0 and (not np.isnan(ensvars[0,0,0,j,i])):
        print([j,i])
      #if mask[j,i] > 0.0 and ensvars[10,0,0,j,i] > 0.0 :

        allsevere,windsevere,sigwindsevere,hailsevere,sighailsevere,torsevere,sigtorsevere = getseveres.getseveres(wind_rpt[:,j,i],sigwind_rpt[:,j,i],hail_rpt[:,j,i],sighail_rpt[:,j,i],tor_rpt[:,j,i],sigtor_rpt[:,j,i])

        if whichvar == 0:
          targetvector.append(allsevere[whichtime])
        if whichvar == 1:
          targetvector.append(windsevere[whichtime])
        if whichvar == 2:
          targetvector.append(sigwindsevere[whichtime])
        if whichvar == 3:
          targetvector.append(hailsevere[whichtime])
        if whichvar == 4:
          targetvector.append(sighailsevere[whichtime])
        if whichvar == 5:
          targetvector.append(torsevere[whichtime])
        if whichvar == 6:
          targetvector.append(sigtorsevere[whichtime])
        if whichvar == 7:
          targetvector.append(max([sigwindsevere[whichtime],sighailsevere[whichtime],sigtorsevere[whichtime]]))

        predtype=[]
        allpredictors=[]
        for ipred in range(len(varlist)):
            allpredictors.append(ensvars[ipred,:,:,j,i])
            predtype.append(vartypelist[ipred])

        

        predvectors=getpredvectors.getpredvectors(np.asarray(allpredictors),predtype)
        trainingvector.append(predvectors[whichtime])




scaler = preprocessing.StandardScaler().fit(trainingvector)
#scaledvector = scaler.transform(trainingvector)
scaledvector = trainingvector #scaler.transform(trainingvector)

#for i in range(len(trainingvector)):
#  print([trainingvector[i],scaledvector[i]]) 

randForest = RandomForestClassifier(n_estimators=100,max_depth=10, criterion='entropy',min_samples_leaf=30,max_features='auto',max_samples=0.25,oob_score=True) 


randForest.fit(np.asarray(scaledvector),np.asarray(targetvector))
pickle.dump(randForest, open(outputfile, 'wb'))
pickle.dump(scaler, open(outputfile+'.scale', 'wb'))
