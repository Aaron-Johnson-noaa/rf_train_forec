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

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap, addcyclic
from mpl_toolkits.axes_grid import make_axes_locatable
import matplotlib.axes as maxes

import getseveres,getpredvectors,outputs
import outputfig
import getvarlist

####################################################
#   BEGIN EXECUTABLE CODE ##########################
####################################################

inmodel = str(sys.argv[1])
icase = str(sys.argv[2])
outfile = str(sys.argv[3])
whichtime = int(sys.argv[4])
whichvar = int(sys.argv[5])

ny=64
nx=92


scaler = pickle.load(open(inmodel+'.scale', 'rb'))
randForest = pickle.load(open(inmodel, 'rb'))

path2019='/scratch/ajohns14/prep2022/'
forecprob=np.zeros((ny,nx))

severeprob=np.zeros((ny,nx))

forecprob[:,:]=np.nan

severeprob[:,:]=np.nan

varlist,vartypelist = getvarlist.setvars(whichvar,whichtime)

ensvars=np.zeros((len(vartypelist),10,36,ny,nx))


for imem in range(10):
    smem="%03d"%(imem+1) 
    print(path2019+icase+'_'+smem+'.nc')
    nc=Dataset(path2019+icase+'_'+smem+'.nc')
 



    if imem == 0:
      lat=nc.variables['lat'][:,:]
      lon=nc.variables['lon'][:,:]
      nc2=Dataset('/scratch/ajohns14/rpts2022/'+icase+'.nc') #
      wind_rpt=nc2.variables['wind'][:,:,:]
      hail_rpt=nc2.variables['hail'][:,:,:]
      tor_rpt=nc2.variables['tor'][:,:,:]
      sigwind_rpt=nc2.variables['sigwind'][:,:,:]
      sighail_rpt=nc2.variables['sighail'][:,:,:]
      sigtor_rpt=nc2.variables['sigtor'][:,:,:]
      mask=nc2.variables['mask'][:,:] #

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
      if ensvars[10,0,0,j,i] > 0.0:   #adding lat lon bounds here limits domain over which forecast is calculate
 
        allsevere,windsevere,sigwindsevere,hailsevere,sighailsevere,torsevere,sigtorsevere = getseveres.getseveres(wind_rpt[:,j,i],sigwind_rpt[:,j,i],hail_rpt[:,j,i],sighail_rpt[:,j,i],tor_rpt[:,j,i],sigtor_rpt[:,j,i]) #
 
        if whichvar == 0:
          severeprob[j,i]=allsevere[whichtime]
        if whichvar == 1:
          severeprob[j,i]=windsevere[whichtime]
        if whichvar == 2:
          severeprob[j,i]=sigwindsevere[whichtime]
        if whichvar == 3:
          severeprob[j,i]=hailsevere[whichtime]
        if whichvar == 4:
          severeprob[j,i]=sighailsevere[whichtime]
        if whichvar == 5:
          severeprob[j,i]=torsevere[whichtime]
        if whichvar == 6:
          severeprob[j,i]=sigtorsevere[whichtime]
        if whichvar == 7:
          severeprob[j,i]=max([sigwindsevere[whichtime],sighailsevere[whichtime],sigtorsevere[whichtime]]) #

        #print([j,i,severeprob[j,i]])

        predtype=[]
        allpredictors=[]
        for ipred in range(len(varlist)):
            allpredictors.append(ensvars[ipred,:,:,j,i])
            predtype.append(vartypelist[ipred])



        predvectors=getpredvectors.getpredvectors(np.asarray(allpredictors),predtype)


        #scaledvector = scaler.transform([predvectors[whichtime]])
        scaledvector = [predvectors[whichtime]] #scaler.transform([predvectors[whichtime]])

     #   for ijk in range(len(predvectors[whichtime])):
     #     print(predvectors[whichtime][ijk])
             
        returnval=randForest.predict_proba(scaledvector)

#        if j > 25 and j < 35 and i > 50 and i < 60: #!@#
        if len(returnval[0]) > 1:
          forecprob[j,i]=returnval[0,1]
        else:
          forecprob[j,i]=0.0      

#        print(forecprob[j,i])
#        print('======')

#        if j > 25 and j < 35 and i > 50 and i < 60:       
        #print([i,j,forecprob[j,i],severeprob[j,i]])
          #print(predvectors[whichtime])
 
 
bs=0.0 
bsref=0.0 
obar=0.0 
ntotal=0.0 
tablebsnum=np.zeros((101))
tableobar=np.zeros((101))

roc_d=0.0 
roc_d2=0.0
roc_hits=np.zeros((1001))
roc_fa=np.zeros((1001))

for j in range(ny):
  for i in range(nx):
    if mask[j,i] > 0: #adding lat lon bounds here only limits domain over which verification is done for the bs.txt file

      if not np.isnan(forecprob[j,i]): 
        bsindex=int(100.0*forecprob[j,i])
      else:
        bsindex=0
      tablebsnum[bsindex]=tablebsnum[bsindex]+1.0
      tableobar[bsindex]=tableobar[bsindex]+severeprob[j,i]
      ntotal=ntotal+1.0
      if severeprob[j,i] >= 0.5:
        obar=obar+1.0
        roc_d=roc_d+1.0
      else:
        roc_d2=roc_d2+1.0

obar=obar/ntotal

for fbin in range(101):
  if tablebsnum[fbin] > 0:
    tableobar[fbin]=tableobar[fbin]/tablebsnum[fbin]

for j in range(ny):
  for i in range(nx):
    if mask[j,i] > 0: #also need to set the same lat lon bounds here as for the first verification part
      if severeprob[j,i] >= 0.5:
        bsref=bsref+(obar-1.0)*(obar-1.0)
        bs=bs+(forecprob[j,i]-1.0)*(forecprob[j,i]-1.0)
        for iroc in range(1001):
          if forecprob[j,i] >= float(iroc)/1000.0:
            roc_hits[iroc]=roc_hits[iroc]+1.0
      else:
        bsref=bsref+obar*obar
        bs=bs+forecprob[j,i]*forecprob[j,i]
        for iroc in range(1001):
          if forecprob[j,i] >= float(iroc)/1000.0:
            roc_fa[iroc]=roc_fa[iroc]+1.0


bsref=bsref/ntotal
bs=bs/ntotal

nextoutfile=outfile+'.data.txt'
f=open(nextoutfile,"w")
for j in range(ny):
  for i in range(nx):
    if mask[j,i] > 0: 
      f.write('%f %f \n' % (forecprob[j,i],severeprob[j,i]))
f.close()

nextoutfile=outfile+'.txt'
outputs.textoutput(bs,bsref,ntotal,roc_d,roc_d2,roc_fa[:],roc_hits[:],tablebsnum[:],tableobar[:],nextoutfile)

nextoutfile=outfile+'.png'
#outputs.plotoutputnew(lon,lat,severeprob[:,:],forecprob[:,:],nextoutfile,whichvar,'NOT FLOW DEPENDENT')
#outputfig.plotfig10(lon,lat,severeprob[:,:],forecprob[:,:],nextoutfile,whichvar)
#outputfig.plotfig12(lon,lat,severeprob[:,:],forecprob[:,:],nextoutfile,whichvar)
outputfig.plotfig2(lon,lat,severeprob[:,:],forecprob[:,:],nextoutfile,whichvar,icase)







