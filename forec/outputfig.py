import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap, addcyclic
from mpl_toolkits.axes_grid import make_axes_locatable
import matplotlib.axes as maxes
import math
import numpy as np


def getreports(rptfile,rptfile2,rptfile3,itime):
  windlat=[]
  windlon=[]
  haillat=[]
  haillon=[]
  torlat=[]
  torlon=[]
  sigwindlat=[]
  sigwindlon=[]
  sighaillat=[]
  sighaillon=[]
  sigtorlat=[]
  sigtorlon=[]

  infiles=[rptfile,rptfile2,rptfile3]
  for ifile in range(3):
    with open(infiles[ifile],"r") as fin:
      beginrpt=1
      tornrpt=0
      windrpt=0
      hailrpt=0
      for line in fin:
        tokens=line.split(",")
        print(tokens)
        if tokens[0]=='Time':
          if beginrpt == 1:
            beginrpt=0
            tornrpt=1
          elif tornrpt == 1:
            tornrpt=0
            windrpt=1
          elif windrpt == 1:
            windrpt=0
            hailrpt=1
        else:
          inttime=int(tokens[0])

          inthr=math.floor(inttime/100.0)
          intmin=inttime-(100*inthr)

          if ifile == 0:
            if inttime >= 1200:
              #inttime=inttime-2400
              inthr=inthr-24
              if intmin > 0:
                inthr=inthr+1
                intmin=60-intmin
              inttime=100*inthr + intmin
          elif ifile == 1:
            if inttime < 1200:
              inttime=inttime + 2400
          elif ifile == 2:
            if inttime < 1200:
              inttime=inttime + 4800
            else:
              inttime=inttime + 2400

          #print([inthr,intmin,inttime])

          if inttime >= 100*(itime-1) and inttime <= 100*(itime) + 5 :
            if tornrpt == 1:
              if tokens[1]=='UNK' or int(tokens[1]) < 2:
                torlat.append(float(tokens[5]))
                torlon.append(float(tokens[6]))
              else:
                sigtorlat.append(float(tokens[5]))
                sigtorlon.append(float(tokens[6]))
            elif windrpt == 1:
              if tokens[1]=='UNK' or int(tokens[1]) < 75:
                windlat.append(float(tokens[5]))
                windlon.append(float(tokens[6]))
                print(['wind',float(tokens[5]),float(tokens[6])])
              else:
                sigwindlat.append(float(tokens[5]))
                sigwindlon.append(float(tokens[6]))
                print(['sigwind',float(tokens[5]),float(tokens[6])])
            elif hailrpt ==1:
              if int(tokens[1]) >= 200 :
                sighaillat.append(float(tokens[5]))
                sighaillon.append(float(tokens[6]))
                print(['sighail',float(tokens[5]),float(tokens[6])])
              else:
                haillat.append(float(tokens[5]))
                haillon.append(float(tokens[6]))
                print(['hail',float(tokens[5]),float(tokens[6])])

  return windlat,windlon,haillat,haillon,torlat,torlon,sigwindlat,sigwindlon,sighaillat,sighaillon,sigtorlat,sigtorlon



     
def plotfig2(lon,lat,severeprob,forecprob,outfile,isev,casestr):
#def plotoutput(lon,lat,severeprob,forecprob,outfile,titlestr):
  import json
  import math
  import pygrib as grb
  import scipy.ndimage as ndimage
  from netCDF4 import Dataset
  from matplotlib.colors import BoundaryNorm
  fin = grb.open('/ourdisk/hpc/map/HWT_2022/radVTS/LAMprod_20220509000000/member001/radVTS01_202205090000f004.grib2')
  apcp_msg_f=fin.select()[872]

  nxin=92
  nyin=64
  nxout=1799 #1746
  nyout=1059 #1014
 
  #radius=18 #18
  radius=27 #18
  #radius=36 #18

  if casestr=='20220511':
    rptfile='/home/ajohns14/rf/fv3_2022/obs/rpts2022/220510_rpts.csv'
    rptfile2='/home/ajohns14/rf/fv3_2022/obs/rpts2022/220511_rpts.csv'
    rptfile3='/home/ajohns14/rf/fv3_2022/obs/rpts2022/220512_rpts.csv'
  elif casestr=='20220527':
    rptfile='/home/ajohns14/rf/fv3_2022/obs/rpts2022/220526_rpts.csv'
    rptfile2='/home/ajohns14/rf/fv3_2022/obs/rpts2022/220527_rpts.csv'
    rptfile3='/home/ajohns14/rf/fv3_2022/obs/rpts2022/220528_rpts.csv'
  else:
    print('storm reports not defined')
    exit()

  jsonfile='/condo/map3/ajohns14/hwt_dd1.'+casestr+'.json'
  with open(jsonfile) as json_file:
    json_data=json.load(json_file)
  lllon=json_data['corners'][0][1]
  lllat=json_data['corners'][0][0]
  urlon=json_data['corners'][2][1]
  urlat=json_data['corners'][1][0]
#  if lllon < 0:
#    lllon=lllon+360
#  if urlon < 0:
#    urlon=urlon+360

  print(['urlon,lon[20,20]: ',urlon,lon[20,20]])

  mindist1=999999
  mindist2=999999
  closest_i1=-1
  closest_j1=-1
  closest_i2=-1
  closest_j2=-1
  for jj in range(lat.shape[0]):
    for ii in range(lat.shape[1]):
      dist_from_center1=math.sqrt((lat[jj,ii]-lllat)*(lat[jj,ii]-lllat) + (lon[jj,ii]-lllon)*(lon[jj,ii]-lllon))
      dist_from_center2=math.sqrt((lat[jj,ii]-urlat)*(lat[jj,ii]-urlat) + (lon[jj,ii]-urlon)*(lon[jj,ii]-urlon))
      if dist_from_center1 < mindist1:
        mindist1=dist_from_center1
        closest_i1=ii
        closest_j1=jj
      if dist_from_center2 < mindist2:
        mindist2=dist_from_center2
        closest_i2=ii
        closest_j2=jj
  i1=closest_i1
  i2=closest_i2
  j1=closest_j1
  j2=closest_j2

  print(['j1,j2,i1,i2: ',j1,j2,i1,i2])

  #m=Basemap(resolution='i',projection='lcc',width=5000000,height=3500000,lat_0=38.5,lon_0=-97.5,lat_1=36.0,lat_2=36.0)
  #m=Basemap(resolution='i',projection='lcc',width=2000000,height=2000000,lat_0=38.5,lon_0=-83.0,lat_1=36.0,lat_2=36.0)
  if casestr=='20220511':
    m=Basemap(resolution='i',projection='lcc',lat_0=38.5,lon_0=-97.0,lat_1=36.0,lat_2=36.0,llcrnrlon=lllon,urcrnrlon=urlon,llcrnrlat=lllat,urcrnrlat=urlat)
  else:
    m=Basemap(resolution='i',projection='lcc',lat_0=38.5,lon_0=-83.0,lat_1=36.0,lat_2=36.0,llcrnrlon=lllon,urcrnrlon=urlon,llcrnrlat=lllat,urcrnrlat=urlat)
  x,y=m(lon,lat)

  width=10; height=8
  plt.figure(figsize=(width,height))
  m.drawstates(color='k')
  m.drawcoastlines(color='k')
  m.drawcountries(color='k')


  LEVS_rpt=np.arange(1.0,10.0,10)

  #wrfplot=plt.contour(x,y,severeprob,LEVS_rpt,colors='red',linewidths=1.0)


  forecprobsm=ndimage.gaussian_filter(forecprob,sigma=1)

  LEVS=np.arange(0.02,0.52,0.02)

  #wrfplot2=plt.contourf(x,y,forecprobsm,LEVS,cmap='jet',extend='max')

  if isev==5:
    LEVSb=[0.02,0.05,0.10,0.15,0.30,0.45,0.60]
    #LEVSb=[0.02,0.05,0.10,0.15,0.30,0.45,0.60,0.61]
    LEVSc=[0.01,0.035,0.075,0.125,0.20,0.25,0.50,0.55]
    mycmap=['#008000','#653700','#FFD700','#FF0000','#FF00FF','#7E1E9C','#000080']
    #mycmap=(matplotlib.colors.ListedColormap(['#008000','#653700','#FFD700','#FF0000','#FF00FF','#7E1E9C','#000080']))
  elif isev==7:
    mycmap=['black']
    LEVSb=[0.10]
  else:
    mycmap=['#653700','#FFD700','#FF0000','#FF00FF','#7E1E9C']
    #mycmap=(matplotlib.colors.ListedColormap(['#653700','#FFD700','#FF0000','#FF00FF','#7E1E9C']))
    LEVSb=[0.05,0.15,0.30,0.45,0.60]
    #LEVSb=[0.05,0.15,0.30,0.45,0.60,0.70]
    LEVSc=[0.10,0.20,0.25,0.35,0.40,0.50]
  
  #bnorm = BoundaryNorm(LEVSb, ncolors=len(LEVSb)-1, clip=True)

  #wrfplot2=plt.contourf(x,y,forecprobsm,LEVS,cmap=mycmap,extend='max',norm=bnorm)
#  wrfplot2=plt.contour(x,y,forecprobsm,LEVSb,colors='black',linewidths=1.0)
  for icol in range(len(LEVSb)):
    LEVSx=np.arange(LEVSb[icol],LEVSb[icol]+10.0,10.0)
    wrfplot3=plt.contour(x,y,forecprobsm,LEVSx,colors=mycmap[icol],linewidths=3.0,zorder=100)
#  wrfplot3=plt.contour(x,y,forecprobsm,LEVSc,colors=mycmap,linewidths=1.0)


 
  for itime in range(12,37):
    windlat,windlon,haillat,haillon,torlat,torlon,sigwindlat,sigwindlon,sighaillat,sighaillon,sigtorlat,sigtorlon = getreports(rptfile,rptfile2,rptfile3,itime)
    if isev==0:
      print(len(windlat),len(torlat))
      for irpt in range(len(windlat)):
        xx, yy = m(windlon[irpt], windlat[irpt])
        plot = m.scatter(xx, yy, c='blue', s=80, edgecolors='none',zorder=15,marker='s')
      for irpt in range(len(sigwindlat)):
        xx, yy = m(sigwindlon[irpt], sigwindlat[irpt])
        plot = m.scatter(xx, yy, c='black', s=80, edgecolors='none',zorder=20,marker='s')
      for irpt in range(len(haillat)):
        xx, yy = m(haillon[irpt], haillat[irpt])
        plot = m.scatter(xx, yy, c='green', s=80, edgecolors='none',zorder=15,marker='o')
      for irpt in range(len(sighaillat)):
        xx, yy = m(sighaillon[irpt], sighaillat[irpt])
        plot = m.scatter(xx, yy, c='black', s=80, edgecolors='none',zorder=20,marker='o')
      for irpt in range(len(torlat)):
        xx, yy = m(torlon[irpt], torlat[irpt])
        plot = m.scatter(xx, yy, c='red', s=80, edgecolors='none',zorder=15,marker='v')
      for irpt in range(len(sigtorlat)):
        xx, yy = m(sigtorlon[irpt], sigtorlat[irpt])
        plot = m.scatter(xx, yy, c='black', s=80, edgecolors='none',zorder=20,marker='v')

    elif isev==1:

      for irpt in range(len(windlat)): 
        xx, yy = m(windlon[irpt], windlat[irpt])
        plot = m.scatter(xx, yy, c='blue', s=80, edgecolors='none',zorder=15,marker='s')
      for irpt in range(len(sigwindlat)): 
        xx, yy = m(sigwindlon[irpt], sigwindlat[irpt])
        plot = m.scatter(xx, yy, c='black', s=80, edgecolors='none',zorder=20,marker='s')

    elif isev==3:

      for irpt in range(len(haillat)):
        xx, yy = m(haillon[irpt], haillat[irpt])
        plot = m.scatter(xx, yy, c='green', s=80, edgecolors='none',zorder=15,marker='o')
      for irpt in range(len(sighaillat)):
        xx, yy = m(sighaillon[irpt], sighaillat[irpt])
        plot = m.scatter(xx, yy, c='black', s=80, edgecolors='none',zorder=20,marker='o')

    elif isev==5:

      for irpt in range(len(torlat)):
        xx, yy = m(torlon[irpt], torlat[irpt])
        plot = m.scatter(xx, yy, c='red', s=80, edgecolors='none',zorder=15,marker='v')
      for irpt in range(len(sigtorlat)):
        xx, yy = m(sigtorlon[irpt], sigtorlat[irpt])
        plot = m.scatter(xx, yy, c='black', s=80, edgecolors='none',zorder=20,marker='v')

    elif isev==7:

      for irpt in range(len(windlat)):
        xx, yy = m(windlon[irpt], windlat[irpt])
        plot = m.scatter(xx, yy, c='blue', s=80, edgecolors='none',zorder=15,marker='s')
      for irpt in range(len(sighaillat)):
        xx, yy = m(sighaillon[irpt], sighaillat[irpt])
        plot = m.scatter(xx, yy, c='black', s=80, edgecolors='none',zorder=20,marker='o')
      for irpt in range(len(sigtorlat)):
        xx, yy = m(sigtorlon[irpt], sigtorlat[irpt])
        plot = m.scatter(xx, yy, c='black', s=80, edgecolors='none',zorder=20,marker='v')

  F = plt.gcf()
  ax = plt.gca()  # Gets the current axes                                                                                                          
#  divider = make_axes_locatable(ax)  # Lets us move axes around                                                                                    
#  cax = divider.append_axes("right", size="2%",pad=0.23) #,axes_class=maxes.Axes) # Adds an axis for the colorbar                                    
#  F.add_axes(cax)  # Adds the new axis to the figure as the current working axis                            
#  bar = plt.colorbar(wrfplot2,cax=cax,orientation='vertical',format='%4.2f')
#  bar.ax.tick_params(labelsize=20)
  plt.tight_layout()
  plt.savefig(outfile,format='png',bbox_inches='tight',dpi=100)
  plt.clf()
  plt.cla()
  plt.close('all')
    
def plotfig12(lon,lat,severeprob,forecprob,outfile,isev):
#def plotoutput(lon,lat,severeprob,forecprob,outfile,titlestr):
  import pygrib as grb
  import scipy.ndimage as ndimage
  from netCDF4 import Dataset
  from matplotlib.colors import BoundaryNorm
  fin = grb.open('/ourdisk/hpc/map/HWT_2022/radVTS/LAMprod_20220509000000/member001/radVTS01_202205090000f004.grib2')
  apcp_msg_f=fin.select()[872]

  nxin=92
  nyin=64
  nxout=1799 #1746
  nyout=1059 #1014
 
  #radius=18 #18
  radius=27 #18
  #radius=36 #18


  #m=Basemap(resolution='i',projection='lcc',width=5000000,height=3500000,lat_0=38.5,lon_0=-97.5,lat_1=36.0,lat_2=36.0)
  m=Basemap(resolution='i',projection='lcc',width=2000000,height=2000000,lat_0=38.5,lon_0=-83.0,lat_1=36.0,lat_2=36.0)
  x,y=m(lon,lat)

  width=10; height=8
  plt.figure(figsize=(width,height))
  m.drawstates(color='k')
  m.drawcoastlines(color='k')
  m.drawcountries(color='k')


  LEVS_rpt=np.arange(1.0,10.0,10)

  wrfplot=plt.contour(x,y,severeprob,LEVS_rpt,colors='red',linewidths=1.0)


  forecprobsm=ndimage.gaussian_filter(forecprob,sigma=1)

  LEVS=np.arange(0.02,0.52,0.02)

  wrfplot2=plt.contourf(x,y,forecprobsm,LEVS,cmap='jet',extend='max')

  if isev==5:
    LEVSb=[0.02,0.05,0.10,0.15,0.30,0.45,0.60]
    #LEVSb=[0.02,0.05,0.10,0.15,0.30,0.45,0.60,0.61]
    LEVSc=[0.01,0.035,0.075,0.125,0.20,0.25,0.50,0.55]
    mycmap=['#008000','#653700','#FFD700','#FF0000','#FF00FF','#7E1E9C','#000080']
    #mycmap=(matplotlib.colors.ListedColormap(['#008000','#653700','#FFD700','#FF0000','#FF00FF','#7E1E9C','#000080']))
  elif isev==7:
    mycmap=['black']
    LEVSb=[0.10]
  else:
    mycmap=['#653700','#FFD700','#FF0000','#FF00FF','#7E1E9C']
    #mycmap=(matplotlib.colors.ListedColormap(['#653700','#FFD700','#FF0000','#FF00FF','#7E1E9C']))
    LEVSb=[0.05,0.15,0.30,0.45,0.60]
    #LEVSb=[0.05,0.15,0.30,0.45,0.60,0.70]
    LEVSc=[0.10,0.20,0.25,0.35,0.40,0.50]
  
  #bnorm = BoundaryNorm(LEVSb, ncolors=len(LEVSb)-1, clip=True)

  #wrfplot2=plt.contourf(x,y,forecprobsm,LEVS,cmap=mycmap,extend='max',norm=bnorm)
#  wrfplot2=plt.contour(x,y,forecprobsm,LEVSb,colors='black',linewidths=1.0)
  for icol in range(len(LEVSb)):
    LEVSx=np.arange(LEVSb[icol],LEVSb[icol]+10.0,10.0)
    wrfplot3=plt.contour(x,y,forecprobsm,LEVSx,colors=mycmap[icol],linewidths=3.0)
#  wrfplot3=plt.contour(x,y,forecprobsm,LEVSc,colors=mycmap,linewidths=1.0)


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
   
def plotfig10(lon,lat,severeprob,forecprob,outfile,isev):
#def plotoutput(lon,lat,severeprob,forecprob,outfile,titlestr):
  import pygrib as grb
  import scipy.ndimage as ndimage
  from netCDF4 import Dataset
  from matplotlib.colors import BoundaryNorm
  fin = grb.open('/ourdisk/hpc/map/HWT_2022/radVTS/LAMprod_20220509000000/member001/radVTS01_202205090000f004.grib2')
  apcp_msg_f=fin.select()[872]

  nxin=92
  nyin=64
  nxout=1799 #1746
  nyout=1059 #1014
 
  #radius=18 #18
  radius=27 #18
  #radius=36 #18


  #m=Basemap(resolution='i',projection='lcc',width=5000000,height=3500000,lat_0=38.5,lon_0=-97.5,lat_1=36.0,lat_2=36.0)
  m=Basemap(resolution='i',projection='lcc',width=3000000,height=2500000,lat_0=38.5,lon_0=-97.5,lat_1=36.0,lat_2=36.0)
  x,y=m(lon,lat)

  width=10; height=8
  plt.figure(figsize=(width,height))
  m.drawstates(color='k')
  m.drawcoastlines(color='k')
  m.drawcountries(color='k')


  LEVS_rpt=np.arange(1.0,10.0,10)

  wrfplot=plt.contour(x,y,severeprob,LEVS_rpt,colors='red',linewidths=1.0)


  forecprobsm=ndimage.gaussian_filter(forecprob,sigma=1)

  LEVS=np.arange(0.02,0.52,0.02)

  wrfplot2=plt.contourf(x,y,forecprobsm,LEVS,cmap='jet',extend='max')

  if isev==5:
    LEVSb=[0.02,0.05,0.10,0.15,0.30,0.45,0.60]
    #LEVSb=[0.02,0.05,0.10,0.15,0.30,0.45,0.60,0.61]
    LEVSc=[0.01,0.035,0.075,0.125,0.20,0.25,0.50,0.55]
    mycmap=['#008000','#653700','#FFD700','#FF0000','#FF00FF','#7E1E9C','#000080']
    #mycmap=(matplotlib.colors.ListedColormap(['#008000','#653700','#FFD700','#FF0000','#FF00FF','#7E1E9C','#000080']))
  elif isev==7:
    mycmap=['black']
    LEVSb=[0.10]
  else:
    mycmap=['#653700','#FFD700','#FF0000','#FF00FF','#7E1E9C']
    #mycmap=(matplotlib.colors.ListedColormap(['#653700','#FFD700','#FF0000','#FF00FF','#7E1E9C']))
    LEVSb=[0.05,0.15,0.30,0.45,0.60]
    #LEVSb=[0.05,0.15,0.30,0.45,0.60,0.70]
    LEVSc=[0.10,0.20,0.25,0.35,0.40,0.50]
  
  #bnorm = BoundaryNorm(LEVSb, ncolors=len(LEVSb)-1, clip=True)

  #wrfplot2=plt.contourf(x,y,forecprobsm,LEVS,cmap=mycmap,extend='max',norm=bnorm)
#  wrfplot2=plt.contour(x,y,forecprobsm,LEVSb,colors='black',linewidths=1.0)
  for icol in range(len(LEVSb)):
    LEVSx=np.arange(LEVSb[icol],LEVSb[icol]+10.0,10.0)
    wrfplot3=plt.contour(x,y,forecprobsm,LEVSx,colors=mycmap[icol],linewidths=3.0)
#  wrfplot3=plt.contour(x,y,forecprobsm,LEVSc,colors=mycmap,linewidths=1.0)


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
 

