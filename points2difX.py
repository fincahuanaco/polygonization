import sys
import pandas as pd
import numpy as np
from scipy.ndimage.filters import gaussian_filter
from scipy.ndimage.filters import gaussian_laplace
import struct
import imageio
import time

def readcsv(filename): #vtk to csv

  #df = pd.read_csv(filename, header=None, sep = ',')
  df = pd.read_csv(filename, sep = ',')
  #print(df.shape)

  df = df[["Points:0","Points:1","Points:2"]]  #filter
  M=df.values[:,[0,1,2]] #old function was .as_matrix()

  return M

def readtxt(filename): #filipe file format
  M=[]
  with open(filename, "r") as localfile:
     n = int(localfile.readline())
     for line in localfile: #rest
       n,p1,p2,p3,v1,v2,v3= line.split()  
       M.append([float(p1),float(p2),float(p3)])
  return M


def limits(filename,wx,wy,wz):
  pM=readcsv(filename)  #we hope nx3 shape
  P=np.array(pM)

  xmin,xmax=99999,-99999
  ymin,ymax=99999,-99999
  zmin,zmax=99999,-99999
  for v in P:
    u=v#*float(sfactor) #500
    if(u[0]>xmax): 
      xmax=u[0]
    if(u[0]<xmin): 
      xmin=u[0]

    if(u[1]>ymax): 
      ymax=u[1]
    if(u[1]<ymin): 
      ymin=u[1]

    if(u[2]>zmax): 
      zmax=u[2]
    if(u[2]<zmin): 
      zmin=u[2]

  dx=(xmax-xmin)/wx #x
  dy=(ymax-ymin)/wy #y
  dz=(zmax-zmin)/wz #z

  print("%.2f %.2f"%(xmin,xmax),",","%.2f %.2f"%(ymin,ymax),",","%.2f %.2f"%(zmin,zmax))
  print("dx: ",dx,"dy: ",dy,"dz: ",dz)

def process(filename,wx,wy,wz):
  pM=readcsv(filename)  #we hope nx3 shape
  P=np.array(pM)
  print("wx: ",wx,"wy: ",wy,"wz: ",wz)

  image3d = np.zeros((wx,wy,wz),dtype=np.float32) #gray
 
  dx=0.55/wx  #1.2
  dy=0.55/wy 
  dz=0.55/wz 
  for v in P:
    i=int((v[0]-dx)/dx) +3
    j=int((v[1]-dy)/dy) +3
    k=int((v[2]-dz)/dz) +3
    image3d[j,i,k]=1 #binary
#    image3d[j,i,k]=image3d[j,i,k]+1 #counting
  
  return image3d

def save2grid(filename,volume,dimx,dimy,dimz):

  with open(filename, "wb") as file:
    for i in range(dimx):
      for j in range(dimy):
        for k in range(dimz):
          f = volume[i][j][k] #[3.14, 2.7, 0.0, -1.0, 1.1]
          b = struct.pack('f', f)
          file.write(b)

def Main(filename,dimx,dimy,dimz,vsigma):
  limits(filename,dimx,dimy,dimz)
  start=time.time()
  image=process(filename,dimx,dimy,dimz)
  print("Make cube take :%.2fs"%(time.time()-start))
  volmax=np.max(image)
  print("max(discrete volume) :",volmax)
  fileout="%s_%d"%( '.'.join(filename.split('.')[:-1]), dimx )
  print("Saving %s.dif"%fileout) #changed for differentiate
  save2grid("%s.dif"%fileout,image,dimx,dimy,dimz)

  #Smooth
  start=time.time()
  #blur = gaussian_filter(image, sigma=vsigma,truncate=2)
  blur = gaussian_laplace(image,vsigma,truncate=1)
  blur=0.85-blur
  blur = gaussian_filter(blur, sigma=vsigma,truncate=1)  
  print("Saving %s.sdif"%fileout)  #changed for differentiate
  save2grid("%s.sdif"%fileout,blur,dimx,dimy,dimz)
  print("Smoothing take %.2fs"%(time.time()-start))

  print("done..!")
  return 

if __name__ == "__main__":
  if(len(sys.argv)<6):
    print("Wrong parameters ...!")
    print("python3 particles2dif.py points.csv dimx dimy dimz sigma")
    exit()
  Main(sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]),float(sys.argv[5]))


