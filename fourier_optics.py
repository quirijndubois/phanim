import numpy as np
from phanim.quickplot import canvasPlot
from scipy.fft import fft2
from scipy.fft import ifft2
from scipy.fft import fftfreq
from scipy.fft import fftshift
import cv2
import matplotlib.pyplot as plt

class Canvas():
    def __init__(self,range,res):
        self.res = res
        self.range = range
        self.x = np.linspace(-range,range,res)
        self.xv,self.yv = np.meshgrid(self.x,self.x)
    
    def generateSlit(self,thickness,height):
        self.picture = (np.abs(self.xv) < thickness/2) * (np.abs(self.yv)< height/2)
        self.picture = self.picture.astype(float)
        
    def generateDoubleSlit(self,thickness,height,seperation):
        self.picture = (
            (np.abs(self.xv - seperation/2) < thickness/2) * (np.abs(self.yv)<height/2) + 
            (np.abs(self.xv + seperation/2) < thickness/2) * (np.abs(self.yv)<height/2)
        )
        self.picture = self.picture.astype(float)
        
    def generateCircle(self,radius):
        self.picture = (self.xv**2+self.yv**2 < radius**2)
        self.picture = self.picture.astype(float)

    def experiment(self,lam,distance):
        A = fft2(self.picture)
        kx = fftfreq(len(self.x),np.diff(self.x)[0]) * 2 * np.pi
        kxv, kyv = np.meshgrid(kx,kx)
        k = 2*np.pi / (lam)
        self.picture = np.abs(ifft2(A*np.exp(1j*distance*np.sqrt(k**2-kxv**2-kyv**2))))

    def loadImage(self,path,inverse=False):
        img = cv2.imread(path)
        if inverse:
            img = cv2.bitwise_not(img)
        img = np.pad(img, 200, mode = 'constant')
        img = cv2.resize(img,dsize=(int(self.res),int(self.res)),interpolation=cv2.INTER_CUBIC)
        self.picture = np.array(img).sum(axis=2).astype(float)
        self.x = np.linspace(-self.range,self.range,self.picture.shape[0])
        self.xv,self.yv = np.meshgrid(self.x,self.x)
        
    def plot(self,pic = False, size = False, figSize = 5, aspectRatio = 1, inferno = True):
        if size == False:
            size = self.xv[0][0]*-1
        
        if pic == False:
            pic = self.picture
        canvasPlot(self,pic,aspectRatio,figSize,size,inferno=inferno)

def plotDiffraction(c,aspectRatio,figSize,size):
  A = fft2(c.U0)
  kx = fftfreq(len(c.x),np.diff(c.x)[0]) * 2 * np.pi
  kxv, kyv = np.meshgrid(kx,kx)
  plt.figure(figsize=(figSize,figSize*aspectRatio))
  plt.pcolormesh(fftshift(kxv.magnitude),fftshift(kyv.magnitude),np.abs(fftshift(A)))
  plt.xlim(-size,size)
  plt.ylim(-size*aspectRatio,size*aspectRatio)
  plt.show()