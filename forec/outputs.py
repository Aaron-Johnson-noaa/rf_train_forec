import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap, addcyclic
from mpl_toolkits.axes_grid import make_axes_locatable
import matplotlib.axes as maxes

import numpy as np

def textoutput(bs,bsref,ntotal,roc_d,roc_d2,roc_fa,roc_hits,tablebsnum,tableobar,outfile):
  f=open(outfile,"w")
  f.write('%f %f %f \n' % (bs,bsref,ntotal))
  f.write('%f %f \n' % (roc_d,roc_d2))
  for i in range(1001):
    tbin=(float(i)/1000.0)
    f.write('%f %f %f \n' % (tbin,roc_fa[i],roc_hits[i]))
  for i in range(101):
    fbin=(float(i)/100.0)
    f.write('%f %f %f \n' % (fbin,tablebsnum[i],tableobar[i]))
  f.close()
    
def plotoutputdiff(lon,lat,severeprob,forecprob,forecprob2,outfile,isev,titlestr):
#def plotoutput(lon,lat,severeprob,forecprob,outfile,titlestr):
  import pygrib as grb
  import scipy.ndimage as ndimage
  from netCDF4 import Dataset
  from matplotlib.colors import BoundaryNorm
#912,1508  fin=grb.open('/scratch/ajohns14/20190521/fv3lam_hord5_mem0/2019052100/postprd/rrfs.t00z.bgdawpf001.tm00.grib2')
  fin = grb.open('/ourdisk/hpc/map/HWT_2022/radVTS/LAMprod_20220509000000/member001/radVTS01_202205090000f004.grib2')
  #fin = grb.open('/ourdisk/hpc/map/HWT_2021/HWT_MAP_ensemble1/GSI_20210510000000/member001/map2-hybrid01_202105100000f001.grib2')
  #fin = grb.open('/scratch/ajohns14/HWT_test_20210412/LAMprod_202104120000/member001/map-hybrid01_202104120000f001.grib2')
#  apcp_msg_f=fin.select()[856]
  apcp_msg_f=fin.select()[872]

  nxin=92
  nyin=64
  nxout=1799 #1746
  nyout=1059 #1014
 
  #radius=18 #18
  radius=27 #18
  #radius=36 #18


  m=Basemap(resolution='i',projection='lcc',width=5000000,height=3500000,lat_0=38.5,lon_0=-97.5,lat_1=36.0,lat_2=36.0)
  x,y=m(lon,lat)

  width=10; height=8
  plt.figure(figsize=(width,height))
  m.drawstates(color='k')
  m.drawcoastlines(color='k')
  m.drawcountries(color='k')


  LEVS_rpt=np.arange(1.0,10.0,10)

  wrfplot=plt.contour(x,y,severeprob,LEVS_rpt,colors='red')

  forecprobdiff=forecprob-forecprob2 #atj
  #atj forecprobsm=ndimage.gaussian_filter(forecprob,sigma=1)
  forecprobdiffsm=ndimage.gaussian_filter(forecprobdiff,sigma=1) #atj

  LEVS=np.arange(-0.1,0.105,0.005) #atj

  wrfplot2=plt.contourf(x,y,forecprobdiffsm,LEVS,cmap='bwr',extend='both') #atj

  plt.title('%s' % (titlestr), \
                fontsize=20,bbox=dict(facecolor='white', alpha=1.0),\
                x=0.5,y=.95,weight = 'demibold',style='oblique', \
                stretch='normal', family='sans-serif')


  F = plt.gcf()
  ax = plt.gca()  # Gets the current axes                                                                                                          
  divider = make_axes_locatable(ax)  # Lets us move axes around                                                                                    
  cax = divider.append_axes("right", size="2%",pad=0.23) #,axes_class=maxes.Axes) # Adds an axis for the colorbar                                    
  F.add_axes(cax)  # Adds the new axis to the figure as the current working axis                            
  bar = plt.colorbar(wrfplot2,cax=cax,orientation='vertical',format='%4.2f')
  bar.ax.tick_params(labelsize=20)
  plt.tight_layout()
  plt.savefig(outfile,format='png',bbox_inches='tight',dpi=100)
  plt.clf()
  plt.cla()
  plt.close('all')
    
def plotoutputreg(lon,lat,severeprob,forecprob,outfile,isev,titlestr):
#def plotoutput(lon,lat,severeprob,forecprob,outfile,titlestr):
  import pygrib as grb
  import scipy.ndimage as ndimage
  from netCDF4 import Dataset
  from matplotlib.colors import BoundaryNorm
#912,1508  fin=grb.open('/scratch/ajohns14/20190521/fv3lam_hord5_mem0/2019052100/postprd/rrfs.t00z.bgdawpf001.tm00.grib2')
  fin = grb.open('/ourdisk/hpc/map/HWT_2022/radVTS/LAMprod_20220509000000/member001/radVTS01_202205090000f004.grib2')
  #fin = grb.open('/ourdisk/hpc/map/HWT_2021/HWT_MAP_ensemble1/GSI_20210510000000/member001/map2-hybrid01_202105100000f001.grib2')
  #fin = grb.open('/scratch/ajohns14/HWT_test_20210412/LAMprod_202104120000/member001/map-hybrid01_202104120000f001.grib2')
#  apcp_msg_f=fin.select()[856]
  apcp_msg_f=fin.select()[872]

  nxin=92
  nyin=64
  nxout=1799 #1746
  nyout=1059 #1014
 

  #radius=18 #18
  radius=27 #18
  #radius=36 #18


  m=Basemap(resolution='i',projection='lcc',width=5000000,height=3500000,lat_0=38.5,lon_0=-97.5,lat_1=36.0,lat_2=36.0)
  x,y=m(lon,lat)

  width=10; height=8
  plt.figure(figsize=(width,height))
  m.drawstates(color='k')
  m.drawcoastlines(color='k')
  m.drawcountries(color='k')


  LEVS_rpt=np.arange(1.0,10.0,10)

  wrfplot=plt.contour(x,y,severeprob,LEVS_rpt,colors='red')

  #LEVS=np.arange(0.05,1.05,0.05)
  #LEVS=np.arange(0.02,0.335,0.015)
  #wrfplot2=plt.contourf(x,y,forecprob,LEVS,cmap='jet',extend='max')

  forecprobsm=ndimage.gaussian_filter(forecprob,sigma=1)


  LEVS=np.arange(0.02,2.02,0.05)

  wrfplot2=plt.contourf(x,y,forecprobsm,LEVS,cmap='jet',extend='max')

  plt.title('%s' % (titlestr), \
                fontsize=20,bbox=dict(facecolor='white', alpha=1.0),\
                x=0.5,y=.95,weight = 'demibold',style='oblique', \
                stretch='normal', family='sans-serif')


  F = plt.gcf()
  ax = plt.gca()  # Gets the current axes                                                                                                          
  divider = make_axes_locatable(ax)  # Lets us move axes around                                                                                    
  cax = divider.append_axes("right", size="2%",pad=0.23) #,axes_class=maxes.Axes) # Adds an axis for the colorbar                                    
  F.add_axes(cax)  # Adds the new axis to the figure as the current working axis                            
  bar = plt.colorbar(wrfplot2,cax=cax,orientation='vertical',format='%4.2f')
  bar.ax.tick_params(labelsize=20)
  plt.tight_layout()
  plt.savefig(outfile,format='png',bbox_inches='tight',dpi=100)
  plt.clf()
  plt.cla()
  plt.close('all')
   
def plotoutputnew(lon,lat,severeprob,forecprob,outfile,isev,titlestr):
#def plotoutput(lon,lat,severeprob,forecprob,outfile,titlestr):
  import pygrib as grb
  import scipy.ndimage as ndimage
  from netCDF4 import Dataset
  from matplotlib.colors import BoundaryNorm
#912,1508  fin=grb.open('/scratch/ajohns14/20190521/fv3lam_hord5_mem0/2019052100/postprd/rrfs.t00z.bgdawpf001.tm00.grib2')
  fin = grb.open('/ourdisk/hpc/map/HWT_2022/radVTS/LAMprod_20220509000000/member001/radVTS01_202205090000f004.grib2')
  #fin = grb.open('/ourdisk/hpc/map/HWT_2021/HWT_MAP_ensemble1/GSI_20210510000000/member001/map2-hybrid01_202105100000f001.grib2')
  #fin = grb.open('/scratch/ajohns14/HWT_test_20210412/LAMprod_202104120000/member001/map-hybrid01_202104120000f001.grib2')
#  apcp_msg_f=fin.select()[856]
  apcp_msg_f=fin.select()[872]

  nxin=92
  nyin=64
  nxout=1799 #1746
  nyout=1059 #1014
 

  #radius=18 #18
  radius=27 #18
  #radius=36 #18


  m=Basemap(resolution='i',projection='lcc',width=5000000,height=3500000,lat_0=38.5,lon_0=-97.5,lat_1=36.0,lat_2=36.0)
  x,y=m(lon,lat)

  width=10; height=8
  plt.figure(figsize=(width,height))
  m.drawstates(color='k')
  m.drawcoastlines(color='k')
  m.drawcountries(color='k')


  LEVS_rpt=np.arange(1.0,10.0,10)

  wrfplot=plt.contour(x,y,severeprob,LEVS_rpt,colors='red')

  #LEVS=np.arange(0.05,1.05,0.05)
  #LEVS=np.arange(0.02,0.335,0.015)
  #wrfplot2=plt.contourf(x,y,forecprob,LEVS,cmap='jet',extend='max')

  forecprobsm=ndimage.gaussian_filter(forecprob,sigma=1)


  LEVS=np.arange(0.02,0.62,0.02)

  wrfplot2=plt.contourf(x,y,forecprobsm,LEVS,cmap='jet',extend='max')

  plt.title('%s' % (titlestr), \
                fontsize=20,bbox=dict(facecolor='white', alpha=1.0),\
                x=0.5,y=.95,weight = 'demibold',style='oblique', \
                stretch='normal', family='sans-serif')


  F = plt.gcf()
  ax = plt.gca()  # Gets the current axes                                                                                                          
  divider = make_axes_locatable(ax)  # Lets us move axes around                                                                                    
  cax = divider.append_axes("right", size="2%",pad=0.23) #,axes_class=maxes.Axes) # Adds an axis for the colorbar                                    
  F.add_axes(cax)  # Adds the new axis to the figure as the current working axis                            
  bar = plt.colorbar(wrfplot2,cax=cax,orientation='vertical',format='%4.2f')
  bar.ax.tick_params(labelsize=20)
  plt.tight_layout()
  plt.savefig(outfile,format='png',bbox_inches='tight',dpi=100)
  plt.clf()
  plt.cla()
  plt.close('all')
  
def plotoutput(lon,lat,severeprob,forecprob,outfile,isev,titlestr):
#def plotoutput(lon,lat,severeprob,forecprob,outfile,titlestr):
  import pygrib as grb
  import scipy.ndimage as ndimage
  from netCDF4 import Dataset
  from matplotlib.colors import BoundaryNorm
#912,1508  fin=grb.open('/scratch/ajohns14/20190521/fv3lam_hord5_mem0/2019052100/postprd/rrfs.t00z.bgdawpf001.tm00.grib2')
  fin = grb.open('/ourdisk/hpc/map/HWT_2022/radVTS/LAMprod_20220509000000/member001/radVTS01_202205090000f004.grib2')
  #fin = grb.open('/ourdisk/hpc/map/HWT_2021/HWT_MAP_ensemble1/GSI_20210510000000/member001/map2-hybrid01_202105100000f001.grib2')
  #fin = grb.open('/scratch/ajohns14/HWT_test_20210412/LAMprod_202104120000/member001/map-hybrid01_202104120000f001.grib2')
#  apcp_msg_f=fin.select()[856]
  apcp_msg_f=fin.select()[872]

  nxin=92
  nyin=64
  nxout=1799 #1746
  nyout=1059 #1014
 
  ncremap = Dataset('/home/ajohns14/rf/fv3_2022/remap/remap.nc',mode='r')
  remap_x=ncremap.variables['remap_x'][:,:]
  remap_y=ncremap.variables['remap_y'][:,:]
  
  forecproblg=np.zeros((nyout,nxout),dtype=np.float32)
  forecproblg1=np.zeros((nyout,nxout),dtype=np.float32)
  for j in range(nyout):
    for i in range(nxout):
      if forecprob[remap_y[j,i],remap_x[j,i]]>=0:
        forecproblg1[j,i]=np.float32(forecprob[remap_y[j,i],remap_x[j,i]])
      else:
        forecproblg1[j,i]=0.0 #-1.0 

  #radius=18 #18
  radius=27 #18
  #radius=36 #18
#  for j in range(nyout):
#    print(j)
#    for i in range(nxout):
#      icount=0.0
#      ival=0.0
#      for jj in range(max(0,j-radius),min(nyout,j+radius)):
#        for ii in range(max(0,i-radius),min(nxout,i+radius)):
#          if forecproblg1[jj,ii] >= 0.0:
#            icount=icount+1.0
#            ival=ival+forecproblg1[jj,ii]
#      if icount > 0.5:
#        forecproblg[j,i]=ival/icount
#      else:
#        forecproblg[j,i]=-1.0
  forecproblg = ndimage.gaussian_filter(forecproblg1,sigma=radius)
  apcp_msg_f['values']=forecproblg[:,:]


  msg_f=apcp_msg_f.tostring()
  grbout_f=open(outfile+'.grb','wb')
  grbout_f.write(msg_f)
  grbout_f.close()


  m=Basemap(resolution='i',projection='lcc',width=5000000,height=3500000,lat_0=38.5,lon_0=-97.5,lat_1=36.0,lat_2=36.0)
  x,y=m(lon,lat)

  width=10; height=8
  plt.figure(figsize=(width,height))
  m.drawstates(color='k')
  m.drawcoastlines(color='k')
  m.drawcountries(color='k')


  LEVS_rpt=np.arange(1.0,10.0,10)

#  wrfplot=plt.contour(x,y,severeprob,LEVS_rpt,colors='red')

  #LEVS=np.arange(0.05,1.05,0.05)
  #LEVS=np.arange(0.02,0.335,0.015)
  #wrfplot2=plt.contourf(x,y,forecprob,LEVS,cmap='jet',extend='max')

  forecprobsm=ndimage.gaussian_filter(forecprob,sigma=1)



  if isev==5:
    LEVS=[0.02,0.05,0.10,0.15,0.30,0.45,0.60,0.61]
    LEVSc=[0.01,0.035,0.075,0.125,0.20,0.25,0.50,0.55]
    mycmap=(matplotlib.colors.ListedColormap(['#008000','#653700','#FFD700','#FF0000','#FF00FF','#7E1E9C','#000080']))
  else:
    mycmap=(matplotlib.colors.ListedColormap(['#653700','#FFD700','#FF0000','#FF00FF','#7E1E9C']))
    LEVS=[0.05,0.15,0.30,0.45,0.60,0.70]
    LEVSc=[0.10,0.20,0.25,0.35,0.40,0.50]
 
  bnorm = BoundaryNorm(LEVS, ncolors=len(LEVS)-1, clip=True)

  wrfplot2=plt.contourf(x,y,forecprobsm,LEVS,cmap=mycmap,extend='max',norm=bnorm)
  wrfplot3=plt.contour(x,y,forecprobsm,LEVSc,colors='black',linewidths=1.0)

  plt.title('%s' % (titlestr), \
                fontsize=20,bbox=dict(facecolor='white', alpha=1.0),\
                x=0.5,y=.95,weight = 'demibold',style='oblique', \
                stretch='normal', family='sans-serif')

  plt.clabel(wrfplot3, inline=1, fontsize=8,fmt='%.2f')

  F = plt.gcf()
  ax = plt.gca()  # Gets the current axes                                                                                                          
  divider = make_axes_locatable(ax)  # Lets us move axes around                                                                                    
  cax = divider.append_axes("right", size="2%",pad=0.23) #,axes_class=maxes.Axes) # Adds an axis for the colorbar                                    
  F.add_axes(cax)  # Adds the new axis to the figure as the current working axis                            
  bar = plt.colorbar(wrfplot2,cax=cax,orientation='vertical',format='%4.2f')
  bar.ax.tick_params(labelsize=20)
  plt.tight_layout()
  plt.savefig(outfile,format='png',bbox_inches='tight',dpi=100)
  plt.clf()
  plt.cla()
  plt.close('all')
 

def plotoutputd1(lon,lat,severeprob,forecprob,outfile,titlestr,jsontime):
  import json

  jsonfile='/condo/map3/ajohns14/hwt_dd1.'+jsontime+'.json'
  with open(jsonfile) as json_file:
    json_data=json.load(json_file)
  lllon=json_data['corners'][0][1]
  lllat=json_data['corners'][0][0]
  urlon=json_data['corners'][2][1]
  urlat=json_data['corners'][1][0]
 
  width_meters = 120000*abs(lllon-urlon)
  height_meters = 120000*abs(lllat-urlat)
  cen_lon=(lllon+urlon)/2.0
  cen_lat=(lllat+urlat)/2.0
  truelat1=38.5
  truelat2=38.5
 
  m = Basemap(resolution='i',projection='lcc',width=width_meters,\
    height=height_meters,lat_0=cen_lat,lon_0=cen_lon,lat_1=truelat1,\
    lat_2=truelat2)

  x,y=m(lon,lat)

  width=10; height=8
  plt.figure(figsize=(width,height))
  m.drawstates(color='k')
  m.drawcoastlines(color='k')
  m.drawcountries(color='k')


  LEVS_rpt=np.arange(1.0,10.0,10)

#  wrfplot=plt.contour(x,y,severeprob,LEVS_rpt,colors='red')
 
  #LEVS=np.arange(0.05,1.05,0.05)
  LEVS=np.arange(0.02,0.335,0.015)
  wrfplot2=plt.contourf(x,y,forecprob,LEVS,cmap='jet',extend='max')
 
  plt.title('%s' % (titlestr), \
                fontsize=16,bbox=dict(facecolor='white', alpha=1.0),\
                x=0.5,y=.95,weight = 'demibold',style='oblique', \
                stretch='normal', family='sans-serif')

  F = plt.gcf()
  ax = plt.gca()  # Gets the current axes                                                                                                          
  divider = make_axes_locatable(ax)  # Lets us move axes around                                                                                    
  cax = divider.append_axes("right", size="2%",pad=0.23) #,axes_class=maxes.Axes) # Adds an axis for the colorbar                                    
  F.add_axes(cax)  # Adds the new axis to the figure as the current working axis                            
  bar = plt.colorbar(wrfplot2,cax=cax,orientation='vertical',format='%4.2f')
  bar.ax.tick_params(labelsize=20)
  plt.tight_layout()
  plt.savefig(outfile,format='png',bbox_inches='tight',dpi=100)
  plt.clf()
  plt.cla()
  plt.close('all')
 

def plotoutputd2(lon,lat,severeprob,forecprob,outfile,titlestr,jsontime):
  import json

  jsonfile='/condo/map3/ajohns14/hwt_dd2.'+jsontime+'.json'
  with open(jsonfile) as json_file:
    json_data=json.load(json_file)
  lllon=json_data['corners'][0][1]
  lllat=json_data['corners'][0][0]
  urlon=json_data['corners'][2][1]
  urlat=json_data['corners'][1][0]
 
  width_meters = 120000*abs(lllon-urlon)
  height_meters = 120000*abs(lllat-urlat)
  cen_lon=(lllon+urlon)/2.0
  cen_lat=(lllat+urlat)/2.0
  truelat1=38.5
  truelat2=38.5
 
  m = Basemap(resolution='i',projection='lcc',width=width_meters,\
    height=height_meters,lat_0=cen_lat,lon_0=cen_lon,lat_1=truelat1,\
    lat_2=truelat2)

  x,y=m(lon,lat)

  width=10; height=8
  plt.figure(figsize=(width,height))
  m.drawstates(color='k')
  m.drawcoastlines(color='k')
  m.drawcountries(color='k')


  LEVS_rpt=np.arange(1.0,10.0,10)

#  wrfplot=plt.contour(x,y,severeprob,LEVS_rpt,colors='red')

  LEVS=np.arange(0.02,0.335,0.015)

  wrfplot2=plt.contourf(x,y,forecprob,LEVS,cmap='jet',extend='max')
 
  plt.title('%s' % (titlestr), \
                fontsize=16,bbox=dict(facecolor='white', alpha=1.0),\
                x=0.5,y=.95,weight = 'demibold',style='oblique', \
                stretch='normal', family='sans-serif')

  F = plt.gcf()
  ax = plt.gca()  # Gets the current axes                                                                                                          
  divider = make_axes_locatable(ax)  # Lets us move axes around                                                                                    
  cax = divider.append_axes("right", size="2%",pad=0.23) #,axes_class=maxes.Axes) # Adds an axis for the colorbar                                    
  F.add_axes(cax)  # Adds the new axis to the figure as the current working axis                            
  bar = plt.colorbar(wrfplot2,cax=cax,orientation='vertical',format='%4.2f')
  bar.ax.tick_params(labelsize=20)
  plt.tight_layout()
  plt.savefig(outfile,format='png',bbox_inches='tight',dpi=100)
  plt.clf()
  plt.cla()
  plt.close('all')
 

