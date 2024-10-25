import numpy as np

def getseveres(wind_rpt,sigwind_rpt,hail_rpt,sighail_rpt,tor_rpt,sigtor_rpt):

  allsevere=np.zeros(7)
  windsevere=np.zeros(7)
  sigwindsevere=np.zeros(7)
  hailsevere=np.zeros(7)
  sighailsevere=np.zeros(7)
  torsevere=np.zeros(7)
  sigtorsevere=np.zeros(7)

  for itime in range(12,16):
          if wind_rpt[itime] > 0.5:
            allsevere[0] = 1.0
            allsevere[1] = 1.0
            windsevere[0] = 1.0
            windsevere[1] = 1.0
          if hail_rpt[itime] > 0.5:
            allsevere[0] = 1.0
            allsevere[1] = 1.0
            hailsevere[0] = 1.0
            hailsevere[1] = 1.0
          if tor_rpt[itime] > 0.5:
            allsevere[0] = 1.0
            allsevere[1] = 1.0
            torsevere[0] = 1.0
            torsevere[1] = 1.0
          if sigwind_rpt[itime] > 0.5:
            allsevere[0] = 1.0
            allsevere[1] = 1.0
            windsevere[0] = 1.0
            windsevere[1] = 1.0
            sigwindsevere[0] = 1.0
            sigwindsevere[1] = 1.0
          if sighail_rpt[itime] > 0.5:
            allsevere[0] = 1.0
            allsevere[1] = 1.0
            hailsevere[0] = 1.0
            hailsevere[1] = 1.0
            sighailsevere[0] = 1.0
            sighailsevere[1] = 1.0
          if sigtor_rpt[itime] > 0.5:
            allsevere[0] = 1.0
            allsevere[1] = 1.0
            torsevere[0] = 1.0
            torsevere[1] = 1.0
            sigtorsevere[0] = 1.0
            sigtorsevere[1] = 1.0


  for itime in range(16,20):
          if wind_rpt[itime] > 0.5:
            allsevere[0] = 1.0
            allsevere[2] = 1.0
            windsevere[0] = 1.0
            windsevere[2] = 1.0
          if hail_rpt[itime] > 0.5:
            allsevere[0] = 1.0
            allsevere[2] = 1.0
            hailsevere[0] = 1.0
            hailsevere[2] = 1.0
          if tor_rpt[itime] > 0.5:
            allsevere[0] = 1.0
            allsevere[2] = 1.0
            torsevere[0] = 1.0
            torsevere[2] = 1.0
          if sigwind_rpt[itime] > 0.5:
            allsevere[0] = 1.0
            allsevere[2] = 1.0
            windsevere[0] = 1.0
            windsevere[2] = 1.0
            sigwindsevere[0] = 1.0
            sigwindsevere[2] = 1.0
          if sighail_rpt[itime] > 0.5:
            allsevere[0] = 1.0
            allsevere[2] = 1.0
            hailsevere[0] = 1.0
            hailsevere[2] = 1.0
            sighailsevere[0] = 1.0
            sighailsevere[2] = 1.0
          if sigtor_rpt[itime] > 0.5:
            allsevere[0] = 1.0
            allsevere[2] = 1.0
            torsevere[0] = 1.0
            torsevere[2] = 1.0
            sigtorsevere[0] = 1.0
            sigtorsevere[2] = 1.0


  for itime in range(20,24):
          if wind_rpt[itime] > 0.5:
            allsevere[0] = 1.0
            allsevere[3] = 1.0
            windsevere[0] = 1.0
            windsevere[3] = 1.0
          if hail_rpt[itime] > 0.5:
            allsevere[0] = 1.0
            allsevere[3] = 1.0
            hailsevere[0] = 1.0
            hailsevere[3] = 1.0
          if tor_rpt[itime] > 0.5:
            allsevere[0] = 1.0
            allsevere[3] = 1.0
            torsevere[0] = 1.0
            torsevere[3] = 1.0
          if sigwind_rpt[itime] > 0.5:
            allsevere[0] = 1.0
            allsevere[3] = 1.0
            windsevere[0] = 1.0
            windsevere[3] = 1.0
            sigwindsevere[0] = 1.0
            sigwindsevere[3] = 1.0
          if sighail_rpt[itime] > 0.5:
            allsevere[0] = 1.0
            allsevere[3] = 1.0
            hailsevere[0] = 1.0
            hailsevere[3] = 1.0
            sighailsevere[0] = 1.0
            sighailsevere[3] = 1.0
          if sigtor_rpt[itime] > 0.5:
            allsevere[0] = 1.0
            allsevere[3] = 1.0
            torsevere[0] = 1.0
            torsevere[3] = 1.0
            sigtorsevere[0] = 1.0
            sigtorsevere[3] = 1.0


  for itime in range(24,28):
          if wind_rpt[itime] > 0.5:
            allsevere[0] = 1.0
            allsevere[4] = 1.0
            windsevere[0] = 1.0
            windsevere[4] = 1.0
          if hail_rpt[itime] > 0.5:
            allsevere[0] = 1.0
            allsevere[4] = 1.0
            hailsevere[0] = 1.0
            hailsevere[4] = 1.0
          if tor_rpt[itime] > 0.5:
            allsevere[0] = 1.0
            allsevere[4] = 1.0
            torsevere[0] = 1.0
            torsevere[4] = 1.0
          if sigwind_rpt[itime] > 0.5:
            allsevere[0] = 1.0
            allsevere[4] = 1.0
            windsevere[0] = 1.0
            windsevere[4] = 1.0
            sigwindsevere[0] = 1.0
            sigwindsevere[4] = 1.0
          if sighail_rpt[itime] > 0.5:
            allsevere[0] = 1.0
            allsevere[4] = 1.0
            hailsevere[0] = 1.0
            hailsevere[4] = 1.0
            sighailsevere[0] = 1.0
            sighailsevere[4] = 1.0
          if sigtor_rpt[itime] > 0.5:
            allsevere[0] = 1.0
            allsevere[4] = 1.0
            torsevere[0] = 1.0
            torsevere[4] = 1.0
            sigtorsevere[0] = 1.0
            sigtorsevere[4] = 1.0


  for itime in range(28,32):
          if wind_rpt[itime] > 0.5:
            allsevere[0] = 1.0
            allsevere[5] = 1.0
            windsevere[0] = 1.0
            windsevere[5] = 1.0
          if hail_rpt[itime] > 0.5:
            allsevere[0] = 1.0
            allsevere[5] = 1.0
            hailsevere[0] = 1.0
            hailsevere[5] = 1.0
          if tor_rpt[itime] > 0.5:
            allsevere[0] = 1.0
            allsevere[5] = 1.0
            torsevere[0] = 1.0
            torsevere[5] = 1.0
          if sigwind_rpt[itime] > 0.5:
            allsevere[0] = 1.0
            allsevere[5] = 1.0
            windsevere[0] = 1.0
            windsevere[5] = 1.0
            sigwindsevere[0] = 1.0
            sigwindsevere[5] = 1.0
          if sighail_rpt[itime] > 0.5:
            allsevere[0] = 1.0
            allsevere[5] = 1.0
            hailsevere[0] = 1.0
            hailsevere[5] = 1.0
            sighailsevere[0] = 1.0
            sighailsevere[5] = 1.0
          if sigtor_rpt[itime] > 0.5:
            allsevere[0] = 1.0
            allsevere[5] = 1.0
            torsevere[0] = 1.0
            torsevere[5] = 1.0
            sigtorsevere[0] = 1.0
            sigtorsevere[5] = 1.0


  for itime in range(32,36):
          if wind_rpt[itime] > 0.5:
            allsevere[0] = 1.0
            allsevere[6] = 1.0
            windsevere[0] = 1.0
            windsevere[6] = 1.0
          if hail_rpt[itime] > 0.5:
            allsevere[0] = 1.0
            allsevere[6] = 1.0
            hailsevere[0] = 1.0
            hailsevere[6] = 1.0
          if tor_rpt[itime] > 0.5:
            allsevere[0] = 1.0
            allsevere[6] = 1.0
            torsevere[0] = 1.0
            torsevere[6] = 1.0
          if sigwind_rpt[itime] > 0.5:
            allsevere[0] = 1.0
            allsevere[6] = 1.0
            windsevere[0] = 1.0
            windsevere[6] = 1.0
            sigwindsevere[0] = 1.0
            sigwindsevere[6] = 1.0
          if sighail_rpt[itime] > 0.5:
            allsevere[0] = 1.0
            allsevere[6] = 1.0
            hailsevere[0] = 1.0
            hailsevere[6] = 1.0
            sighailsevere[0] = 1.0
            sighailsevere[6] = 1.0
          if sigtor_rpt[itime] > 0.5:
            allsevere[0] = 1.0
            allsevere[6] = 1.0
            torsevere[0] = 1.0
            torsevere[6] = 1.0
            sigtorsevere[0] = 1.0
            sigtorsevere[6] = 1.0


  return allsevere,windsevere,sigwindsevere,hailsevere,sighailsevere,torsevere,sigtorsevere    
